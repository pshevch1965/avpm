from __future__ import annotations

import json
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from avpm.commands.config import (
    run_get,
    run_path,
    run_set,
    run_show,
    run_unset,
)


class ConfigCommandTests(unittest.TestCase):
    @patch("avpm.commands.config.config_path")
    @patch("avpm.commands.config.load_config")
    def test_shows_configuration(self, load_config, config_path) -> None:
        load_config.return_value = {
            "default_country": "EE",
            "watch_interval": 2.0,
            "output_format": "text",
        }
        config_path.return_value = Path("/tmp/config.json")
        output = StringIO()

        with redirect_stdout(output):
            result = run_show(Namespace(json=False))

        self.assertEqual(result, 0)
        self.assertIn("default_country   : EE", output.getvalue())
        self.assertIn("/tmp/config.json", output.getvalue())

    @patch("avpm.commands.config.load_config")
    def test_shows_json_configuration(self, load_config) -> None:
        load_config.return_value = {
            "default_country": None,
            "watch_interval": 2.0,
            "output_format": "json",
        }
        output = StringIO()

        with redirect_stdout(output):
            result = run_show(Namespace(json=True))

        self.assertEqual(result, 0)
        self.assertEqual(
            json.loads(output.getvalue())["output_format"],
            "json",
        )

    @patch("avpm.commands.config.load_config")
    def test_gets_setting(self, load_config) -> None:
        load_config.return_value = {"default_country": None}
        output = StringIO()

        with redirect_stdout(output):
            result = run_get(Namespace(key="default_country"))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "-\n")

    @patch("avpm.commands.config.set_config_value", return_value="EE")
    def test_sets_setting(self, set_value) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run_set(
                Namespace(key="default_country", value="ee")
            )

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "default_country = EE\n")

    @patch("avpm.commands.config.unset_config_value", return_value=2.0)
    def test_unsets_setting(self, unset_value) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run_unset(Namespace(key="watch_interval"))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "watch_interval = 2.0\n")

    @patch("avpm.commands.config.config_path")
    def test_prints_path(self, config_path) -> None:
        config_path.return_value = Path("/tmp/config.json")
        output = StringIO()

        with redirect_stdout(output):
            result = run_path(Namespace())

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "/tmp/config.json\n")
