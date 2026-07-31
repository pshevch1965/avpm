from __future__ import annotations

from avpm.core.command import Command


class HelpCommand(Command):

    name = "help"
    help = "Show help"

    def __init__(self, registry):
        self.registry = registry

    def run(self, args) -> int:

        print()

        print("Available commands")

        print()

        for cmd in self.registry.all():
            print(f"{cmd.name:12} {cmd.help}")

        return 0