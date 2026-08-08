from __future__ import annotations

import unittest
import json
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.status import run
from avpm.exceptions import BackendError
from avpm.models import VPNStatus


class StatusCommandTests(unittest.TestCase):
    @patch("avpm.commands.status.AdGuardBackend")
    def test_quiet_connected_returns_zero(self, backend_class) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=True,
            raw="Connected to TALLINN",
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=True, json=False))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "")

    @patch("avpm.commands.status.AdGuardBackend")
    def test_quiet_disconnected_returns_one(self, backend_class) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=False,
            raw="VPN is disconnected",
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=True, json=False))

        self.assertEqual(result, 1)
        self.assertEqual(output.getvalue(), "")

    @patch("avpm.commands.status.AdGuardBackend")
    def test_quiet_backend_error_returns_one(self, backend_class) -> None:
        backend_class.return_value.status.side_effect = BackendError(
            "Status failed"
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=True, json=False))

        self.assertEqual(result, 1)
        self.assertEqual(output.getvalue(), "")

    @patch("avpm.commands.status.AdGuardBackend")
    def test_regular_status_prints_raw_output(self, backend_class) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=True,
            raw="Connected to TALLINN",
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=False, json=False))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue().strip(), "Connected to TALLINN")

    @patch("avpm.commands.status.AdGuardBackend")
    def test_json_status(self, backend_class) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=True,
            location="TALLINN",
            raw="Connected to TALLINN in TUN mode, running on tun0",
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=False, json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertTrue(payload["connected"])
        self.assertEqual(payload["location"], "TALLINN")

    @patch("avpm.commands.status.AdGuardBackend")
    def test_json_backend_error(self, backend_class) -> None:
        backend_class.return_value.status.side_effect = BackendError(
            "Status failed"
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(quiet=False, json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(payload["connected"])
        self.assertEqual(payload["error"], "Status failed")


if __name__ == "__main__":
    unittest.main()
