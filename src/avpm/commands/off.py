from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()
    backend.disconnect()

    print("VPN disconnected.")

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "off",
        help="Disconnect VPN",
    )

    parser.set_defaults(func=run)