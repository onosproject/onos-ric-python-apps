# Copyright 2004-present Facebook. All Rights Reserved.
# SPDX-FileCopyrightText: 2019-present Open Networking Foundation <info@opennetworking.org>
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.8-slim

WORKDIR /usr/local

COPY onos_e2_sm ./onos_e2_sm
RUN pip install --upgrade pip ./onos_e2_sm --no-cache-dir

# speed up subsequent image builds by pre-dl and pre-installing pre-reqs
COPY fb-ah-xapp/setup.py ./airhop_pci/setup.py
RUN pip install ./airhop_pci --no-cache-dir

# install actual app code
COPY fb-ah-xapp ./airhop_pci
RUN pip install ./airhop_pci --no-cache-dir

ENTRYPOINT [ "python" ]

# docker build --tag fb-ah-xapp:latest -f fb-ah-xapp/Dockerfile .
