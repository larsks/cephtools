# Ceph tools for ODF

This repository will deploy a `cephtools` pod in which the credentials from the `external_cluster_details` secret have been extracted into appropriate configuration files in `/etc/ceph`. This makes it easy to run diagnostic commands.

## Deploy

The `cephtools` directory deploys an unprivileged container:

```
kubectl apply -k cephtools
```

The `cephtools-privileged` directory deploys a privileged container (and adds the necessary ClusterRoleBinding to grant access to the `privileged` scc):

```
kubectl apply -k cephtools-privileged
```

In general you will not need the privileged version.

### Remote deployment

Instead of cloning this repository and deploying from local directories, you can deploy directly from the github repository:

```
kubectl apply -k https://github.com/larsks/cephtools//cephtools
```

## Access

To access the container:

```
k exec -it deploy/cephtools -- bash
```

You will find yourself in the `/etc/ceph` directory. Source the `ceph.env` file:

```
. ceph.env
```

Now you should be able to run `ceph` commands:

```
bash-5.2$ ceph health
HEALTH_WARN 10 large omap objects
```

Or `rbd` commands:

```
bash-5.2$ rbd ls $RBD_POOL
csi-vol-633451f6-1f4f-4320-aa3f-7ab4cbcbb79b
csi-vol-93dc578f-ad58-4666-a1a7-546e5ee5b6f6
csi-vol-99a6995b-1b15-4116-b5e0-e674016552d5
csi-vol-b9db3957-7b07-4404-a602-c9f9cb2a57af
csi-vol-d0cc6e97-086d-4a04-bf03-b5bf1b480924
csi-vol-fbd8ae27-808e-48a9-81ca-9c9af4352c62
```
