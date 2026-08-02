from __future__ import annotations

import shutil
import subprocess
import re

from avpm.backends.base import Backend
from avpm.exceptions import BackendError, BackendNotFoundError
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
        if not self.exists():
            raise BackendNotFoundError(
                f"'{self.executable}' was not found in PATH"
            )

        result = self._run("list-locations")

        if result.returncode != 0:
            raise BackendError(
                result.stderr.strip() or "Unable to obtain locations"
            )

        text = self._strip_ansi(result.stdout)

        locations: list[Location] = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("ISO"):
                continue

            if line.startswith("You can connect"):
                continue

            parts = re.split(r"\s{2,}", line)

            if len(parts) < 4:
                continue

            iso = parts[0]
            country = parts[1]
            city = parts[2]

            try:
                ping = int(parts[3])
            except ValueError:
                ping = None

            locations.append(
                Location(
                    iso=iso,
                    country=country,
                    city=city,
                    ping=ping,
                )
            )

        return locations

    @staticmethod
    def _strip_ansi(text: str) -> str:
        return re.sub(
            r"\x1b\[[0-9;]*m",
            "",
            text,
        )
