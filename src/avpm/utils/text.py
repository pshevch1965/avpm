from __future__ import annotations

import re


ANSI_ESCAPE = re.compile(
    r"\x1b\[[0-9;]*m"
)


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from terminal output."""
    return ANSI_ESCAPE.sub("", text)