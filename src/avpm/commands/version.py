from __future__ import annotations

from avpm import __version__


def run(args) -> int:
    print(__version__)
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "version",
        help="Show AVPM version",
    )

    parser.set_defaults(func=run)