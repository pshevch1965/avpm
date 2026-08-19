from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.toggle import run
from avpm.models import VPNStatus


class ToggleCommandTests(unittest.TestCase):
    @patch("avpm.commands.toggle.AdGuardBackend")
    def test_disconnects_when_connected(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.status.return_value = VPNStatus(connected=True)
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace())

        self.assertEqual(result, 0)
        backend.disconnect.assert_called_once_with()
        backend.connect.assert_not_called()
        self.assertEqual(output.getvalue(), "VPN disconnected.\n")

    @patch("avpm.commands.toggle.AdGuardBackend")
    def test_connects_when_disconnected(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.status.return_value = VPNStatus(connected=False)
        backend.connect.return_value = "Successfully Connected to TALLINN"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace())

        self.assertEqual(result, 0)
        backend.connect.assert_called_once_with()
        backend.disconnect.assert_not_called()
        self.assertEqual(
            output.getvalue(),
            "Successfully Connected to TALLINN\n",
        )

    @patch("avpm.commands.toggle.AdGuardBackend")
    def test_cleans_connect_output(self, backend_class) -> None:
        backend = backend_class.return_value
        backend.status.return_value = VPNStatus(connected=False)
        backend.connect.return_value = (
            "Log is being written to: /tmp/adguard.log\n"
            "Successfully Connected to KYIV"
        )
        output = StringIO()

        with redirect_stdout(output):
            run(Namespace())

        self.assertEqual(
            output.getvalue(),
            "Successfully Connected to KYIV\n",
        )


if __name__ == "__main__":
    unittest.main()
