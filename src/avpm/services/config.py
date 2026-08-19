from __future__ import annotations

import json
import os
import tempfile
from argparse import Namespace
from pathlib import Path

from avpm.exceptions import ConfigError


DEFAULT_CONFIG: dict[str, object] = {
    "default_country": None,
    "watch_interval": 2.0,
    "output_format": "text",
}

JSON_COMMANDS = {
    "status",
    "locations",
    "fastest",
    "find",
    "ip",
    "health",
    "watch",
}


def config_path() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")

    if base:
        return Path(base).expanduser() / "avpm" / "config.json"

    return Path.home() / ".config" / "avpm" / "config.json"


def validate_config_value(key: str, value: object) -> object:
    if key not in DEFAULT_CONFIG:
        allowed = ", ".join(DEFAULT_CONFIG)
        raise ConfigError(f"Unknown setting '{key}'. Allowed: {allowed}")

    if key == "default_country":
        if not isinstance(value, str):
            raise ConfigError("default_country must be text")

        country = value.strip()

        if not country:
            raise ConfigError("default_country cannot be empty")

        return country.upper() if len(country) == 2 else country

    if key == "watch_interval":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ConfigError("watch_interval must be a number")

        interval = float(value)

        if interval <= 0:
            raise ConfigError("watch_interval must be greater than zero")

        return interval

    if not isinstance(value, str) or value not in {"text", "json"}:
        raise ConfigError("output_format must be 'text' or 'json'")

    return value


def parse_config_value(key: str, value: str) -> object:
    if key == "watch_interval":
        try:
            return validate_config_value(key, float(value))
        except ValueError as exc:
            raise ConfigError("watch_interval must be a number") from exc

    return validate_config_value(key, value)


def load_overrides(path: Path | None = None) -> dict[str, object]:
    source = path or config_path()

    if not source.exists():
        return {}

    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Unable to read configuration: {exc}") from exc

    if not isinstance(payload, dict):
        raise ConfigError("Configuration root must be a JSON object")

    overrides: dict[str, object] = {}

    for key, value in payload.items():
        overrides[key] = validate_config_value(key, value)

    return overrides


def load_config(path: Path | None = None) -> dict[str, object]:
    return {**DEFAULT_CONFIG, **load_overrides(path)}


def apply_runtime_config(args: Namespace) -> None:
    command = getattr(args, "command", None)

    if command == "config":
        return

    uses_config = command in JSON_COMMANDS or command in {
        "connect",
        "reconnect",
    }

    if not uses_config:
        return

    config = load_config()

    if command in JSON_COMMANDS and not getattr(args, "quiet", False):
        if getattr(args, "text", False):
            args.json = False
        elif not getattr(args, "json", False):
            args.json = config["output_format"] == "json"

    if command == "watch" and args.interval is None:
        args.interval = config["watch_interval"]

    if command == "fastest" and args.country is None:
        args.country = config["default_country"]

    if (
        command in {"connect", "reconnect"}
        and args.fastest
        and args.country is None
    ):
        args.country = config["default_country"]


def save_overrides(
    overrides: dict[str, object],
    path: Path | None = None,
) -> Path:
    destination = path or config_path()

    try:
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".config-",
            suffix=".json",
            dir=destination.parent,
            delete=False,
        ) as temporary:
            json.dump(overrides, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
            temporary_path = Path(temporary.name)

        temporary_path.chmod(0o600)
        temporary_path.replace(destination)
        destination.chmod(0o600)
        return destination
    except OSError as exc:
        raise ConfigError(f"Unable to save configuration: {exc}") from exc


def set_config_value(
    key: str,
    value: str,
    path: Path | None = None,
) -> object:
    parsed = parse_config_value(key, value)
    overrides = load_overrides(path)
    overrides[key] = parsed
    save_overrides(overrides, path)
    return parsed


def unset_config_value(
    key: str,
    path: Path | None = None,
) -> object:
    if key not in DEFAULT_CONFIG:
        parse_config_value(key, "")

    overrides = load_overrides(path)
    overrides.pop(key, None)
    save_overrides(overrides, path)
    return DEFAULT_CONFIG[key]
