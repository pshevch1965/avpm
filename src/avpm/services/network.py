from __future__ import annotations

import ipaddress
import json
import socket
from urllib.error import URLError
from urllib.request import urlopen

from avpm.exceptions import NetworkError


PUBLIC_IP_URL = "https://api64.ipify.org?format=json"


def interface_exists(name: str) -> bool:
    """Return whether a network interface exists on this system."""
    try:
        return name in {
            interface_name
            for _, interface_name in socket.if_nameindex()
        }
    except OSError:
        return False


def fetch_public_ip(timeout: float = 5.0) -> str:
    """Return the current public IPv4 or IPv6 address."""
    try:
        with urlopen(PUBLIC_IP_URL, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))

        return str(ipaddress.ip_address(payload["ip"]))
    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        TimeoutError,
        URLError,
    ) as exc:
        raise NetworkError("Unable to obtain public IP") from exc
