from __future__ import annotations

from avpm.models import Location


def sort_by_ping(
    locations: list[Location],
) -> list[Location]:
    """Return locations sorted by ping, with unknown values last."""
    return sorted(
        locations,
        key=lambda location: (
            location.ping is None,
            location.ping if location.ping is not None else 0,
        ),
    )
