from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()

    locations = backend.locations()

    print(f"{'ISO':<5} {'Country':<22} {'City':<28} {'Ping':>5}")
    print("-" * 65)

    for location in locations:
        ping = "-" if location.ping is None else str(location.ping)

        print(
            f"{location.iso:<5}"
            f"{location.country:<22}"
            f"{location.city:<28}"
            f"{ping:>5}"
        )

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "locations",
        help="List VPN locations",
    )

    parser.set_defaults(func=run)