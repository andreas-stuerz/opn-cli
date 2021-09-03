import unittest
from click.testing import CliRunner
from opnsense_cli.commands.new import new


class TestNewCommands(unittest.TestCase):
    def test_new(self):
        runner = CliRunner()
        result = runner.invoke(new)

        self.assertEqual(0, result.exit_code)
