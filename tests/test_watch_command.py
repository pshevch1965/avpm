from __future__ import annotations

import argparse
import json
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from unittest.mock import patch

from avpm.commands.watch import (
    collect_snapshot,
    positive_float,
    positive_int,
    run,
)
from avpm.exceptions import BackendError
from avpm.models import VPNStatus


TIMESTAMP = datetime(2026, 8, 19, 12, 0, tzinfo=timezone.utc)


class CollectSnapshotTests(unittest.TestCase):
    def test_collects_connected_status(self) -> None:
        backend = unittest.mock.MagicMock()
        backend.status.return_value = VPNStatus(
            connected=True,
            location="STOCKHOLM",
            interface="tun0",
        )

        snapshot = collect_snapshot(backend, TIMESTAMP)

        self.assertTrue(snapshot["connected"])
        self.assertEqual(snapshot["location"], "STOCKHOLM")
        self.assertEqual(snapshot["interface"], "tun0")
        self.assertIsNone(snapshot["error"])

    def test_captures_backend_error(self) -> None:
        backend = unittest.mock.MagicMock()
        backend.status.side_effect = BackendError("Status failed")

        snapshot = collect_snapshot(backend, TIMESTAMP)

        self.assertFalse(snapshot["connected"])
        self.assertEqual(snapshot["error"], "Status failed")


class WatchCommandTests(unittest.TestCase):
    @patch("avpm.commands.watch.time.sleep")
    @patch("avpm.commands.watch.collect_snapshot")
    def test_stops_after_requested_count(self, collect, sleep) -> None:
        collect.side_effect = [
            {
                "timestamp": "first",
                "connected": True,
                "location": "TALLINN",
                "interface": "tun0",
                "error": None,
            },
            {
                "timestamp": "second",
                "connected": False,
                "location": None,
                "interface": None,
                "error": None,
            },
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(interval=0.5, count=2, json=False))

        self.assertEqual(result, 0)
        self.assertEqual(collect.call_count, 2)
        sleep.assert_called_once_with(0.5)
        self.assertIn("Connected", output.getvalue())
        self.assertIn("Disconnected", output.getvalue())

    @patch("avpm.commands.watch.collect_snapshot")
    def test_prints_json_lines(self, collect) -> None:
        collect.return_value = {
            "timestamp": "2026-08-19T12:00:00+00:00",
            "connected": True,
            "location": "KYIV",
            "interface": "tun0",
            "error": None,
        }
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(interval=1.0, count=1, json=True))

        payload = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(payload["location"], "KYIV")

    @patch("avpm.commands.watch.time.sleep", side_effect=KeyboardInterrupt)
    @patch("avpm.commands.watch.collect_snapshot")
    def test_ctrl_c_stops_cleanly(self, collect, sleep) -> None:
        collect.return_value = {
            "timestamp": "now",
            "connected": True,
            "location": "RIGA",
            "interface": "tun0",
            "error": None,
        }

        with redirect_stdout(StringIO()):
            result = run(Namespace(interval=2.0, count=None, json=False))

        self.assertEqual(result, 0)


class WatchArgumentTests(unittest.TestCase):
    def test_requires_positive_interval(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError):
            positive_float("0")

    def test_requires_positive_count(self) -> None:
        with self.assertRaises(argparse.ArgumentTypeError):
            positive_int("-1")
