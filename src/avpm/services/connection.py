from __future__ import annotations

from avpm.backends.base import Backend
from avpm.exceptions import BackendError
from avpm.models import Location
from avpm.services.locations import fastest_location, filter_locations


def get_fastest_location(
    backend: Backend,
    *,
    country: str | None = None,
) -> Location:
    """Return the backend location with the lowest known ping."""
    locations = filter_locations(
        backend.locations(),
        country=country,
    )
    location = fastest_location(locations)

    if location is None:
        suffix = f" for country '{country}'" if country else ""
        raise BackendError(
            f"No VPN locations with known ping found{suffix}"
        )

    return location
