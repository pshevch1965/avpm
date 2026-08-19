from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError


class AdGuardBackendStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = AdGuardBackend()

    @patch.object(AdGuardBackend, "exists", return_value=True)
    @patch.object(AdGuardBackend, "_run")
    def test_returns_connected_status(self, run_mock, exists_mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            args=["adguardvpn-cli", "status"],
            returncode=0,
            stdout=(
                "Connected to \x1b[1mKYIV\x1b[0m in "
                "\x1b[1mTUN\x1b[0m mode, running on "
                "\x1b[1mtun0\x1b[0m\n"
            ),
            stderr="",
        )

        status = self.backend.status()

        self.assertTrue(status.connected)
        self.assertEqual(status.location, "KYIV")
        self.assertEqual(status.interface, "tun0")
        self.assertIn("KYIV", status.raw)
        self.assertNotIn("\x1b", status.raw)

    @patch.object(AdGuardBackend, "exists", return_value=True)
    @patch.object(AdGuardBackend, "_run")
    def test_returns_disconnected_status(self, run_mock, exists_mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            args=["adguardvpn-cli", "status"],
            returncode=0,
            stdout="VPN is disconnected\n",
            stderr="",
        )

        status = self.backend.status()

        self.assertFalse(status.connected)
        self.assertIsNone(status.location)
        self.assertIsNone(status.interface)

    @patch.object(AdGuardBackend, "exists", return_value=True)
    @patch.object(AdGuardBackend, "_run")
    def test_raises_backend_error_on_failed_command(
        self,
        run_mock,
        exists_mock,
    ) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            args=["adguardvpn-cli", "status"],
            returncode=1,
            stdout="",
            stderr="Status failed",
        )

        with self.assertRaisesRegex(BackendError, "Status failed"):
            self.backend.status()


class AdGuardBackendExportLogsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = AdGuardBackend()

    @patch.object(AdGuardBackend, "exists", return_value=True)
    @patch.object(AdGuardBackend, "_run")
    def test_exports_logs(self, run_mock, exists_mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="Logs exported",
            stderr="",
        )

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "logs.zip"
            output.write_bytes(b"logs")

            result = self.backend.export_logs(output)

        self.assertEqual(result, output)
        run_mock.assert_called_once_with(
            "export-logs",
            "-o",
            str(output),
            "-f",
        )

    @patch.object(AdGuardBackend, "exists", return_value=True)
    @patch.object(AdGuardBackend, "_run")
    def test_reports_missing_export(self, run_mock, exists_mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr="",
        )

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "logs.zip"

            with self.assertRaisesRegex(
                BackendError,
                "log archive was not created",
            ):
                self.backend.export_logs(output)


if __name__ == "__main__":
    unittest.main()
