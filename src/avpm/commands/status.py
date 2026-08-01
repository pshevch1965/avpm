from __future__ import annotations

from avpm.drivers.adguard import AdGuardDriver


def run(args) -> int:
    try:
        status = AdGuardDriver.status()
    except FileNotFoundError:
        print("AdGuard VPN CLI not found.")
        return 1

    print(status.raw)

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "status",
        help="Show VPN status",
    )

    parser.set_defaults(func=run)