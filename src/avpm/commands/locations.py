from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend
from avpm.uint.table import print_locations


def run(args) -> int:
    backend = AdGuardBackend()

    locations = backend.locations()

    print_locations(locations)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "locations",
        help="List VPN locations",
    )

    parser.set_defaults(func=run)