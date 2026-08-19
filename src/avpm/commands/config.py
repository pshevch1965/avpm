from __future__ import annotations

from argparse import Namespace

from avpm.exceptions import ConfigError
from avpm.services.config import (
    DEFAULT_CONFIG,
    config_path,
    load_config,
    set_config_value,
    unset_config_value,
)
from avpm.ui import print_json


def display_value(value: object) -> str:
    return "-" if value is None else str(value)


def run_show(args: Namespace) -> int:
    config = load_config()

    if getattr(args, "json", False):
        print_json(config)
        return 0

    print("AVPM Configuration")
    print()
    print(f"{'Path':<18}: {config_path()}")

    for key, value in config.items():
        print(f"{key:<18}: {display_value(value)}")

    return 0


def run_get(args: Namespace) -> int:
    if args.key not in DEFAULT_CONFIG:
        raise ConfigError(f"Unknown setting '{args.key}'")

    print(display_value(load_config()[args.key]))
    return 0


def run_set(args: Namespace) -> int:
    value = set_config_value(args.key, args.value)
    print(f"{args.key} = {display_value(value)}")
    return 0


def run_unset(args: Namespace) -> int:
    value = unset_config_value(args.key)
    print(f"{args.key} = {display_value(value)}")
    return 0


def run_path(args: Namespace) -> int:
    print(config_path())
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "config",
        help="Manage AVPM configuration",
    )
    parser.set_defaults(func=run_show, json=False)
    actions = parser.add_subparsers(dest="config_command")

    show_parser = actions.add_parser("show", help="Show configuration")
    show_parser.add_argument(
        "--json",
        action="store_true",
        help="Print configuration as JSON",
    )
    show_parser.set_defaults(func=run_show)

    get_parser = actions.add_parser("get", help="Get a setting")
    get_parser.add_argument("key", choices=tuple(DEFAULT_CONFIG))
    get_parser.set_defaults(func=run_get)

    set_parser = actions.add_parser("set", help="Set a setting")
    set_parser.add_argument("key", choices=tuple(DEFAULT_CONFIG))
    set_parser.add_argument("value")
    set_parser.set_defaults(func=run_set)

    unset_parser = actions.add_parser("unset", help="Reset a setting")
    unset_parser.add_argument("key", choices=tuple(DEFAULT_CONFIG))
    unset_parser.set_defaults(func=run_unset)

    path_parser = actions.add_parser("path", help="Show configuration path")
    path_parser.set_defaults(func=run_path)
