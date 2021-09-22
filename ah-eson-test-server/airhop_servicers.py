#!/usr/bin/env python3

#
# Copyright (c) 2020-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from typing import Dict, Optional, Tuple

import logging
import random
import time

from google.protobuf.wrappers_pb2 import StringValue, UInt32Value
from grpc._server import _Server

from airhop_api_pb2 import (
    nr_pb2,
    nr_mlb_pb2,
    nr_mlb_pb2_grpc,
    nr_pci_pb2,
    nr_pci_pb2_grpc,
    nr_registration_pb2,
    nr_registration_pb2_grpc,
)


class AHEmulator:
    """
    track ncgi and pci such that the service can return realistically fake
      change requests
    """

    ncgi_pci_map: Dict[int, int] = {}

    @classmethod
    def register(cls, ncgi: int, pci: int) -> None:
        cls.ncgi_pci_map[ncgi] = pci

    @classmethod
    def unregister(cls, ncgi: int) -> None:
        if ncgi in cls.ncgi_pci_map:
            del cls.ncgi_pci_map[ncgi]

    @classmethod
    def get_random_ncgi_pci(cls) -> Optional[Tuple[int, int]]:
        if len(cls.ncgi_pci_map) == 0:
            return None
        return random.choice(list(cls.ncgi_pci_map.items()))

    @classmethod
    def get_random_ncgi_pair(cls) -> Optional[Tuple[int, int]]:
        if len(cls.ncgi_pci_map) <= 1:
            return None

        ncgi1 = random.choice(list(cls.ncgi_pci_map.keys()))
        ncgi2 = ncgi1
        while ncgi2 == ncgi1:
            ncgi2 = random.choice(list(cls.ncgi_pci_map.keys()))
        return ncgi1, ncgi2


class RegistrationServiceServicer(nr_registration_pb2_grpc.RegistrationServiceServicer):
    """
    test framework
    """

    def __init__(self):
        logging.info("nr_registration_pb2_grpc.RegistrationServiceServicer started")

    def Register(self, request_iterator, context):
        # log request
        for r in request_iterator:
            logging.info(f"### Register ncgi={r.ncgi}")
            request: nr_pb2.Cell = r
            logging.debug(f"Register request:\n{request}")

            AHEmulator.register(request.ncgi, request.pci)

            resp = nr_registration_pb2.RegisterResponse(
                ncgi=request.ncgi,
                error_msg=StringValue(value=f"error_msg for {request.ncgi}"),
            )
            logging.debug(f"Register response:\n{resp}")
            yield resp

    def Unregister(self, request, context):
        logging.info(f"### Unregister ncgi={request.ncgi}")
        logging.debug(f"Unregister request:\n{request}")
        return nr_registration_pb2.UnregisterResponse()

    def AddNeighbor(self, request, context):
        logging.info(f"### AddNeighbor ncgi={request.ncgi}")
        logging.debug(f"AddNeighbor request:\n{request}")
        return nr_registration_pb2.AddNeighborResponse()

    def RemoveNeighbor(self, request, context):
        logging.info(f"### RemoveNeighbor ncgi={request.ncgi}")
        logging.debug(f"RemoveNeighbor request:\n{request}")
        return nr_registration_pb2.RemoveNeighborResponse()


class PciServiceServicer(nr_pci_pb2_grpc.PciServiceServicer):
    """
    pci servicer
    """

    def __init__(self):
        logging.info("nr_pci_pb2_grpc.PciServiceServicer started")

    def _gen_random_change_request(self) -> Optional[nr_pci_pb2.ChangeRequest]:
        ncgi_pci = AHEmulator.get_random_ncgi_pci()
        if ncgi_pci is None:
            return None
        ncgi, pci = ncgi_pci
        new_pci = random.randint(1, 200)
        while new_pci == pci:
            new_pci = random.randint(1, 200)
        return nr_pci_pb2.ChangeRequest(
            ncgi=ncgi, pci=new_pci, conflict=nr_pci_pb2.CONFLICT_DIRECT_COLLISION
        )

    def Subscribe(self, request, context):
        """Subscribe to the PciService in order to listen for the PCI
        algorithm messages for a set of ncgis. Any future PCI change
        will be streamed back through this RPC.
        """
        logging.info(f"### Subscribe")
        logging.debug(f"Subscribe request:\n{request}")
        for _ in range(10):
            change_request = self._gen_random_change_request()
            if change_request is not None:
                resp = nr_pci_pb2.Message(change_req=change_request)
                logging.debug(f"Subscribe response:\n{resp}")
                yield resp
            time.sleep(3)

    def DetectAndResolve(self, request, context):
        """Trigger PCI algorithm to detect and resolve PCI conflict. If a
        conflict is detected and a better PCI is found, the new PCI is
        streamed back through the Subscribe RPC.
        """
        logging.info(f"### DetectAndResolve")
        logging.debug(f"DetectAndResolve request:\n{request}")
        return nr_pci_pb2.DetectAndResolveResponse()

    def ConfirmChange(self, request, context):
        """Confirm a PCI change request has been applied. eSON updates its
        internal PCI to reflect the change.
        """
        logging.info(f"### ConfirmChange ncgi={request.ncgi} pci={request.pci}")
        logging.debug(f"ConfirmChange request:\n{request}")
        return nr_pci_pb2.ConfirmChangeResponse()

    def RejectChange(self, request, context):
        """Reject a PCI change request if the proposed PCI fails to be
        applied.
        """
        logging.info(f"### RejectChange ncgi={request.ncgi} pci={request.pci}")
        logging.debug(f"RejectChange request:\n{request}")
        return nr_pci_pb2.RejectChangeResponse()

    def RetrieveProposedChanges(self, request, context):
        """Retrieve a list of proposed PCI changes. The client shall use
        the ConfirmChange or RejectChange later to update the eSON
        server whether the proposed changes are applied. This RPC may
        take several minutes (the current default is 5 minutes) to
        complete.
        """
        logging.info(f"### RetrieveProposedChanges")
        logging.debug(f"RetrieveProposedChanges request:\n{request}")
        change_reqs = []
        for _ in range(random.randint(4, 10)):
            change_request = self._gen_random_change_request()
            if change_request is not None:
                change_reqs.append(change_request)

        resp = nr_pci_pb2.RetrieveProposedChangesResponse(change_reqs=change_reqs)
        logging.debug(f"RetrieveProposedChanges response:\n{resp}")
        return resp


