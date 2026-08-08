from __future__ import annotations

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()

    print(f"Backend    : AdGuard VPN CLI")
    print(f"Executable : {backend.executable}")
    print(f"Available  : {'Yes' if backend.exists() else 'No'}")

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "backend",
        help="Show backend information",
    )

    parser.set_defaults(func=run)