#!/usr/bin/env python3

#
# Copyright (c) 2020-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# SPDX-FileCopyrightText: Copyright 2020-present Facebook. All Rights Reserved.
#
# SPDX-License-Identifier: MIT

from typing import Dict, Any

import argparse
import grpc
import logging
from concurrent import futures

import airhop_servicers


def serve(port: str) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    airhop_servicers.add_servicers(server)

    # start
    server.add_insecure_port(port)
    server.start()
    logging.info(f"server started on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--port",
        type=str,
        help="Listening port.",
        default="[::]:50051",
    )
    parser.add_argument(
        "--service_hostname",
        type=str,
        help="Used for GetTermination()",
        default="localhost",
    )
    parser.add_argument(
        "--service_port",
        type=int,
        help="Used for GetTermination()",
        default=50051,
    )
    parser.add_argument(
        "--mutate_nth_neighbor",
        type=int,
        help="Used to mutate neighbor of nth cell reported",
    )
    parser.add_argument(
        "--random_control_fail_percent",
        type=int,
        help="Percentage of E2 control messages that return failure.",
        default=0,
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    serve(args.port)
