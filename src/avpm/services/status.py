from __future__ import annotations

import re


CONNECTED_WORD = re.compile(r"\bconnected\b", re.IGNORECASE)


def is_connected(status_text: str) -> bool:
    """Return whether AdGuard VPN status reports an active connection."""
    return CONNECTED_WORD.search(status_text) is not None
