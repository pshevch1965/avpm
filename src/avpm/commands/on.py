from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()
    backend.connect(args.location)

    print("VPN connected.")

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "on",
        help="Connect VPN",
    )

    parser.add_argument(
        "-l",
        "--location",
        help="VPN location",
    )

    parser.set_defaults(func=run)