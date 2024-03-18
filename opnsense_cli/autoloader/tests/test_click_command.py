from unittest import TestCase
from click.core import Command as ClickCommand
from opnsense_cli.autoloader.click_command import ClickCommandAutoloader
from opnsense_cli.cli import cli
from unittest.mock import patch
import os


class TestClickCommandAutoloader(TestCase):
    def setUp(self):
        self._autoloader = ClickCommandAutoloader(cli)
        self._script_dir = os.path.dirname(os.path.realpath(__file__))
        self._commands_dir = f"{self._script_dir}/../../opnsense_cli/commands"

    @patch("opnsense_cli.autoloader.click_command.os.walk")
    def test_autoload_commands(self, os_walk_mock):
        os_walk_mock.return_value = [
            (f"{self._commands_dir}/version", ["__pycache__"], ["__init__.py"]),
            (f"{self._commands_dir}/version/__pycache__", [], ["__init__"]),
        ]
        result = self._autoloader.autoload("opnsense_cli.commands.version")

        self.assertIsInstance(result, ClickCommand)
