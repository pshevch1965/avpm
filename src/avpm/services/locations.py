from __future__ import annotations

from avpm.models import Location


def sort_by_ping(
    locations: list[Location],
) -> list[Location]:
    """Return locations sorted by ping."""
    return sorted(
        locations,
        key=lambda location: location.ping,
    )