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


def fastest_location(
    locations: list[Location],
) -> Location | None:
    """Return the location with the lowest known ping."""
    return next(
        (
            location
            for location in sort_by_ping(locations)
            if location.ping is not None
        ),
        None,
    )
