import os
from unittest.mock import patch, Mock
from opnsense_cli.commands.new.command import command
from opnsense_cli.tests.commands.base import CommandTestCase
from click.testing import CliRunner


class TestNewCommandCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._plugin_model_fixture = self._read_fixture_file('new/command/plugin/model.xml')
        self._mock_model_resp = self._mock_response(content=self._plugin_model_fixture)

        self._plugin_form_fixture = self._read_fixture_file('new/command/plugin/form.xml')
        self._mock_form_resp = self._mock_response(content=self._plugin_form_fixture)

        self._command_template = self._read_template_file('code_generator/command/command.py.j2')
        self._facade_template = self._read_template_file('code_generator/command/command_facade.py.j2')
        self._test_template = self._read_template_file('code_generator/command/command.py.j2')

        self._output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../output'))
        self._generated_command_path = f"{self._output_dir}/commands/plugin/frontend.py"
        self._generated_facade_path = f"{self._output_dir}/facades/command/plugin/frontend.py"
        self._generated_test_path = f"{self._output_dir}/test/commands/plugin/test_haproxy_frontend.py"

    @patch('opnsense_cli.parser.xml.requests.get')
    def test_plugin(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_model_resp,
            self._mock_form_resp
        ]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                'plugin', 'haproxy', 'frontend', '--tag', 'frontends',
                '--model-url', 'https://fake.githubusercontent.com/model.xml',
                '--form-url', 'https://fake.githubusercontent.com/form.xml'
            ],
            catch_exceptions=False
        )
        self._show_fakefs_contents()
        self.assertIn(
            f"generate new code: {self._generated_command_path}\n"
            f"generate new code: {self._generated_facade_path}\n"
            f"generate new code: {self._generated_test_path}\n",
            result.output
        )

        self.assertTrue(os.path.exists(self._generated_command_path))
        self.assertTrue(os.path.exists(self._generated_facade_path))
        self.assertTrue(os.path.exists(self._generated_test_path))

    @patch('opnsense_cli.parser.xml.requests.get')
    def test_plugin_without_form_url(self, mock_model_get: Mock):
        pass
