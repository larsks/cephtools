import argparse
import json
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Any

default_credentials_file = os.getenv(
    "CEPH_CREDENTIALS_FILE", "/ceph/external_cluster_details"
)

default_config_dir = os.getenv("CEPH_CONFIG_DIR", "/etc/ceph")


@dataclass
class Args:
    credentials_file: Path = Path(default_credentials_file)
    config_dir: Path = Path(default_config_dir)


def parse_args() -> Args:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--credentials-file",
        "--credentials",
        "-c",
        default=default_credentials_file,
        type=Path,
        help=f"Path to the external_cluster_details JSON file ({default_credentials_file})",
    )
    p.add_argument(
        "--config-dir",
        "-d",
        default=default_config_dir,
        type=Path,
        help=f"Directory in which to generate configuration files ({default_config_dir})",
    )
    return Args(**vars(p.parse_args()))


def write_users(creds: list[dict[str, Any]], configdir: Path):
    for item in creds:
        if item["kind"] == "Secret" and "userID" in item.get("data", {}):
            userid = item["data"]["userID"]
            userkey = item["data"]["userKey"]
            if not userid.startswith("client."):
                userid = f"client.{userid}"

            with (configdir / f"ceph.{userid}.keyring").open("w") as fd:
                fd.write(f"[{userid}]\n")
                fd.write(f"key={userkey}\n")


def write_ceph_conf(creds: list[dict[str, Any]], configdir: Path):
    mon_host = (
        next(x for x in creds if x["name"] == "rook-ceph-mon-endpoints")["data"]["data"]
        .splitlines()[0]
        .split("=", 1)[1]
    )

    with (configdir / "ceph.conf").open("w") as fd:
        fd.write("[global]\n")
        fd.write(f"mon_host={mon_host}\n")


def write_shell_vars(creds: list[dict[str, Any]], configdir: Path):
    pool = next(x for x in creds if x["name"] == "ceph-rbd")["data"]["pool"]
    provisioner = next(x for x in creds if x["name"] == "rook-csi-rbd-provisioner")[
        "data"
    ]["userID"]
    with (configdir / "ceph.env").open("w") as fd:
        fd.write(f'export CEPH_ARGS="--user {provisioner}"\n')
        fd.write(f'export RBD_POOL="{pool}"\n')


def main():
    args = parse_args()

    with open(args.credentials_file) as fd:
        creds = json.load(fd)

    write_users(creds, args.config_dir)
    write_ceph_conf(creds, args.config_dir)
    write_shell_vars(creds, args.config_dir)


if __name__ == "__main__":
    main()
