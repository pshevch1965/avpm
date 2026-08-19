from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from avpm.exceptions import ConfigError
from avpm.services.config import (
    DEFAULT_CONFIG,
    config_path,
    load_config,
    set_config_value,
    unset_config_value,
)


class ConfigPathTests(unittest.TestCase):
    def test_uses_xdg_config_home(self) -> None:
        with patch.dict(
            os.environ,
            {"XDG_CONFIG_HOME": "/tmp/custom-config"},
        ):
            self.assertEqual(
                config_path(),
                Path("/tmp/custom-config/avpm/config.json"),
            )


class ConfigStorageTests(unittest.TestCase):
    def test_returns_defaults_without_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"

            self.assertEqual(load_config(path), DEFAULT_CONFIG)

    def test_sets_validated_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "avpm" / "config.json"

            self.assertEqual(
                set_config_value("default_country", "ee", path),
                "EE",
            )
            self.assertEqual(
                set_config_value("watch_interval", "1.5", path),
                1.5,
            )
            self.assertEqual(
                set_config_value("output_format", "json", path),
                "json",
            )

            config = load_config(path)
            self.assertEqual(config["default_country"], "EE")
            self.assertEqual(config["watch_interval"], 1.5)
            self.assertEqual(config["output_format"], "json")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_unset_restores_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            set_config_value("default_country", "DE", path)

            result = unset_config_value("default_country", path)

            self.assertIsNone(result)
            self.assertIsNone(load_config(path)["default_country"])
            self.assertNotIn(
                "default_country",
                json.loads(path.read_text(encoding="utf-8")),
            )

    def test_rejects_invalid_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"

            with self.assertRaisesRegex(ConfigError, "greater than zero"):
                set_config_value("watch_interval", "0", path)

            with self.assertRaisesRegex(ConfigError, "text.*json"):
                set_config_value("output_format", "yaml", path)

    def test_rejects_invalid_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text("not json", encoding="utf-8")

            with self.assertRaisesRegex(
                ConfigError,
                "Unable to read configuration",
            ):
                load_config(path)

    def test_rejects_wrong_json_types(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(
                '{"watch_interval": "fast"}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ConfigError, "must be a number"):
                load_config(path)
