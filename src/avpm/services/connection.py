from __future__ import annotations

from avpm.backends.base import Backend
from avpm.exceptions import BackendError
from avpm.models import Location
from avpm.services.locations import fastest_location


def get_fastest_location(backend: Backend) -> Location:
    """Return the backend location with the lowest known ping."""
    location = fastest_location(backend.locations())

    if location is None:
        raise BackendError("No VPN locations with known ping found")

    return location
