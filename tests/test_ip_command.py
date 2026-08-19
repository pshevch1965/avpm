from __future__ import annotations

import json
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from avpm.commands.ip import run


class IpCommandTests(unittest.TestCase):
    @patch("avpm.commands.ip.fetch_public_ip")
    def test_prints_public_ip(self, fetch_public_ip) -> None:
        fetch_public_ip.return_value = "203.0.113.10"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=False))

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "203.0.113.10\n")

    @patch("avpm.commands.ip.fetch_public_ip")
    def test_prints_json(self, fetch_public_ip) -> None:
        fetch_public_ip.return_value = "2001:db8::1"
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(json=True))

        self.assertEqual(result, 0)
        self.assertEqual(
            json.loads(output.getvalue()),
            {"ip": "2001:db8::1"},
        )
