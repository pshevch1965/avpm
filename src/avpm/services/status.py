from __future__ import annotations

import re


CONNECTED_WORD = re.compile(r"\bconnected\b", re.IGNORECASE)
CONNECTED_LOCATION = re.compile(
    r"\bconnected\s+to\s+(.+?)\s+in\s+\S+\s+mode\b",
    re.IGNORECASE,
)
VPN_INTERFACE = re.compile(
    r"\brunning\s+on\s+([^\s,]+)",
    re.IGNORECASE,
)


def is_connected(status_text: str) -> bool:
    """Return whether AdGuard VPN status reports an active connection."""
    return CONNECTED_WORD.search(status_text) is not None


def extract_location(status_text: str) -> str | None:
    """Extract the active location from AdGuard VPN status output."""
    match = CONNECTED_LOCATION.search(status_text)
    return match.group(1) if match else None


def extract_interface(status_text: str) -> str | None:
    """Extract the active VPN network interface."""
    match = VPN_INTERFACE.search(status_text)
    return match.group(1) if match else None
