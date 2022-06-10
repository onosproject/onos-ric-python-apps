<!--
SPDX-FileCopyrightText: Copyright 2004-present Facebook. All Rights Reserved.
SPDX-FileCopyrightText: 2019-present Open Networking Foundation <info@opennetworking.org>

SPDX-License-Identifier: Apache-2.0
-->
# fb-kpimon-xapp
key performance indicator app

This app subscribes to the kpm (key performance metrics) service model and exposes
the metrics via a prometheus gauge endpoint.

## Deploy container

You can deploy the `fb-kpimon-xapp` image using helm:
```
helm repo add sdran https://sdrancharts.onosproject.org
helm install -n micro-onos fb-kpimon-xapp sdran/fb-kpimon-xapp
```

uninstall:
```
helm uninstall -n micro-onos fb-kpimon-xapp
```

view logs:
```
kubectl logs --namespace=micro-onos --tail=100 -lname=fb-kpimon-xapp -f
```
