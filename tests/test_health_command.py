from __future__ import annotations

import json
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.health import run
from avpm.exceptions import BackendError, NetworkError
from avpm.models import VPNStatus


class HealthCommandTests(unittest.TestCase):
    @patch("avpm.commands.health.interface_exists", return_value=True)
    @patch("avpm.commands.health.fetch_public_ip")
    @patch("avpm.commands.health.AdGuardBackend")
    def test_reports_healthy_connection(
        self,
        backend_class,
        fetch_public_ip,
        interface_exists,
    ) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=True,
            location="TALLINN",
            interface="tun0",
        )
        fetch_public_ip.return_value = "203.0.113.10"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=False))

        self.assertEqual(result, 0)
        self.assertIn("OK (connected to TALLINN)", output.getvalue())
        self.assertIn("OK (tun0)", output.getvalue())
        self.assertIn("Result         : Healthy", output.getvalue())
        interface_exists.assert_called_once_with("tun0")

    @patch("avpm.commands.health.fetch_public_ip")
    @patch("avpm.commands.health.AdGuardBackend")
    def test_disconnected_connection_is_unhealthy(
        self,
        backend_class,
        fetch_public_ip,
    ) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=False,
        )
        fetch_public_ip.return_value = "203.0.113.10"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(payload["healthy"])
        self.assertFalse(payload["connected"])
        self.assertFalse(payload["interface_up"])

    @patch("avpm.commands.health.interface_exists", return_value=False)
    @patch("avpm.commands.health.fetch_public_ip")
    @patch("avpm.commands.health.AdGuardBackend")
    def test_missing_interface_is_unhealthy(
        self,
        backend_class,
        fetch_public_ip,
        interface_exists,
    ) -> None:
        backend_class.return_value.status.return_value = VPNStatus(
            connected=True,
            location="KYIV",
            interface="tun0",
        )
        fetch_public_ip.return_value = "203.0.113.10"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=False))

        self.assertEqual(result, 1)
        self.assertIn("NOT FOUND (tun0)", output.getvalue())
        self.assertIn("Problems detected", output.getvalue())
        interface_exists.assert_called_once_with("tun0")

    @patch("avpm.commands.health.fetch_public_ip")
    @patch("avpm.commands.health.AdGuardBackend")
    def test_reports_backend_and_network_errors(
        self,
        backend_class,
        fetch_public_ip,
    ) -> None:
        backend_class.return_value.status.side_effect = BackendError(
            "Status failed"
        )
        fetch_public_ip.side_effect = NetworkError(
            "Unable to obtain public IP"
        )
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertEqual(payload["errors"]["vpn"], "Status failed")
        self.assertEqual(
            payload["errors"]["public_ip"],
            "Unable to obtain public IP",
        )
