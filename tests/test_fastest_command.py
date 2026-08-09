from __future__ import annotations

import unittest
import json
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.fastest import run
from avpm.models import Location


class FastestCommandTests(unittest.TestCase):
    @patch("avpm.commands.fastest.AdGuardBackend")
    def test_lists_fastest_locations_in_country(self, backend_class) -> None:
        backend_class.return_value.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("DE", "Germany", "Frankfurt", 57),
            Location("EE", "Estonia", "Tallinn", 18),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(count=5, country="DE", json=False))

        text = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("Berlin", text)
        self.assertIn("Frankfurt", text)
        self.assertNotIn("Tallinn", text)

    @patch("avpm.commands.fastest.AdGuardBackend")
    def test_prints_json_fastest_locations(self, backend_class) -> None:
        backend_class.return_value.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 18),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(count=1, country=None, json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["city"], "Tallinn")


if __name__ == "__main__":
    unittest.main()
