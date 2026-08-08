from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.commands.connect import clean_connect_output
from avpm.exceptions import BackendError


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        if args.if_needed and backend.status().connected:
            print("VPN is already connected.")
            return 0

        output = backend.connect(args.location)
        print(clean_connect_output(output))
        return 0
    except BackendError as exc:
        print(f"ERROR: {exc}")
        return 1


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "reconnect",
        help="Reconnect VPN",
    )

    parser.add_argument(
        "location",
        nargs="?",
        help="ISO code or city name",
    )

    parser.add_argument(
        "--if-needed",
        action="store_true",
        help="Connect only when VPN is disconnected",
    )

    parser.set_defaults(func=run)
