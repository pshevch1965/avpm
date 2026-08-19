from __future__ import annotations

import argparse
from dataclasses import asdict

from avpm.backends.adguard import AdGuardBackend
from avpm.commands.locations import non_negative_int
from avpm.services.locations import filter_locations, search_locations
from avpm.ui import print_json, print_locations


def run(args: argparse.Namespace) -> int:
    backend = AdGuardBackend()
    locations = search_locations(backend.locations(), args.query)
    locations = filter_locations(locations, max_ping=args.max_ping)

    if args.json:
        print_json([asdict(location) for location in locations])
        return 0

    if not locations:
        print("No VPN locations matched query.")
        return 0

    print_locations(locations)
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "find",
        help="Search VPN locations",
    )

    parser.add_argument(
        "query",
        help="ISO code, country, or city",
    )

    parser.add_argument(
        "--max-ping",
        type=non_negative_int,
        help="Show locations with ping up to this value",
    )

    output_group = parser.add_mutually_exclusive_group()

    output_group.add_argument(
        "--json",
        action="store_true",
        help="Print locations as JSON",
    )

    output_group.add_argument(
        "--text",
        action="store_true",
        help="Force plain-text output",
    )

    parser.set_defaults(func=run)
