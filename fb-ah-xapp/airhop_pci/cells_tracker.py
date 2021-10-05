#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List, Tuple, Union
import logging

from onos_e2_sm.e2sm_rc_pre.v2 import (
    BitString,
    CellGlobalId,
    E2SmRcPreIndicationHeaderFormat1,
    E2SmRcPreIndicationMessageFormat1,
    NrcellIdentity,
    Nrcgi,
    PlmnIdentity,
)


CELLID_BITWIDTH = 36
PLMNID_BITWIDTH = 24


@dataclass
class CellChanges:
    ncgi: int
    is_update: bool  # distinguishes new vs updated cells
    cell_to_register: Optional["CellsState"] = field(default=None)
    neighbors_to_add: Dict[int, int] = field(default_factory=dict)  # maps ncgi -> pci
    neighbors_to_remove: List[int] = field(default_factory=list)  # list of ncgi
    neighbors_to_update: Dict[int, int] = field(
        default_factory=dict
    )  # maps ncgi -> pci
    nci: int = field(init=False)  # NRCellIdentity, lower 36 bits of ncgi

    def __post_init__(self):
        nci_mask = (0x1 << CELLID_BITWIDTH) - 1
        self.nci = self.ncgi & nci_mask


def bytes_nci_bitstring(nci: int, bits: int) -> BitString:
    """convert an integer value to an APER BitString

    for a 36 bit number like 0x123456789,
    represented as a bitstring of 5 bytes: [0x12, 0x34, 0x56, 0x78, 0x90]
    to do this, we pad it at the LSB 0x1234567890, then convert it via big endian

    ["0x%x" % e for e in int.to_bytes(0x123456789 << 4, 5, byteorder="big")]

    ONF says that this is how APER encoding works for bit strings
    """

    # round up to minimum number of bytes required to represent 'bits' bits
    bytecnt = -(-bits // 8)
    bitstring_bits = bytecnt * 8

    # if the data in the bitstring exceeds the actual data, the data needs to be
    #   shifted to up to keep the 0 padding at the end of the bitstring.
    shift = bitstring_bits - bits

    return BitString(
        value=int.to_bytes(nci << shift, bytecnt, byteorder="big"), len=bits
    )


def parse_nci_bitstring(n_rcell_identity: BitString) -> int:
    """convert an APER BitString to an integer

    For a 36-bit bitstring encoded as 5 bytes, [0x12, 0x34, 0x56, 0x78, 0x90]
    there are 4 bits of padding at the end to fill the byte.

    When converted to a value, that padding needs to be stripped off, by
    shifting the nibble off.
    0x1234567890 >> 4 = 0x123456789

    ONF says that this is how APER encoding works for bit strings
    """

    bitstring_bits = len(n_rcell_identity.value.value) * 8
    bits = n_rcell_identity.value.len

    # calculate the amount of 0 padding needs to be stripped off the LSB side
    shift = bitstring_bits - bits

    return (
        int.from_bytes(
            n_rcell_identity.value.value,
            byteorder="big",
            signed=False,
        )
        >> shift
    )


def cgiFromNcgi(ncgi: int) -> CellGlobalId:
    # ncgi = (plmnid << CELLID_BITWIDTH) | nci

    # nci bitwidth = CELLID_BITWIDTH
    # plmnid bitwidth = PLMNID_BITWIDTH
    plmnid_mask = (0x1 << PLMNID_BITWIDTH) - 1
    plmnid = (ncgi >> CELLID_BITWIDTH) & plmnid_mask
    nci_mask = (0x1 << CELLID_BITWIDTH) - 1
    nci = ncgi & nci_mask
    return CellGlobalId(
        nr_cgi=Nrcgi(
            p_lmn_identity=PlmnIdentity(
                value=int.to_bytes(plmnid, 3, byteorder="little")
            ),
            n_rcell_identity=NrcellIdentity(value=bytes_nci_bitstring(nci, bits=36)),
        )
    )


@dataclass
class CellsState:
    """
    given indication_message of E2SmRcPreIndicationMessageFormat1,
    create dataclass of cell state
    """

    indication_header: E2SmRcPreIndicationHeaderFormat1 = field(
        default=None, repr=False
    )
    indication_message: E2SmRcPreIndicationMessageFormat1 = field(
        default=None, repr=False
    )
    cgi: CellGlobalId = field(init=False)
    ncgi: int = field(init=False)
    nci: int = field(init=False)
    e2_node_id: str = field(default="", repr=False)
    neighbors: Dict[int, Tuple[int, int]] = field(init=False)  # maps ncgi -> (pci, fcn)
    pci: Optional[int] = field(init=False)
    fcn: Optional[int] = field(init=False)
    plmnid: int = field(init=False)

    # Optional fields for display
    lat: float = field(default=0)
    lng: float = field(default=0)
    azimuth: float = field(default=0)
    arc_width: float = field(default=0)
    tilt: float = field(default=0)
    height: float = field(default=0)

    def __post_init__(self):
        self.cgi = self.indication_header.cgi
        self.plmnid = int.from_bytes(
            self.indication_header.cgi.nr_cgi.p_lmn_identity.value,
            byteorder="little",
            signed=False,
        )
        self.nci = parse_nci_bitstring(
            self.indication_header.cgi.nr_cgi.n_rcell_identity
        )
        self.ncgi = (self.plmnid << CELLID_BITWIDTH) | self.nci
        self.pci = self.indication_message.pci.value
        self.fcn = self.indication_message.dl_arfcn.nr_arfcn.value

        self.neighbors: Dict[int, Tuple[int, int]] = {}  # maps ncgi -> (pci, fcn)
        for n in self.indication_message.neighbors:
            n_plmnid = int.from_bytes(
                n.cgi.nr_cgi.p_lmn_identity.value, byteorder="little", signed=False
            )
            n_nci = parse_nci_bitstring(n.cgi.nr_cgi.n_rcell_identity)
            n_ncgi = (n_plmnid << CELLID_BITWIDTH) | n_nci
            n_pci = n.pci.value
            n_fcn = n.dl_arfcn.nr_arfcn.value
            if n_ncgi in self.neighbors:
                logging.error(
                    f"Cannot monitor cell, bad data in neighbors. "
                    f"ncgi=0x{n_ncgi:x} already exists in {sorted(self.neighbors)}. "
                    f"msg={self.indication_message}"
                )
                raise Exception(f"repeated neighbor ncgi 0x{n_ncgi:x}")
            self.neighbors[n_ncgi] = (n_pci, n_fcn)

    def __xor__(self, other: "CellsState") -> Optional[CellChanges]:
        """
        calculates difference between self and other
        returns difference using CellChanges
        """
        if self.ncgi != other.ncgi:
            raise Exception("ncgi differs, cannot calculate change")

        current_neighbors = set(self.neighbors.keys())
        new_neighbors = set(other.neighbors.keys())

        same_neighbors = current_neighbors & new_neighbors
        removed_neighbors = current_neighbors - same_neighbors
        added_neighbors = new_neighbors - same_neighbors
        updated_neighbors = set()

        # check pci values of same_neighbors to see if any pci is changed
        # if different, add it to the updated_neighbors set to issue update
        for n_ncgi in same_neighbors:
            if self.neighbors[n_ncgi] != other.neighbors[n_ncgi]:
                updated_neighbors.add(n_ncgi)

        if len(added_neighbors) + len(removed_neighbors) + len(updated_neighbors) == 0:
            return None

        return CellChanges(
            ncgi=self.ncgi,
            is_update=True,
            neighbors_to_add={
                k: v for k, v in other.neighbors.items() if k in added_neighbors
            },
            neighbors_to_update={
                k: v for k, v in other.neighbors.items() if k in updated_neighbors
            },
            neighbors_to_remove=list(removed_neighbors),
        )


class CellsTracker:
    def __init__(self):
        self.ncgi_cells_map: Dict[int, CellsState] = {}

    def dump(
        self,
    ) -> List[Dict[str, Union[int, str, List[Dict[str, Union[int, str]]]]]]:
        return [
            {
                "ncgi": hex(ncgi),
                "pci": cs.pci,
                "neighbors": [
                    {"ncgi": hex(k), "pci": v}
                    for k, (v, _) in sorted(cs.neighbors.items())
                ],
                "location": {
                    "lat": cs.lat,
                    "lng": cs.lng,
                },
                "sector": {
                    "azimuth": cs.azimuth,
                    "arc": cs.arc_width,
                    "centroid": {
                        "lat": cs.lat,
                        "lng": cs.lng,
                    },
                },
            }
            for ncgi, cs in sorted(self.ncgi_cells_map.items())
        ]

    def update(
        self,
        e2_node_id: str,
        indication_header: E2SmRcPreIndicationHeaderFormat1,
        indication_message: E2SmRcPreIndicationMessageFormat1,
    ) -> CellChanges:
        """
        given a new e2sm_rc_pre indication message,
        return list of change operations,
        such as new cells, added or removed neighbors
        """
        cs = CellsState(
            indication_header=indication_header,
            indication_message=indication_message,
            e2_node_id=e2_node_id,
        )

        try:
            if cs.ncgi in self.ncgi_cells_map:
                if cs.pci != self.ncgi_cells_map[cs.ncgi].pci:
                    logging.debug(f"ncgi=0x{cs.ncgi:x} " f"update pci {cs.pci}")
                    return CellChanges(
                        ncgi=cs.ncgi,
                        is_update=True,
                        cell_to_register=cs,
                    )
                neighbor_changes = self.ncgi_cells_map[cs.ncgi] ^ cs
                logging.debug(
                    f"ncgi=0x{cs.ncgi:x} already tracked, "
                    f"neighbor_diff={neighbor_changes}"
                )
                return neighbor_changes

            logging.debug(f"ncgi=0x{cs.ncgi:x} " f"pci={cs.pci} " f"tracking new {cs}")

            return CellChanges(
                ncgi=cs.ncgi,
                is_update=False,
                cell_to_register=cs,
            )
        finally:
            if cs.ncgi in self.ncgi_cells_map.keys():
                cs.lat = self.ncgi_cells_map[cs.ncgi].lat
                cs.lng = self.ncgi_cells_map[cs.ncgi].lng
                cs.azimuth = self.ncgi_cells_map[cs.ncgi].azimuth
                cs.tilt = self.ncgi_cells_map[cs.ncgi].tilt
                cs.arc_width = self.ncgi_cells_map[cs.ncgi].arc_width
                cs.height = self.ncgi_cells_map[cs.ncgi].height
            self.ncgi_cells_map[cs.ncgi] = cs

    def get_pci(self, ncgi: int) -> int:
        """
        returns pci given ncgi
        throws exception if ncgi had not been seen before
        """
        return self.ncgi_cells_map[ncgi].pci

    def get_cgi(self, ncgi: int) -> CellGlobalId:
        """
        returns cgi given ncgi
        throws exception if ncgi had not been seen before
        """
        return self.ncgi_cells_map[ncgi].cgi

    def get_e2_node_id(self, ncgi: int) -> str:
        """
        returns E2 node ID given ncgi of the associated cell.
        throws exception if ncgi had not been seen before:
        """
        return self.ncgi_cells_map[ncgi].e2_node_id

    def find_ncgi(self, e2_node_id: str, nci: int) -> Optional[int]:
        """
        find ncgi given e2_node_id and nci, returns None if not found

        nci is sometimes called cell id
        cell id is in the rc-pre service model as "NRCellIdentity"
        """
        nci_mask = (0x1 << CELLID_BITWIDTH) - 1
        for ncgi, state in self.ncgi_cells_map.items():
            if state.e2_node_id != e2_node_id:
                continue
            logging.info(
                f"ncgi:0x{ncgi:x}: state.nci:0x{state.nci:x} ==? nci:0x{nci:x}"
            )
            if state.nci == nci:
                return ncgi
        return None
