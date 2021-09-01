import unittest
from click.testing import CliRunner
from opnsense_cli.commands.plugin.haproxy import haproxy


class TestHaproxyCommands(unittest.TestCase):
    def test_firewall(self):
        runner = CliRunner()
        result = runner.invoke(haproxy)

        self.assertEqual(0, result.exit_code)
