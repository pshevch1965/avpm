from __future__ import annotations

import argparse
import sys

from avpm.commands.about import register as register_about
from avpm.commands.help import register as register_help
from avpm.commands.version import register as register_version
from avpm.commands.status import register as register_status
from avpm.commands.toggle import register as register_toggle
from avpm.exceptions import AvpmError
from avpm.commands.backend import register as register_backend
from avpm.commands.on import register as register_on
from avpm.commands.off import register as register_off
from avpm.commands.locations import register as register_locations
from avpm.commands.doctor import register as register_doctor
from avpm.commands.connect import register as register_connect
from avpm.commands.completion import register as register_completion
from avpm.commands.disconnect import register as register_disconnect
from avpm.commands.reconnect import register as register_reconnect
from avpm.commands.fastest import register as register_fastest
from avpm.commands.find import register as register_find
from avpm.commands.ip import register as register_ip
from avpm.commands.health import register as register_health
from avpm.commands.support import register as register_support

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vpn",
        description="AVPM - AdGuard VPN Manager",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        metavar="<command>",
    )

    register_version(subparsers)
    register_about(subparsers)
    register_help(subparsers, parser)
    register_status(subparsers)
    register_toggle(subparsers)
    register_backend(subparsers)
    register_on(subparsers)
    register_off(subparsers)
    register_locations(subparsers)
    register_doctor(subparsers)
    register_connect(subparsers)
    register_disconnect(subparsers)
    register_reconnect(subparsers)
    register_fastest(subparsers)
    register_find(subparsers)
    register_ip(subparsers)
    register_health(subparsers)
    register_support(subparsers)
    register_completion(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except AvpmError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
