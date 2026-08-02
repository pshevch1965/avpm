from __future__ import annotations

import platform
import shutil
import sys

from avpm.backends.adguard import AdGuardBackend


def run(args) -> int:
    backend = AdGuardBackend()

    checks = []

    # Python
    checks.append(
        (
            "Python",
            f"OK ({sys.version.split()[0]})",
        )
    )

    # System
    checks.append(
        (
            "System",
            platform.system(),
        )
    )

    # Backend
    if backend.exists():
        checks.append(
            (
                "AdGuard CLI",
                "OK",
            )
        )
    else:
        checks.append(
            (
                "AdGuard CLI",
                "NOT FOUND",
            )
        )

    # Executable path
    path = shutil.which(backend.executable)

    checks.append(
        (
            "Executable",
            path or "-",
        )
    )

    print("AVPM Diagnostics")
    print()

    for name, value in checks:
        print(f"{name:<15}: {value}")

    print()

    if backend.exists():
        print("Result          : System ready")
        return 0

    print("Result          : Problems detected")
    return 1


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "doctor",
        help="Run diagnostics",
    )

    parser.set_defaults(func=run)