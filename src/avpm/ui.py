"""
Output helpers.
"""

from __future__ import annotations

import json
from collections.abc import Sequence

from avpm.models import Location


def title(version: str) -> None:
    print("=" * 42)
    print(f" AVPM {version}")
    print("=" * 42)


def info(text: str) -> None:
    print(text)


def error(text: str) -> None:
    print(f"ERROR: {text}")


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def print_locations(
    locations: Sequence[Location],
    title: str | None = None,
) -> None:
    if title:
        print(title)
        print()

    print(f"{'ISO':<4} {'Country':<22} {'City':<30} {'Ping'}")
    print("-" * 65)

    for loc in locations:
        print(
            f"{loc.iso:<4}"
            f"{loc.country:<23}"
            f"{loc.city:<31}"
            f"{loc.ping}"
        )
