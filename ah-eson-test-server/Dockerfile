# SPDX-FileCopyrightText: Copyright 2020-present Facebook. All Rights Reserved.
#
# SPDX-License-Identifier: MIT

FROM python:3.8-slim

WORKDIR /code

RUN pip install --upgrade pip grpcio 'protobuf<4' --no-cache-dir

COPY ah-eson-test-server .

RUN chmod +x server.py

# run
CMD [ "./server.py" ]

# docker build --tag ah-eson-test-server:latest -f ah-eson-test-server/Dockerfile .
