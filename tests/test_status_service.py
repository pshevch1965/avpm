from __future__ import annotations

import unittest

from avpm.services.status import extract_location, is_connected


class IsConnectedTests(unittest.TestCase):
    def test_connected_status(self) -> None:
        status = "Connected to KYIV in TUN mode, running on tun0"

        self.assertTrue(is_connected(status))

    def test_disconnected_status(self) -> None:
        status = "VPN is disconnected"

        self.assertFalse(is_connected(status))

    def test_is_case_insensitive(self) -> None:
        self.assertTrue(is_connected("CONNECTED to RIGA"))

    def test_unrecognized_status_is_not_connected(self) -> None:
        self.assertFalse(is_connected("VPN service is starting"))


class ExtractLocationTests(unittest.TestCase):
    def test_extracts_connected_location(self) -> None:
        status = "Connected to NEW YORK in TUN mode, running on tun0"

        self.assertEqual(extract_location(status), "NEW YORK")

    def test_returns_none_when_disconnected(self) -> None:
        self.assertIsNone(extract_location("VPN is disconnected"))


if __name__ == "__main__":
    unittest.main()
