from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.commands.connect import clean_connect_output
from avpm.exceptions import BackendError
from avpm.services.connection import get_fastest_location


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        if args.country and not args.fastest:
            raise BackendError("--country requires --fastest")

        if args.if_needed and backend.status().connected:
            print("VPN is already connected.")
            return 0

        location = args.location

        if args.fastest:
            fastest = get_fastest_location(
                backend,
                country=args.country,
            )
            location = fastest.city
            print(
                "Fastest location: "
                f"{fastest.city}, {fastest.country} ({fastest.ping} ms)"
            )

        output = backend.connect(location)
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

    location_group = parser.add_mutually_exclusive_group()

    location_group.add_argument(
        "location",
        nargs="?",
        help="ISO code or city name",
    )

    location_group.add_argument(
        "-f",
        "--fastest",
        action="store_true",
        help="Reconnect to the location with the lowest ping",
    )

    parser.add_argument(
        "-c",
        "--country",
        help="Limit fastest-location selection by country name or ISO code",
    )

    parser.add_argument(
        "--if-needed",
        action="store_true",
        help="Connect only when VPN is disconnected",
    )

    parser.set_defaults(func=run)
