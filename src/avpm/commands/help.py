from __future__ import annotations

import argparse


def run(args: argparse.Namespace) -> int:
    args.parser.print_help()
    return 0


def register(
    subparsers,
    root_parser: argparse.ArgumentParser,
) -> None:
    parser = subparsers.add_parser(
        "help",
        help="Show help",
    )

    parser.set_defaults(func=run, parser=root_parser)
