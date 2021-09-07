import unittest
from click.testing import CliRunner
from opnsense_cli.commands.core.firewall import firewall


class TestFirewallCommands(unittest.TestCase):
    def test_firewall(self):
        runner = CliRunner()
        result = runner.invoke(firewall)

        self.assertEqual(0, result.exit_code)
