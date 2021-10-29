# fb-ah-xapp

This app is the adapter xApp that enables the Airhop eSON service to
monitor and control RANs via RIC platforms using a RIC SDK.

This app is an adapter to Airhop's eSON service, covering physical cell identifier
(PCI) confict resolution, and mobility load balancing (MLB).

This app uses the ONF Python SDK.

## Functionality

An E2 subscription to the rc-pre service model is made. Cell information such as PCI
and neighbor information is received pushed to the Airhop eSON service.

PCI information of the cell and its neighbors are used by the eSON PCI conflict algorithm.

Cell individual offset of the cell and its neighbors are used by the eSON MLB algorithm.

An E2 subscription to the KPM service model is also made. The cell capacity information
is sent to the eSON service and used by the MLB algorithm.

The app listens to changes from the eSON service. PCI change requests are issued
via the eSON's conflict resolution algorithm, neighbor cell individual offset
change requests are issued by eSON's MLB algorithm. When a change request is received,
the app will issue an E2 control message to the expected E2 node.

This all also responds to http requests to view or modify the cell information.


## Usage

Since the Airhop eSON service is a commercial product, it is not included in this
package, instead a test server is included that mimics messages that could be sent
from the eSON service. The messages do not perform the PCI conflict and MLB algorithms,
but will send arbitrary PCI change requests and cell individual offset change requests
to exercise the E2 control pathways. This test server is called `ah-eson-test-server`
and is included in this repository.


# Basic Usage

```
usage: main.py [-h] [--ca-path CA_PATH] [--key-path KEY_PATH]
               [--cert-path CERT_PATH] [--e2t-endpoint E2T_ENDPOINT]
               [--e2sub-endpoint E2SUB_ENDPOINT]
               [--eson-endpoint ESON_ENDPOINT] [--grpc-port GRPC_PORT]
               [--pci-subscribe-delay PCI_SUBSCRIBE_DELAY | --pci-maintenance-delay PCI_MAINTENANCE_DELAY]
               [--pci-maintenance-period PCI_MAINTENANCE_PERIOD]

Airhop PCI xApp.

optional arguments:
  -h, --help            show this help message and exit
  --ca-path CA_PATH     path to CA certificate
  --key-path KEY_PATH   path to client private key
  --cert-path CERT_PATH
                        path to client certificate
  --e2t-endpoint E2T_ENDPOINT
                        E2T service endpoint
  --e2sub-endpoint E2SUB_ENDPOINT
                        E2Sub service endpoint
  --eson-endpoint ESON_ENDPOINT
                        Airhop eson service endpoint
  --grpc-port GRPC_PORT
                        grpc Port number
  --pci-subscribe-delay PCI_SUBSCRIBE_DELAY, -s PCI_SUBSCRIBE_DELAY
                        Initial delay (s) before PCI conflict resolution
                        changes subscription, if not specified does not
                        subscribe.
  --pci-maintenance-delay PCI_MAINTENANCE_DELAY, -m PCI_MAINTENANCE_DELAY
                        Initial delay (s) before monitoring proposed PCI
                        conflict resolution changes, if not specified do not
                        monitor.
  --pci-maintenance-period PCI_MAINTENANCE_PERIOD
                        Period (s) for monitoring proposed PCI conflict
                        resolution changes, only used if --pci-maintenance-
                        delay is specified. Default=30
```

## Parameters to specify connection to the ric

RIC endpoints: `--e2t-endpoint "hostname:port"`, `--e2sub-endpoint "hostname:port"`

SSL client certificate params: `--ca-path <filename>` `--key-path <filename>` -`-cert-path <filename>`

## Parameter to specify connection to the eSON service

`--eson-endpoint hostname:port`

## Parameters to specify options for the PCI algorithm

There are multiple ways to run the PCI conflict resolution algorithm.
* "subscribe" to a stream of changes
  * Conflict subscription will stream conflict resolution updates as the eSON gets new information.
  * Enable this method by specifying `--pci-subscribe-delay`, which sets the
    delay time to begin receiving conflict resolution changes
* "maintenance" window oneshot
  * This method will request eSON to detect and resolve all conflicts at once.
  * Enable this method by specifying `--pci-maintenance-delay`, which sets the
    delay time to query all changes.
  * Use `--pci-maintenance-period` to specify the time it will wait before another
    resolution request is sent to the eSON service.


## Examples

(These examples assume that the surrogate server is running on port 50051 of the same machine.)


Only monitor cell messages from E2 node

```
python3 main.py \
    --e2t-endpoint "localhost:50051" \
    --e2sub-endpoint "localhost:50051" \
    --eson-endpoint "localhost:50051"
```

Monitor cell messages AND resolve PCI conflicts via subscription method

```
python3 main.py \
    --e2t-endpoint "localhost:50051" \
    --e2sub-endpoint "localhost:50051" \
    --eson-endpoint "localhost:50051" \
    --pci-subscribe-delay 0
```

Monitor cell messages AND resolve PCI conflicts via subscription method 30 seconds after start

```
python3 main.py \
    --e2t-endpoint "localhost:50051" \
    --e2sub-endpoint "localhost:50051" \
    --eson-endpoint "localhost:50051" \
    --pci-subscribe-delay 30
```

Monitor cell messages and resolve PCI conflicts via maintenance window 30 seconds after start, and repeat every 5 minutes

```
python3 main.py \
    --e2t-endpoint "localhost:50051" \
    --e2sub-endpoint "localhost:50051" \
    --eson-endpoint "localhost:50051" \
    --pci-maintenance-delay 30 \
    --pci-maintenance-period 300
```
