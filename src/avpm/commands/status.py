from __future__ import annotations

from argparse import Namespace
from dataclasses import asdict

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError
from avpm.ui import print_json


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        status = backend.status()
    except BackendError as exc:
        if args.quiet:
            return 1

        if args.json:
            print_json(
                {
                    "connected": False,
                    "location": None,
                    "error": str(exc),
                }
            )
            return 1

        raise

    if args.quiet:
        return 0 if status.connected else 1

    if args.json:
        print_json(asdict(status))
        return 0

    print(status.raw)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "status",
        help="Show VPN status",
    )

    output_group = parser.add_mutually_exclusive_group()

    output_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Print nothing and return connection state as exit code",
    )

    output_group.add_argument(
        "--json",
        action="store_true",
        help="Print status as JSON",
    )

    parser.set_defaults(func=run)
