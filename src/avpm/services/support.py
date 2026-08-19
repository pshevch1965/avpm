from __future__ import annotations

import json
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from avpm import __version__
from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError, SupportError


SUPPORT_README = """\
AVPM support archive

report.json contains AVPM, Python, Linux, backend, and structured VPN status
information intended for troubleshooting.

Excluded by default: public IP address, username, home path, environment
variables, and raw AdGuard VPN logs.

If adguardvpn-logs.zip is present, it was explicitly requested with
--include-logs. Raw logs may contain sensitive diagnostic information. Review
them before sharing the archive.
"""


def collect_report(
    backend: AdGuardBackend,
    generated_at: datetime | None = None,
) -> dict[str, object]:
    timestamp = generated_at or datetime.now(timezone.utc)
    available = backend.exists()
    vpn: dict[str, object] = {
        "status_available": False,
        "connected": False,
        "location": None,
        "interface": None,
    }
    errors: dict[str, str] = {}

    if available:
        try:
            status = backend.status()
            vpn.update(
                {
                    "status_available": True,
                    "connected": status.connected,
                    "location": status.location,
                    "interface": status.interface,
                }
            )
        except BackendError as exc:
            errors["vpn_status"] = str(exc)

    return {
        "generated_at": timestamp.astimezone(timezone.utc).isoformat(),
        "avpm_version": __version__,
        "python_version": platform.python_version(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "backend": {
            "name": backend.executable,
            "available": available,
        },
        "vpn": vpn,
        "errors": errors,
    }


def create_support_archive(
    output: Path | None = None,
    *,
    include_logs: bool = False,
    backend: AdGuardBackend | None = None,
    generated_at: datetime | None = None,
) -> Path:
    timestamp = generated_at or datetime.now(timezone.utc)
    destination = output or Path.cwd() / (
        f"avpm-support-{timestamp:%Y%m%d-%H%M%S}.zip"
    )
    destination = destination.expanduser().resolve()

    if destination.exists():
        raise SupportError(f"Output file already exists: {destination}")

    if not destination.parent.is_dir():
        raise SupportError(
            f"Output directory does not exist: {destination.parent}"
        )

    active_backend = backend or AdGuardBackend()
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            prefix=".avpm-support-",
            suffix=".zip",
            dir=destination.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)

        with ZipFile(
            temporary_path,
            "w",
            compression=ZIP_DEFLATED,
        ) as archive:
            report = collect_report(active_backend, timestamp)
            archive.writestr(
                "report.json",
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            )
            archive.writestr("README.txt", SUPPORT_README)

            if include_logs:
                with tempfile.TemporaryDirectory() as directory:
                    logs_path = Path(directory) / "adguardvpn-logs.zip"
                    active_backend.export_logs(logs_path)
                    archive.write(logs_path, "adguardvpn-logs.zip")

        temporary_path.replace(destination)
        return destination
    except (BackendError, OSError) as exc:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
        raise SupportError(f"Unable to create support archive: {exc}") from exc
