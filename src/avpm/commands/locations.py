from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()

    locations = backend.locations()

    for location in locations:
        print(location.country)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "locations",
        help="List VPN locations",
    )

    parser.set_defaults(func=run)