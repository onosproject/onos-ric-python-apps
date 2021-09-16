FROM python:3.8-slim

# install all deps
WORKDIR /usr/local
COPY fb-kpimon-xapp ./kpimon
COPY onos_e2_sm ./onos_e2_sm
RUN pip install ./kpimon ./onos_e2_sm --no-cache-dir

ENTRYPOINT [ "python" ]

# docker build --tag fb-kpimon-xapp:latest -f fb-kpimon-xapp/Dockerfile .
