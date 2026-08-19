from __future__ import annotations

from argparse import Namespace

from avpm.backends.adguard import AdGuardBackend
from avpm.exceptions import BackendError, NetworkError
from avpm.models import VPNStatus
from avpm.services.network import fetch_public_ip, interface_exists
from avpm.ui import print_json


def run(args: Namespace) -> int:
    errors: dict[str, str] = {}

    try:
        status = AdGuardBackend().status()
    except BackendError as exc:
        status = VPNStatus(connected=False)
        errors["vpn"] = str(exc)

    try:
        public_ip = fetch_public_ip()
    except NetworkError as exc:
        public_ip = None
        errors["public_ip"] = str(exc)

    interface_up = bool(
        status.interface
        and interface_exists(status.interface)
    )
    healthy = bool(
        status.connected
        and interface_up
        and public_ip
        and not errors
    )

    payload = {
        "healthy": healthy,
        "connected": status.connected,
        "location": status.location,
        "interface": status.interface,
        "interface_up": interface_up,
        "public_ip": public_ip,
        "errors": errors,
    }

    if args.json:
        print_json(payload)
    else:
        print_health(payload)

    return 0 if healthy else 1


def print_health(payload: dict[str, object]) -> None:
    errors = payload["errors"]
    location = payload["location"] or "unknown location"
    interface = payload["interface"] or "-"
    public_ip = payload["public_ip"] or "-"

    if "vpn" in errors:
        vpn_value = f"ERROR ({errors['vpn']})"
    elif payload["connected"]:
        vpn_value = f"OK (connected to {location})"
    else:
        vpn_value = "DOWN (disconnected)"

    if payload["interface_up"]:
        interface_value = f"OK ({interface})"
    elif payload["interface"]:
        interface_value = f"NOT FOUND ({interface})"
    else:
        interface_value = "-"

    if "public_ip" in errors:
        ip_value = f"ERROR ({errors['public_ip']})"
    else:
        ip_value = f"OK ({public_ip})"

    print("AVPM Health")
    print()
    print(f"{'VPN':<15}: {vpn_value}")
    print(f"{'Interface':<15}: {interface_value}")
    print(f"{'Public IP':<15}: {ip_value}")
    print()
    result = "Healthy" if payload["healthy"] else "Problems detected"
    print(f"{'Result':<15}: {result}")


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "health",
        help="Check VPN connection health",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print health report as JSON",
    )

    parser.set_defaults(func=run)
