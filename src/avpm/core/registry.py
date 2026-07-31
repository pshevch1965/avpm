"""
Command registry.
"""

from __future__ import annotations

from typing import Dict

from avpm.core.command import Command


class Registry:

    def __init__(self) -> None:
        self.commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self.commands[command.name] = command

    def get(self, name: str) -> Command | None:
        return self.commands.get(name)

    def all(self):
        return sorted(self.commands.values(), key=lambda c: c.name)