from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from avpm.commands.support import run


class SupportCommandTests(unittest.TestCase):
    @patch("avpm.commands.support.create_support_archive")
    def test_creates_archive_at_requested_path(self, create_archive) -> None:
        create_archive.return_value = Path("/tmp/support.zip")
        output = StringIO()

        with redirect_stdout(output):
            result = run(
                Namespace(output="report.zip", include_logs=False)
            )

        self.assertEqual(result, 0)
        create_archive.assert_called_once_with(
            Path("report.zip"),
            include_logs=False,
        )
        self.assertEqual(
            output.getvalue(),
            "Support archive: /tmp/support.zip\n",
        )
