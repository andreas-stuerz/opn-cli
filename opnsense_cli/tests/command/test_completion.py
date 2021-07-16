import unittest

from click.testing import CliRunner
from opnsense_cli.commands.completion import completion


class TestCompletionCommands(unittest.TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(completion)

        self.assertEqual(0, result.exit_code)
