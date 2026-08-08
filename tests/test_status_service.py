from __future__ import annotations

import unittest

from avpm.services.status import is_connected


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


if __name__ == "__main__":
    unittest.main()
