FROM python:3.8-slim

WORKDIR /usr/local

COPY onos_e2_sm ./onos_e2_sm
RUN pip install --upgrade pip ./onos_e2_sm --no-cache-dir

COPY fb-ah-xapp ./airhop_pci
RUN pip install ./airhop_pci --no-cache-dir

ENTRYPOINT [ "python" ]

# docker build --tag fb-ah-xapp:latest -f fb-ah-xapp/Dockerfile .
