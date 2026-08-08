from __future__ import annotations

import unittest
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
            result = run(Namespace(country="EE", max_ping=None))

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
            result = run(Namespace(country="DE", max_ping=None))

        self.assertEqual(result, 0)
        self.assertEqual(
            output.getvalue().strip(),
            "No VPN locations matched filters.",
        )


if __name__ == "__main__":
    unittest.main()
