from __future__ import annotations

import shutil
import subprocess
import re
from unittest import result

from avpm.backends.base import Backend
from avpm.exceptions import BackendError, BackendNotFoundError
from avpm.models import VPNStatus
from avpm.models import Location
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
        result.stdout = strip_ansi(result.stdout)
        result.stderr = strip_ansi(result.stderr)
        return result

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

        text = result.stdout

        locations: list[Location] = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if "COUNTRY" in line and "CITY" in line:
                continue

            if line.startswith("You can connect"):
                continue

            # Последнее поле — ping
            match = re.search(r"\s+(\d+)$", line)

            if not match:
                continue

            ping = int(match.group(1))

            data = line[:match.start()].strip()

            # ISO — первые 2 символа
            iso = data[:2]

            rest = data[2:].strip()

            parts = re.split(r"\s{2,}", rest)

            if len(parts) == 2:
                # иногда city сливается с country/ISO на первой строке
                city_match = re.search(r"([A-Za-zÀ-ÿ ()]+)\s+(\d+)$", parts[1])

                if city_match:
                    city = city_match.group(1).strip()
                    ping = int(city_match.group(2))

            if len(parts) < 2:
                continue

            country = parts[0]
            city = parts[1]

            locations.append(
                Location(
                    iso=iso,
                    country=country,
                    city=city,
                    ping=ping,
                )
            )
        return locations

