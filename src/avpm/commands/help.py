from __future__ import annotations


def run(args) -> int:
    args.parser.print_help()
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "help",
        help="Show help",
    )

    parser.set_defaults(func=run, parser=subparsers._parser_class())