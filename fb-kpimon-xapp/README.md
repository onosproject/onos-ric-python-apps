# fb-kpimon-xapp
key performance indicator app

This app subscribes to the kpm (key performance metrics) service model and exposes
the metrics via a prometheus gauge endpoint.

## Build image

From the root directory of this repo, run:
```
make image/fb-kpimon-xapp
```

## Deploy container

By convention, helm charts are stored in the sdran-helm-chart repository.

from the root directory of sdran-helm-chart repository, deploy to kubernetes:
```
helm install -n micro-onos \
    --set image.repository=localhost/fb-kpimon-xapp \
    --set image.tag=latest \
    fb-kpimon-xapp ./fb-kpimon-xapp
```

uninstall:
```
helm uninstall -n micro-onos fb-kpimon-xapp
```

view logs:
```
kubectl logs --namespace=micro-onos --tail=100 -lname=fb-kpimon-xapp -f
```
