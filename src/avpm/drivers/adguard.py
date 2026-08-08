from __future__ import annotations

import shutil
import subprocess

from avpm.models import VPNStatus


class AdGuardDriver:
    CLI = "adguardvpn-cli"

    @classmethod
    def exists(cls) -> bool:
        return shutil.which(cls.CLI) is not None

    @classmethod
    def _run(cls, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [cls.CLI, *args],
            capture_output=True,
            text=True,
            check=False,
        )

    @classmethod
    def status(cls) -> VPNStatus:
        if not cls.exists():
            raise FileNotFoundError(cls.CLI)

        result = cls._run("status")

        text = result.stdout.strip()

        connected = "connected" in text.lower()
        location = None

        return VPNStatus(
            connected=connected,
            location=location,
            raw=text,
        )