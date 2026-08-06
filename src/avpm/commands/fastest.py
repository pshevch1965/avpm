from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.ui import print_locations
from avpm.services.locations import sort_by_ping


def run(args: Namespace) -> int:
    backend = AdGuardBackend()


    try:
        locations = backend.locations()
    except BackendError as exc:
        print(f"ERROR: {exc}")
        return 1

    locations = sort_by_ping(
        backend.locations(),
    )

    limit = args.count or 10

    print_locations(
        locations[:limit],
        title=f"Top {limit} fastest locations",
    )

    return 0


def register(subparsers):
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

    parser.set_defaults(func=run)