class MlbServiceServicer(nr_mlb_pb2_grpc.MlbServiceServicer):
    """If there are multiple clients that subscribe to cell specific
    offsets changes, one and only one shall confirm the change.
    """

    def __init__(self):
        logging.info("nr_mlb_pb2_grpc.MlbServiceServicer started")

    def _gen_random_change_request(self) -> Optional[nr_mlb_pb2.ChangeRequest]:
        ncgi_ncgi = AHEmulator.get_random_ncgi_pair()
        if ncgi_ncgi is None:
            return None
        ncgi, neighbor_ncgi = ncgi_ncgi

        # cio/qoffset enum values:
        # Q-OffsetRange ::=                   ENUMERATED {
        #     dB-24, dB-22, dB-20, dB-18, dB-16, dB-14,
        #     dB-12, dB-10, dB-8, dB-6, dB-5, dB-4, dB-3,
        #     dB-2, dB-1, dB0, dB1, dB2, dB3, dB4, dB5,
        #     dB6, dB8, dB10, dB12, dB14, dB16, dB18,
        #     dB20, dB22, dB24}

        cio = random.randint(0, 30)
        q_offset = random.randint(0, 30)

        return nr_mlb_pb2.ChangeRequest(
            ncgi=ncgi,
            neighbor_ncgi=neighbor_ncgi,
            cio=UInt32Value(value=cio),
            q_offset=UInt32Value(value=q_offset),
        )

    def Subscribe(self, request, context):
        """Subscribe to the MlbService for MLB algorithm messages. Any
        future neighbor cell specific offsets change will be streamed
        back through this RPC.
        """
        logging.info(f"### Mlb Subscribe")
        logging.debug(f"Mlb Subscribe request:\n{request}")
        for _ in range(10):
            change_request = self._gen_random_change_request()
            if change_request is not None:
                resp = nr_mlb_pb2.Message(change_req=change_request)
                logging.debug(f"Mlb Subscribe response:\n{resp}")
                yield resp
            time.sleep(3)

    def ReportCapacity(self, request, context):
        """Report cell capacity periodically. The recommended period is 10
        seconds.
        """
        logging.info(
            "### Mlb ReportCapacity "
            f"ncgi={request.ncgi} "
            f"capacity_value={request.capacity_value} "
        )
        logging.debug(f"Mlb ReportCapacity request:\n{request}")
        return nr_mlb_pb2.ReportCapacityResponse()

    def ConfirmChange(self, request, context):
        """Confirm a neighbor cell individual offsets change request has
        been applied. eSON updates internally to reflect the change.
        """
        logging.info(
            "### Mlb ConfirmChange "
            f"ncgi={request.ncgi} "
            f"neighbor_ncgi={request.neighbor_ncgi} "
            f"cio={request.cio.value} "
            f"q_offset={request.q_offset.value} "
        )
        logging.debug(f"Mlb ConfirmChange request:\n{request}")
        return nr_mlb_pb2.ConfirmChangeResponse()


def add_servicers(server: _Server):
    nr_registration_pb2_grpc.add_RegistrationServiceServicer_to_server(
        RegistrationServiceServicer(), server
    )
    nr_pci_pb2_grpc.add_PciServiceServicer_to_server(PciServiceServicer(), server)
    nr_mlb_pb2_grpc.add_MlbServiceServicer_to_server(MlbServiceServicer(), server)
