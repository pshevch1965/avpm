from __future__ import annotations

import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO

from avpm.commands.completion import run


class CompletionCommandTests(unittest.TestCase):
    def test_generates_bash_completion(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(shell="bash"))

        script = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("complete -F _vpn_completion vpn", script)
        self.assertIn("--if-needed", script)
        self.assertIn("--json", script)

    def test_generates_zsh_completion(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            result = run(Namespace(shell="zsh"))

        script = output.getvalue()
        self.assertEqual(result, 0)
        self.assertTrue(script.startswith("#compdef vpn"))
        self.assertIn("'completion:Generate shell completion'", script)
        self.assertIn("--country:Filter by country", script)
        self.assertIn("_describe 'option' options", script)


if __name__ == "__main__":
    unittest.main()
