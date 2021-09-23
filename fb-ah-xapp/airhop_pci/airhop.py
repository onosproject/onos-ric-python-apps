#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

from typing import Dict, List, Iterator, Optional, Tuple, Type
from types import TracebackType

import asyncio
import logging

from grpclib.client import Channel, Configuration
from betterproto.grpc.util.async_channel import AsyncChannel

from .airhop_api.com.airhopcomm.eson.nr.registration.v1 import (
    AddNeighborResponse,
    RegisterResponse,
    RegistrationServiceStub,
    RemoveNeighborResponse,
    UnregisterResponse,
)
from .airhop_api.com.airhopcomm.eson.nr.pci.v1 import (
    PciServiceStub,
    ChangeRequest,
    ConfirmChangeResponse,
    DetectAndResolveResponse,
    Message,
    RejectChangeResponse,
    RetrieveProposedChangesResponse,
)

from .airhop_api.com.airhopcomm.eson.nr.v1 import (
    Cell,
    CellSize,
    Neighbor,
)

from .airhop_api.com.airhopcomm.eson.nr.mlb.v1 import (
    ChangeRequest as MlbChangeRequest,
    ConfirmChangeResponse as MlbConfirmChangeResponse,
    MlbServiceStub,
    ReportCapacityResponse,
)


def make_neighbor(ncgi: int, pci: int, fcn: int) -> Neighbor:
    return Neighbor(
        ncgi=ncgi,
        cell_size=CellSize.CELL_SIZE_OUTDOOR_SMALL,
        dl_nrarfcn=fcn,
        ul_nrarfcn=fcn,
        pci=pci,
    )


class AirhopEsonClient:
    """
    wrappers to airhop eson api

    Usage:
        with AirhopEsonClient(args.eson_endpoint) as client:
            client.register()
    """

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.channel: Optional[Channel] = None
        self.reg_client: Optional[RegistrationServiceStub] = None
        self.pci_client: Optional[PciServiceStub] = None
        self.mlb_client: Optional[MlbServiceStub] = None

    def __enter__(self) -> "AirhopEsonClient":
        host, port = self.endpoint.rsplit(":", 1)
        logging.debug(f"Attempting to connect to {host} {port}")
        self.channel = Channel(
            host,
            port,
            config=Configuration(
                _keepalive_time=15,  # seconds
                _keepalive_permit_without_calls=True,
                _http2_max_pings_without_data=0,
            ),
        )
        self.reg_client = RegistrationServiceStub(self.channel)
        self.pci_client = PciServiceStub(self.channel)
        self.mlb_client = MlbServiceStub(self.channel)
        return self

    def __exit__(
        self,
        _exception_type: Optional[Type[BaseException]],
        _exception_value: Optional[BaseException],
        _traceback: Optional[TracebackType],
    ) -> bool:
        if self.channel is None:
            raise Exception("Client is uninitialized")
        self.channel.close()
        self.channel = None
        self.reg_client = None
        self.pci_client = None
        self.mlb_client = None

    async def register(self, cells: List[Cell]) -> List[RegisterResponse]:
        """
        register a set of cells
        """
        cells_stream = AsyncChannel()
        await cells_stream.send_from(
            cells,
            close=True,
        )

        responses = []
        async for register_r in self.reg_client.register(cells_stream):
            logging.debug(register_r)
            responses.append(register_r)

        return responses

    async def unregister(self, ncgi: int) -> None:
        """
        unregister a cell
        """
        unregister_r: UnregisterResponse = await self.reg_client.unregister(ncgi=ncgi)
        logging.debug(unregister_r)

    async def add_neighbor(
        self, ncgi: int, neighbor_ncgi_pci_map: Dict[int, Tuple[int, int]]
    ) -> None:
        """
        add neighbors
        """
        n = [
            make_neighbor(n_ncgi, n_pci, n_fcn)
            for n_ncgi, (n_pci, n_fcn) in sorted(neighbor_ncgi_pci_map.items())
        ]
        r: AddNeighborResponse = await self.reg_client.add_neighbor(
            ncgi=ncgi, neighbors=n
        )
        logging.debug(r)

    async def remove_neighbor(self, ncgi: int, neighbor_ncgis: List[int]) -> None:
        """
        remove neighbors
        """
        r: RemoveNeighborResponse = await self.reg_client.remove_neighbor(
            ncgi=ncgi, neighbor_ncgis=neighbor_ncgis
        )
        logging.debug(r)

    async def pci_subscribe(self) -> Iterator[ChangeRequest]:
        """
        subscribe to pci conflicts
        """
        async for message in self.pci_client.subscribe():
            change_request: ChangeRequest = message.change_req
            logging.debug(change_request)
            yield change_request

    async def pci_detect_and_resolve(self) -> None:
        r: DetectAndResolveResponse = await self.pci_client.detect_and_resolve()
        logging.debug(r)

    async def pci_confirm_change(self, ncgi: int, pci: int) -> None:
        r: ConfirmChangeResponse = await self.pci_client.confirm_change(
            ncgi=ncgi, pci=pci
        )
        logging.debug(r)

    async def pci_reject_change(self, ncgi: int, pci: int) -> None:
        r: RejectChangeResponse = await self.pci_client.reject_change(
            ncgi=ncgi, pci=pci
        )
        logging.debug(r)

    async def pci_get_proposed_changes(self) -> List[ChangeRequest]:
        r: RetrieveProposedChangesResponse = (
            await self.pci_client.retrieve_proposed_changes()
        )
        logging.debug(f"len(RetrieveProposedChangesResponse)={len(r.change_reqs)}")
        return r.change_reqs

    async def mlb_subscribe(self) -> Iterator[MlbChangeRequest]:
        """
        subscribe to mlb actions
        """
        async for message in self.mlb_client.subscribe():
            change_request: MlbChangeRequest = message.change_req
            logging.debug(change_request)
            yield change_request

    async def mlb_report_capacity(self, ncgi: int, capacity_value: int) -> None:
        r: ReportCapacityResponse = await self.mlb_client.report_capacity(
            ncgi=ncgi,
            capacity_value=capacity_value,
        )
        logging.debug(r)

    async def mlb_confirm_change(
        self,
        ncgi: int,
        neighbor_ncgi: int,
        cio: Optional[int] = None,
        q_offset: Optional[int] = None,
    ) -> None:
        r: MlbConfirmChangeResponse = await self.mlb_client.confirm_change(
            ncgi=ncgi,
            neighbor_ncgi=neighbor_ncgi,
            cio=cio,
            q_offset=q_offset,
        )
        logging.debug(r)
