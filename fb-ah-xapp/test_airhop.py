#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import asyncio
import logging

from airhop_pci.airhop_api.com.airhopcomm.eson.nr.registration.v1 import (
    RegisterResponse,
    RegistrationServiceStub,
    UnregisterResponse,
)
from airhop_pci.airhop_api.com.airhopcomm.eson.nr.v1 import (
    Cell,
    CellSize,
    CellSpecificOffsets,
    Neighbor,
    NeighborList,
    PciPool,
    PciRange,
)

from airhop_pci.airhop import AirhopEsonClient


async def test_register(ah: AirhopEsonClient) -> None:
    logging.info("test_register()")
    await ah.register(
        cells=[
            Cell(
                ncgi=1,
                cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                dl_nrarfcn=5,
                ul_nrarfcn=5,
                pci=1,
                pci_pool=PciPool(
                    [
                        PciRange(lower_pci=1, upper_pci=10),
                        PciRange(lower_pci=20, upper_pci=30),
                    ]
                ),
                neighbors=NeighborList(
                    [
                        Neighbor(
                            ncgi=2,
                            cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                            dl_nrarfcn=1,
                            ul_nrarfcn=1,
                            pci=1,
                        ),
                        Neighbor(
                            ncgi=3,
                            cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                            dl_nrarfcn=1,
                            ul_nrarfcn=1,
                            pci=1,
                        ),
                    ]
                ),
                vendor_info="vendor_info",
                capacity_class_value=100,
                cell_specific_offsets=CellSpecificOffsets(
                    cio=12, offset_freq=12, q_offset=12
                ),
            ),
            Cell(
                ncgi=2,
                cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                dl_nrarfcn=5,
                ul_nrarfcn=5,
                pci=1,
                pci_pool=PciPool(
                    [
                        PciRange(lower_pci=1, upper_pci=10),
                        PciRange(lower_pci=20, upper_pci=30),
                    ]
                ),
                neighbors=NeighborList(
                    [
                        Neighbor(
                            ncgi=2,
                            cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                            dl_nrarfcn=1,
                            ul_nrarfcn=1,
                            pci=1,
                        ),
                        Neighbor(
                            ncgi=3,
                            cell_size=CellSize.CELL_SIZE_ENTERPRISE,
                            dl_nrarfcn=1,
                            ul_nrarfcn=1,
                            pci=1,
                        ),
                    ]
                ),
                vendor_info="vendor_info",
                capacity_class_value=100,
                cell_specific_offsets=CellSpecificOffsets(
                    cio=12, offset_freq=12, q_offset=12
                ),
            ),
        ],
    )


async def test_unregister(ah: AirhopEsonClient) -> None:
    logging.info("test_unregister()")
    await ah.unregister(12)


async def test_mlb_subscribe(ah: AirhopEsonClient) -> None:
    logging.info("test_mlb_subscribe()")

    async for change_request in ah.mlb_subscribe():
        logging.info(change_request)
        await ah.mlb_confirm_change(
            ncgi=change_request.ncgi,
            neighbor_ncgi=change_request.neighbor_ncgi,
            cio=change_request.cio,
            q_offset=change_request.q_offset,
        )


async def mlb_report_capacity(ah: AirhopEsonClient) -> None:
    logging.info("mlb_report_capacity()")
    await ah.mlb_report_capacity(ncgi=1234, capacity_value=123)


async def test() -> None:
    logging.info("test()")
    with AirhopEsonClient("localhost:50051") as ah:
        await test_register(ah)
        await test_unregister(ah)
        await test_mlb_subscribe(ah)
        await mlb_report_capacity(ah)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    asyncio.run(test())
