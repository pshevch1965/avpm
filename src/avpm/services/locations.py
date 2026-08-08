from __future__ import annotations

from avpm.models import Location


def filter_locations(
    locations: list[Location],
    *,
    country: str | None = None,
    max_ping: int | None = None,
) -> list[Location]:
    """Filter locations by country name/ISO code and maximum ping."""
    country_key = country.casefold() if country else None

    return [
        location
        for location in locations
        if (
            country_key is None
            or location.iso.casefold() == country_key
            or location.country.casefold() == country_key
        )
        and (
            max_ping is None
            or (
                location.ping is not None
                and location.ping <= max_ping
            )
        )
    ]


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
