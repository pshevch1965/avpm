from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock
from zipfile import ZipFile

from avpm.exceptions import SupportError
from avpm.models import VPNStatus
from avpm.services.support import collect_report, create_support_archive


GENERATED_AT = datetime(2026, 8, 19, 12, 0, tzinfo=timezone.utc)


class CollectReportTests(unittest.TestCase):
    def test_collects_structured_diagnostics_without_sensitive_data(self) -> None:
        backend = MagicMock()
        backend.executable = "adguardvpn-cli"
        backend.exists.return_value = True
        backend.status.return_value = VPNStatus(
            connected=True,
            location="TALLINN",
            interface="tun0",
        )

        report = collect_report(backend, GENERATED_AT)
        serialized = json.dumps(report)

        self.assertEqual(report["vpn"]["location"], "TALLINN")
        self.assertEqual(report["vpn"]["interface"], "tun0")
        self.assertNotIn("public_ip", serialized)
        self.assertNotIn("username", serialized)
        self.assertNotIn("environment", serialized)


class CreateSupportArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = MagicMock()
        self.backend.executable = "adguardvpn-cli"
        self.backend.exists.return_value = True
        self.backend.status.return_value = VPNStatus(
            connected=True,
            location="KYIV",
            interface="tun0",
        )

    def test_creates_safe_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "support.zip"

            result = create_support_archive(
                output,
                backend=self.backend,
                generated_at=GENERATED_AT,
            )

            self.assertEqual(result, output.resolve())
            with ZipFile(output) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {"report.json", "README.txt"},
                )
                report = json.loads(archive.read("report.json"))
                self.assertEqual(report["vpn"]["location"], "KYIV")
            self.backend.export_logs.assert_not_called()

    def test_includes_logs_only_when_requested(self) -> None:
        def export_logs(path: Path) -> Path:
            path.write_bytes(b"raw logs")
            return path

        self.backend.export_logs.side_effect = export_logs

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "support.zip"
            create_support_archive(
                output,
                include_logs=True,
                backend=self.backend,
                generated_at=GENERATED_AT,
            )

            with ZipFile(output) as archive:
                self.assertIn("adguardvpn-logs.zip", archive.namelist())
                self.assertEqual(
                    archive.read("adguardvpn-logs.zip"),
                    b"raw logs",
                )

    def test_refuses_to_overwrite_existing_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "support.zip"
            output.write_bytes(b"existing")

            with self.assertRaisesRegex(
                SupportError,
                "Output file already exists",
            ):
                create_support_archive(output, backend=self.backend)
