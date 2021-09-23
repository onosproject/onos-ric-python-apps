airhop_pci is the adapter xApp that enables the Airhop eSON service to
monitor and control RANs via RIC platforms using a RIC SDK.

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
