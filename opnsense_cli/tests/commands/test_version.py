import unittest

from click.testing import CliRunner
from opnsense_cli.commands.version import version
from opnsense_cli import __cli_name__, __version__


class TestVersionCommands(unittest.TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(version)

        self.assertIn(f"{__cli_name__} v{__version__}\n", result.output)
        self.assertEqual(0, result.exit_code)
