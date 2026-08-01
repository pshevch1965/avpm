from __future__ import annotations

import argparse
import sys

from avpm.commands.about import register as register_about
from avpm.commands.help import register as register_help
from avpm.commands.version import register as register_version
from avpm.commands.status import register as register_status


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
    register_help(subparsers)
    register_status(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())