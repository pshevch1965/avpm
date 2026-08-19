from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.find import run
from avpm.models import Location


class FindCommandTests(unittest.TestCase):
    @patch("avpm.commands.find.AdGuardBackend.locations")
    def test_prints_matching_locations(self, locations) -> None:
        locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 20),
            Location("DE", "Germany", "Berlin", 40),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(query="tall", max_ping=None, json=False)
            )

        self.assertEqual(result, 0)
        self.assertIn("Tallinn", output.getvalue())
        self.assertNotIn("Berlin", output.getvalue())

    @patch("avpm.commands.find.AdGuardBackend.locations")
    def test_combines_query_and_max_ping(self, locations) -> None:
        locations.return_value = [
            Location("DE", "Germany", "Berlin", 40),
            Location("DE", "Germany", "Frankfurt", 60),
        ]
        output = StringIO()

        with redirect_stdout(output):
            run(Namespace(query="DE", max_ping=50, json=False))

        self.assertIn("Berlin", output.getvalue())
        self.assertNotIn("Frankfurt", output.getvalue())

    @patch("avpm.commands.find.AdGuardBackend.locations")
    def test_prints_json_results(self, locations) -> None:
        locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 20),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(query="est", max_ping=None, json=True)
            )

        self.assertEqual(result, 0)
        self.assertIn('"city": "Tallinn"', output.getvalue())

    @patch("avpm.commands.find.AdGuardBackend.locations")
    def test_reports_no_matches(self, locations) -> None:
        locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 20),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(query="missing", max_ping=None, json=False)
            )

        self.assertEqual(result, 0)
        self.assertEqual(
            output.getvalue(),
            "No VPN locations matched query.\n",
        )
