from __future__ import annotations

import unittest
import json
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.locations import run
from avpm.models import Location


class LocationsCommandTests(unittest.TestCase):
    @patch("avpm.commands.locations.AdGuardBackend")
    def test_prints_filtered_locations(self, backend_class) -> None:
        backend_class.return_value.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 18),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(country="EE", max_ping=None, json=False))

        self.assertEqual(result, 0)
        self.assertIn("Tallinn", output.getvalue())
        self.assertNotIn("Berlin", output.getvalue())

    @patch("avpm.commands.locations.AdGuardBackend")
    def test_reports_empty_filter_result(self, backend_class) -> None:
        backend_class.return_value.locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 18),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(country="DE", max_ping=None, json=False))

        self.assertEqual(result, 0)
        self.assertEqual(
            output.getvalue().strip(),
            "No VPN locations matched filters.",
        )

    @patch("avpm.commands.locations.AdGuardBackend")
    def test_prints_json_locations(self, backend_class) -> None:
        backend_class.return_value.locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 18),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(country=None, max_ping=None, json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(payload[0]["iso"], "EE")
        self.assertEqual(payload[0]["city"], "Tallinn")


if __name__ == "__main__":
    unittest.main()
