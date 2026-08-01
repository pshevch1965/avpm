from __future__ import annotations

import platform

from avpm import __version__


def run(args) -> int:
    print("AVPM")
    print("AdGuard VPN Manager")
    print()
    print(f"Version : {__version__}")
    print(f"Python  : {platform.python_version()}")
    print(f"System  : {platform.system()}")

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "about",
        help="About AVPM",
    )

    parser.set_defaults(func=run)