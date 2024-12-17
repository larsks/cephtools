# Ceph tools for ODF

This repository will deploy a `cephtools` pod in which the credentials from the `external_cluster_details` secret have been extracted into appropriate configuration files in `/etc/ceph`. This makes it easy to run diagnostic commands.

The `cephtools` directory deploys an unprivileged container:

```
kubectl apply -k cephtools
```

The `cephtools-privileged` directory deploys a privileged container (and adds the necessary ClusterRoleBinding to grant access to the `privileged` scc):

```
kubectl apply -k cephtools-privileged
```

In general you will not need the privileged version.

NB: You may need to update the `image` in `cephtools/deployment.yaml` to account for different versions of ODF. At the time of this writing, the Deployment uses the `v4.17` image.
