from __future__ import annotations

import unittest
from argparse import Namespace
from unittest.mock import patch

from avpm.services.config import apply_runtime_config


CONFIG = {
    "default_country": "EE",
    "watch_interval": 1.5,
    "output_format": "json",
}


class RuntimeConfigTests(unittest.TestCase):
    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_applies_default_country_to_fastest(self, load_config) -> None:
        args = Namespace(
            command="fastest",
            country=None,
            json=False,
            text=False,
        )

        apply_runtime_config(args)

        self.assertEqual(args.country, "EE")
        self.assertTrue(args.json)
        load_config.assert_called_once_with()

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_preserves_explicit_fastest_options(self, load_config) -> None:
        args = Namespace(
            command="fastest",
            country="DE",
            json=False,
            text=True,
        )

        apply_runtime_config(args)

        self.assertEqual(args.country, "DE")
        self.assertFalse(args.json)

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_applies_country_only_to_fastest_connections(
        self,
        load_config,
    ) -> None:
        fastest = Namespace(
            command="connect",
            fastest=True,
            country=None,
        )
        regular = Namespace(
            command="connect",
            fastest=False,
            country=None,
        )

        apply_runtime_config(fastest)
        apply_runtime_config(regular)

        self.assertEqual(fastest.country, "EE")
        self.assertIsNone(regular.country)

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_applies_configured_watch_options(self, load_config) -> None:
        args = Namespace(
            command="watch",
            interval=None,
            json=False,
            text=False,
        )

        apply_runtime_config(args)

        self.assertEqual(args.interval, 1.5)
        self.assertTrue(args.json)

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_preserves_explicit_watch_options(self, load_config) -> None:
        args = Namespace(
            command="watch",
            interval=4.0,
            json=False,
            text=True,
        )

        apply_runtime_config(args)

        self.assertEqual(args.interval, 4.0)
        self.assertFalse(args.json)

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_preserves_explicit_json_output(self, load_config) -> None:
        args = Namespace(
            command="health",
            json=True,
            text=False,
        )

        apply_runtime_config(args)

        self.assertTrue(args.json)

    @patch("avpm.services.config.load_config", return_value=CONFIG)
    def test_quiet_status_ignores_output_format(self, load_config) -> None:
        args = Namespace(
            command="status",
            quiet=True,
            json=False,
            text=False,
        )

        apply_runtime_config(args)

        self.assertFalse(args.json)

    @patch("avpm.services.config.load_config")
    def test_config_command_remains_available_without_loading(self, load_config) -> None:
        args = Namespace(command="config")

        apply_runtime_config(args)

        load_config.assert_not_called()


if __name__ == "__main__":
    unittest.main()
