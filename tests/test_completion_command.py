from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.completion import completion_candidates, run
from avpm.models import Location


class CompletionCommandTests(unittest.TestCase):
    def test_generates_bash_completion(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(shell="bash"))

        script = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("complete -F _vpn_completion vpn", script)
        self.assertIn("--if-needed", script)
        self.assertIn("--json", script)
        self.assertIn("_vpn_country_cache_time=-300", script)
        self.assertIn("_vpn_refresh_location_cache", script)
        self.assertIn(
            "vpn completion bash --candidates countries",
            script,
        )

    def test_generates_zsh_completion(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(shell="zsh"))

        script = output.getvalue()
        self.assertEqual(result, 0)
        self.assertTrue(script.startswith("#compdef vpn"))
        self.assertIn("'completion:Generate shell completion'", script)
        self.assertIn("'--help[Show help]'", script)
        self.assertIn(
            "'--country[Filter by country]:country:->countries'",
            script,
        )
        self.assertIn("'1:shell:(bash zsh)'", script)
        self.assertIn("locations) _arguments", script)
        self.assertIn('words=("${words[@]:1}")', script)
        self.assertIn("(( CURRENT-- ))", script)
        self.assertIn("_vpn_country_cache_time=-300", script)
        self.assertIn("_vpn_complete_locations", script)

    def test_generates_country_candidates(self) -> None:
        locations = [
            Location("EE", "Estonia", "Tallinn", 20),
            Location("DE", "Germany", "Berlin", 40),
            Location("DE", "Germany", "Frankfurt", 50),
        ]

        self.assertEqual(
            completion_candidates(locations, "countries"),
            ["DE:Germany", "Germany:DE", "EE:Estonia", "Estonia:EE"],
        )

    def test_generates_location_candidates(self) -> None:
        locations = [
            Location("EE", "Estonia", "Tallinn", 20),
            Location("DE", "Germany", "Berlin", 40),
        ]

        self.assertEqual(
            completion_candidates(locations, "locations"),
            ["Berlin:Germany (DE)", "Tallinn:Estonia (EE)"],
        )

    @patch("avpm.backends.adguard.AdGuardBackend.locations")
    def test_prints_candidates_for_shell_completion(self, locations) -> None:
        locations.return_value = [
            Location("EE", "Estonia", "Tallinn", 20),
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(shell="zsh", candidates="countries"))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "EE:Estonia\nEstonia:EE\n")


if __name__ == "__main__":
    unittest.main()
