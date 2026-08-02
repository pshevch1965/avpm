from __future__ import annotations

import shutil
import subprocess

from avpm.backends.base import Backend
from avpm.exceptions import BackendNotFoundError
from avpm.models import VPNStatus
from avpm.models import Location


class AdGuardBackend(Backend):
    def __init__(self, executable: str = "adguardvpn-cli") -> None:
        self.executable = executable

    def exists(self) -> bool:
        return shutil.which(self.executable) is not None

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self.executable, *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def status(self) -> VPNStatus:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        result = self._run("status")
        text = result.stdout.strip()

        return VPNStatus(
            connected="connected" in text.lower(),
            raw=text,
        )

    def connect(self, location: str | None = None) -> None:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        args = ["connect"]

        if location:
            args.extend(["-l", location])

        result = self._run(*args)

        if result.returncode != 0:
            raise BackendError(result.stderr.strip() or "Connection failed")

    def disconnect(self) -> None:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        result = self._run("disconnect")

        if result.returncode != 0:
            raise BackendError(result.stderr.strip() or "Disconnect failed")

    def locations(self) -> list[Location]:
        return []