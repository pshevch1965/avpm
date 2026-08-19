from __future__ import annotations

from argparse import Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.commands.connect import clean_connect_output


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    if backend.status().connected:
        backend.disconnect()
        print("VPN disconnected.")
        return 0

    output = backend.connect()
    print(clean_connect_output(output))
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "toggle",
        help="Toggle VPN connection",
    )

    parser.set_defaults(func=run)
