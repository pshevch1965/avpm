from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError
from avpm.services.locations import filter_locations, sort_by_ping
from avpm.ui import print_locations


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        locations = backend.locations()
    except BackendError as exc:
        print(f"ERROR: {exc}")
        return 1

    locations = sort_by_ping(
        filter_locations(
            locations,
            country=args.country,
        )
    )

    if not locations:
        print("No VPN locations matched filters.")
        return 0

    limit = args.count

    title = f"Top {limit} fastest locations"

    if args.country:
        title += f" in {args.country}"

    print_locations(
        locations[:limit],
        title=title,
    )

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "fastest",
        help="Show fastest VPN locations",
    )

    parser.add_argument(
        "count",
        nargs="?",
        type=int,
        default=10,
        help="Number of locations to show",
    )

    parser.add_argument(
        "-c",
        "--country",
        help="Filter by country name or ISO code",
    )

    parser.set_defaults(func=run)
