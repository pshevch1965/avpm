from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from avpm.services.support import create_support_archive


def run(args: Namespace) -> int:
    output = Path(args.output) if args.output else None
    archive = create_support_archive(
        output,
        include_logs=args.include_logs,
    )
    print(f"Support archive: {archive}")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "support",
        help="Create a diagnostic support archive",
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Output archive path",
    )

    parser.add_argument(
        "--include-logs",
        action="store_true",
        help="Include raw AdGuard VPN logs (may contain sensitive data)",
    )

    parser.set_defaults(func=run)
