from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        locations = backend.locations()
    except BackendError as exc:
        print(f"ERROR: {exc}")
        return 1

    locations.sort(key=lambda loc: loc.ping)

    limit = args.count or 10

    print(f"Top {limit} fastest locations\n")

    print(f"{'ISO':<4} {'Country':<22} {'City':<30} {'Ping'}")
    print("-" * 65)

    for loc in locations[:limit]:
        print(
            f"{loc.iso:<4} "
            f"{loc.country:<22} "
            f"{loc.city:<30} "
            f"{loc.ping}"
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