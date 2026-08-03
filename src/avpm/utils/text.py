from __future__ import annotations

import re


ANSI_ESCAPE = re.compile(
    r"\x1B\[[0-?]*[ -/]*[@-~]"
)


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from terminal output."""
    return ANSI_ESCAPE.sub("", text)