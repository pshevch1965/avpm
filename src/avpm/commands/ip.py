from __future__ import annotations

from argparse import Namespace

from avpm.services.network import fetch_public_ip
from avpm.ui import print_json


def run(args: Namespace) -> int:
    address = fetch_public_ip()

    if args.json:
        print_json({"ip": address})
    else:
        print(address)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "ip",
        help="Show public IP address",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print public IP as JSON",
    )

    parser.set_defaults(func=run)
