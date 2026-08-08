from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO

from avpm.cli import main


class HelpCommandTests(unittest.TestCase):
    def test_help_prints_root_parser(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = main(["help"])

        help_text = output.getvalue()

        self.assertEqual(result, 0)
        self.assertIn("AVPM - AdGuard VPN Manager", help_text)
        self.assertIn("connect", help_text)
        self.assertIn("reconnect", help_text)
        self.assertIn("fastest", help_text)

    def test_no_command_prints_same_root_help(self) -> None:
        help_output = StringIO()
        default_output = StringIO()

        with redirect_stdout(help_output):
            help_result = main(["help"])

        with redirect_stdout(default_output):
            default_result = main([])

        self.assertEqual(help_result, 0)
        self.assertEqual(default_result, 0)
        self.assertEqual(help_output.getvalue(), default_output.getvalue())


if __name__ == "__main__":
    unittest.main()
