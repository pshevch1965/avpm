from __future__ import annotations

import platform

from avpm import __version__
from avpm.core.command import Command


class AboutCommand(Command):

    name = "about"
    help = "About AVPM"

    def run(self, args) -> int:

        print("AVPM")
        print("AdGuard VPN Manager")
        print()
        print(f"Version : {__version__}")
        print(f"Python  : {platform.python_version()}")

        return 0