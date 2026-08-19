from __future__ import annotations

import argparse
import json
import sys
import time
from argparse import Namespace
from datetime import datetime, timezone

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError


def positive_float(value: str) -> float:
    number = float(value)

    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")

    return number


def positive_int(value: str) -> int:
    number = int(value)

    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")

    return number


def collect_snapshot(
    backend: AdGuardBackend,
    timestamp: datetime | None = None,
) -> dict[str, object]:
    updated_at = timestamp or datetime.now(timezone.utc)

    try:
        status = backend.status()
        return {
            "timestamp": updated_at.isoformat(),
            "connected": status.connected,
            "location": status.location,
            "interface": status.interface,
            "error": None,
        }
    except BackendError as exc:
        return {
            "timestamp": updated_at.isoformat(),
            "connected": False,
            "location": None,
            "interface": None,
            "error": str(exc),
        }


def print_snapshot(snapshot: dict[str, object]) -> None:
    if snapshot["error"]:
        state = f"ERROR ({snapshot['error']})"
    elif snapshot["connected"]:
        state = "Connected"
    else:
        state = "Disconnected"

    print("AVPM Watch — Ctrl+C to stop")
    print()
    print(f"{'Updated':<12}: {snapshot['timestamp']}")
    print(f"{'State':<12}: {state}")
    print(f"{'Location':<12}: {snapshot['location'] or '-'}")
    print(f"{'Interface':<12}: {snapshot['interface'] or '-'}")


def run(args: Namespace) -> int:
    backend = AdGuardBackend()
    updates = 0

    try:
        while args.count is None or updates < args.count:
            snapshot = collect_snapshot(backend)

            if args.json:
                print(json.dumps(snapshot, ensure_ascii=False), flush=True)
            else:
                if sys.stdout.isatty():
                    print("\033[2J\033[H", end="")
                print_snapshot(snapshot)

            updates += 1

            if args.count is not None and updates >= args.count:
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        if not args.json:
            print()

    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "watch",
        help="Watch VPN connection status",
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=positive_float,
        default=2.0,
        help="Refresh interval in seconds (default: 2)",
    )

    parser.add_argument(
        "-n",
        "--count",
        type=positive_int,
        help="Stop after this many updates",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print newline-delimited JSON",
    )

    parser.set_defaults(func=run)
