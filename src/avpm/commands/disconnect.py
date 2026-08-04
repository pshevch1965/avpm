from argparse import ArgumentParser

from avpm.commands.off import run


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "disconnect",
        help="Disconnect VPN",
    )

    parser.set_defaults(func=run)