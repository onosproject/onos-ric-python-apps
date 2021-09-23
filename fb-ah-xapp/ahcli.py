#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import argparse
import asyncio
import logging

from airhop_pci.airhop import AirhopEsonClient


async def async_main(args: argparse.Namespace) -> None:
    with AirhopEsonClient(args.endpoint) as ah:
        if args.unregister:
            coros = []
            for ncgi in range(args.unregister[0], args.unregister[1] + 1):
                logging.info(f"{args.endpoint} :: Unregistering ncgi={ncgi}")
                coros.append(ah.unregister(ncgi))
            await asyncio.gather(*coros)

        if args.unregisterhex:
            coros = []
            for ncgi_hex in args.unregisterhex:
                ncgi = int(ncgi_hex, 16)
                logging.info(f"{args.endpoint} :: Unregistering ncgi={ncgi} 0x{ncgi:x}")
                coros.append(ah.unregister(ncgi))
            await asyncio.gather(*coros)

        if args.detect:
            await ah.pci_detect_and_resolve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Airhop PCI utility.")
    parser.add_argument(
        "--endpoint",
        type=str,
        default="localhost:50051",
        help="Airhop eson service endpoint. Default=%(default)s",
    )
    parser.add_argument(
        "--unregister",
        nargs=2,
        type=int,
        metavar=("start_ncgi", "end_ncgi"),
        help="Unregister ncgi start and end.",
    )
    parser.add_argument(
        "--unregisterhex",
        type=str,
        nargs="+",
        help="Unregister ncgi in hex",
    )
    parser.add_argument(
        "--detect",
        action="store_true",
        help="detect conflicts",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    asyncio.run(async_main(args))
