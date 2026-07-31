"""
Base command interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for all commands."""

    name: str = ""
    help: str = ""

    @abstractmethod
    def run(self, args) -> int:
        """Execute command."""