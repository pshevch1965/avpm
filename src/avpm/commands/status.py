from __future__ import annotations

from argparse import Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        status = backend.status()
    except BackendError:
        if args.quiet:
            return 1
        raise

    if args.quiet:
        return 0 if status.connected else 1

    print(status.raw)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "status",
        help="Show VPN status",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Print nothing and return connection state as exit code",
    )

    parser.set_defaults(func=run)
