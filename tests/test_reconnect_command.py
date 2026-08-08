from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.reconnect import run
from avpm.models import Location, VPNStatus


class ReconnectCommandTests(unittest.TestCase):
    @patch("avpm.commands.reconnect.AdGuardBackend")
    def test_if_needed_skips_active_connection(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.status.return_value = VPNStatus(connected=True)
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(
                    location=None,
                    if_needed=True,
                    fastest=True,
                    country=None,
                )
            )

        self.assertEqual(result, 0)
        backend.status.assert_called_once_with()
        backend.locations.assert_not_called()
        backend.connect.assert_not_called()
        self.assertEqual(output.getvalue().strip(), "VPN is already connected.")

    @patch("avpm.commands.reconnect.AdGuardBackend")
    def test_if_needed_connects_when_disconnected(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.status.return_value = VPNStatus(connected=False)
        backend.connect.return_value = "Successfully connected"
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(
                    location="Tallinn",
                    if_needed=True,
                    fastest=False,
                    country=None,
                )
            )

        self.assertEqual(result, 0)
        backend.status.assert_called_once_with()
        backend.connect.assert_called_once_with("Tallinn")
        self.assertIn("Successfully connected", output.getvalue())

    @patch("avpm.commands.reconnect.AdGuardBackend")
    def test_regular_reconnect_does_not_check_status(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.connect.return_value = "Successfully connected"
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(
                    location=None,
                    if_needed=False,
                    fastest=False,
                    country=None,
                )
            )

        self.assertEqual(result, 0)
        backend.status.assert_not_called()
        backend.connect.assert_called_once_with(None)

    @patch("avpm.commands.reconnect.AdGuardBackend")
    def test_reconnects_to_fastest_city(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 17),
        ]
        backend.connect.return_value = "Successfully connected"
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(
                    location=None,
                    if_needed=False,
                    fastest=True,
                    country=None,
                )
            )

        self.assertEqual(result, 0)
        backend.locations.assert_called_once_with()
        backend.connect.assert_called_once_with("Tallinn")
        self.assertIn(
            "Fastest location: Tallinn, Estonia (17 ms)",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
