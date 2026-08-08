from __future__ import annotations

import shutil
import subprocess
from avpm.backends.base import Backend
from avpm.exceptions import BackendError, BackendNotFoundError
from avpm.models import Location, VPNStatus
from avpm.services.locations import parse_locations
from avpm.services.status import extract_location, is_connected
from avpm.utils.text import strip_ansi


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

        if result.returncode != 0:
            raise BackendError(
                result.stderr.strip()
                or result.stdout.strip()
                or "Unable to obtain VPN status"
            )

        text = strip_ansi(result.stdout).strip()

        return VPNStatus(
            connected=is_connected(text),
            location=extract_location(text),
            raw=text,
        )

    def connect(self, location: str | None = None) -> str:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        if location:
            result = self._run("connect", "-l", location)
        else:
            result = self._run("connect")

        if result.returncode != 0:
            raise BackendError(
                result.stderr.strip() or
                result.stdout.strip() or
                "Unable to connect VPN"
            )

        return result.stdout.strip()

    def disconnect(self) -> None:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        result = self._run("disconnect")

        if result.returncode != 0:
            raise BackendError(result.stderr.strip() or "Disconnect failed")

    def locations(self) -> list[Location]:
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        result = self._run("list-locations")

        if result.returncode != 0:
            raise BackendError(
                result.stderr.strip() or "Unable to obtain locations"
            )

        return parse_locations(result.stdout)
