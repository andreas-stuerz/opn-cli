import unittest
from click.testing import CliRunner
from opnsense_cli.commands.plugin.apibackup import apibackup


class TestApibackupCommands(unittest.TestCase):
    def test_firewall(self):
        runner = CliRunner()
        result = runner.invoke(apibackup)

        self.assertEqual(0, result.exit_code)
