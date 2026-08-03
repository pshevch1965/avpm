from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.backend import BackendError


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        backend.connect(args.location)
        return 0
    except BackendError as exc:
        print(f"ERROR: {exc}")
        return 1


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "connect",
        help="Connect VPN",
    )

    parser.add_argument(
        "location",
        nargs="?",
        help="ISO code or city name",
    )

    parser.set_defaults(func=run)