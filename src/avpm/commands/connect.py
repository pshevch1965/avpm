from argparse import ArgumentParser, Namespace

from avpm.backends.adguard import AdGuardBackend


def run(args: Namespace) -> int:
    backend = AdGuardBackend()

    try:
        output = backend.connect(args.location)
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

    parser.add_argument(
        "location",
        nargs="?",
        help="ISO code or city name",
    )

    parser.set_defaults(func=run)

def clean_connect_output(text: str) -> str:
    ignored = "Log is being written to:"

    return "\n".join(
        line for line in text.splitlines()
        if not line.startswith(ignored)
    ).strip()