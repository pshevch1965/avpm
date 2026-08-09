from __future__ import annotations

import re

from avpm.models import Location
from avpm.utils.text import strip_ansi


ISO_CODE = re.compile(r"^[A-Z]{2}$", re.IGNORECASE)


def parse_locations(output: str) -> list[Location]:
    """Parse the fixed-width table returned by AdGuard VPN CLI."""
    locations: list[Location] = []

    for line in strip_ansi(output).splitlines():
        line = line.rstrip()

        if not line or line.startswith("ISO"):
            continue

        if line.startswith("You can connect"):
            break

        iso = line[0:6].strip()
        country = line[6:27].strip()
        city = line[27:58].strip()
        ping_text = line[58:].strip()

        if not ISO_CODE.fullmatch(iso) or not country or not city:
            continue

        try:
            ping = int(ping_text)
        except ValueError:
            ping = None

        locations.append(
            Location(
                iso=iso.upper(),
                country=country,
                city=city,
                ping=ping,
            )
        )

    return locations


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
