from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class VPNStatus:
    """Current VPN connection status."""

    connected: bool
    location: str | None = None
    interface: str | None = None
    raw: str = ""


@dataclass(slots=True, frozen=True)
class Location:
    """VPN location."""

    iso: str
    country: str
    city: str
    ping: int | None = None
