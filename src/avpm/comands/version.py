from __future__ import annotations

from avpm import __version__
from avpm.core.command import Command


class VersionCommand(Command):

    name = "version"
    help = "Show AVPM version"

    def run(self, args) -> int:
        print(__version__)
        return 0