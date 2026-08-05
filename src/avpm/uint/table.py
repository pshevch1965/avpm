from __future__ import annotations

from collections.abc import Sequence
from avpm.models import Location


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