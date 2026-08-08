from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError
from avpm.services.locations import fastest_location


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        location = args.location

        if args.fastest:
            fastest = fastest_location(backend.locations())

            if fastest is None:
                raise BackendError("No VPN locations with known ping found")

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
    parser: ArgumentParser = subparsers.add_parser(
        "connect",
        help="Connect VPN",
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
        help="Connect to the location with the lowest ping",
    )

    parser.set_defaults(func=run)


def clean_connect_output(text: str) -> str:
    ignored = "Log is being written to:"

    return "\n".join(
        line for line in text.splitlines()
        if not line.startswith(ignored)
    ).strip()
