from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class VPNStatus:
    """Current VPN connection status."""

    connected: bool
    location: str | None = None
    raw: str = ""


@dataclass(slots=True, frozen=True)
class Location:
    """Available VPN location."""

    country: str
    city: str
    code: str | None = None