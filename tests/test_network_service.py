from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from avpm.exceptions import NetworkError
from avpm.services.network import PUBLIC_IP_URL, fetch_public_ip


class FetchPublicIpTests(unittest.TestCase):
    @patch("avpm.services.network.urlopen")
    def test_returns_ipv4_address(self, urlopen) -> None:
        response = MagicMock()
        response.read.return_value = b'{"ip":"203.0.113.10"}'
        urlopen.return_value.__enter__.return_value = response

        result = fetch_public_ip()

        self.assertEqual(result, "203.0.113.10")
        urlopen.assert_called_once_with(PUBLIC_IP_URL, timeout=5.0)

    @patch("avpm.services.network.urlopen")
    def test_returns_ipv6_address(self, urlopen) -> None:
        response = MagicMock()
        response.read.return_value = b'{"ip":"2001:db8::1"}'
        urlopen.return_value.__enter__.return_value = response

        self.assertEqual(fetch_public_ip(), "2001:db8::1")

    @patch("avpm.services.network.urlopen")
    def test_rejects_invalid_response(self, urlopen) -> None:
        response = MagicMock()
        response.read.return_value = b'{"ip":"not-an-ip"}'
        urlopen.return_value.__enter__.return_value = response

        with self.assertRaisesRegex(
            NetworkError,
            "Unable to obtain public IP",
        ):
            fetch_public_ip()

    @patch("avpm.services.network.urlopen")
    def test_wraps_network_errors(self, urlopen) -> None:
        urlopen.side_effect = URLError("offline")

        with self.assertRaisesRegex(
            NetworkError,
            "Unable to obtain public IP",
        ):
            fetch_public_ip()
