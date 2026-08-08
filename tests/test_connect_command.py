from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.connect import run
from avpm.models import Location


class ConnectCommandTests(unittest.TestCase):
    @patch("avpm.commands.connect.AdGuardBackend")
    def test_connects_to_fastest_city(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("LV", "Latvia", "Riga", 18),
        ]
        backend.connect.return_value = "Successfully connected"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(location=None, fastest=True))

        self.assertEqual(result, 0)
        backend.locations.assert_called_once_with()
        backend.connect.assert_called_once_with("Riga")
        self.assertIn("Fastest location: Riga, Latvia (18 ms)", output.getvalue())

    @patch("avpm.commands.connect.AdGuardBackend")
    def test_reports_missing_ping_data(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.locations.return_value = [
            Location("XX", "Unknown", "Unknown", None),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(location=None, fastest=True))

        self.assertEqual(result, 1)
        backend.connect.assert_not_called()
        self.assertIn("No VPN locations with known ping found", output.getvalue())


if __name__ == "__main__":
    unittest.main()
