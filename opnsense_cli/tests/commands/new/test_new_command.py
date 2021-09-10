import os
from unittest.mock import patch, Mock
from opnsense_cli.commands.new.command import command
from opnsense_cli.tests.commands.base import CommandTestCase
from click.testing import CliRunner
import textwrap


class TestNewCommandCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._core_model_fixture = self._read_fixture_file('new/command/core/model.xml')
        self._core_form_fixture = self._read_fixture_file('new/command/core/form.xml')
        self._plugin_model_fixture = self._read_fixture_file('new/command/plugin/model.xml')
        self._plugin_form_fixture = self._read_fixture_file('new/command/plugin/form.xml')

        self._mock_model_core_resp = self._mock_response(content=self._core_model_fixture)
        self._mock_form_core_resp = self._mock_response(content=self._core_form_fixture)
        self._mock_model_plugin_resp = self._mock_response(content=self._plugin_model_fixture)
        self._mock_form_plugin_resp = self._mock_response(content=self._plugin_form_fixture)

        self._command_template = self._read_template_file('code_generator/command/command.py.j2')
        self._facade_template = self._read_template_file('code_generator/command/command_facade.py.j2')
        self._test_template = self._read_template_file('code_generator/command/command.py.j2')

        self._output_dir = self._get_output_path('')
        self._generated_plugin_command_path = f"{self._output_dir}/commands/plugin/frontend.py"
        self._generated_plugin_facade_path = f"{self._output_dir}/facades/command/plugin/frontend.py"
        self._generated_plugin_test_path = f"{self._output_dir}/test/commands/plugin/test_haproxy_frontend.py"

        self._generated_core_command_path = f"{self._output_dir}/commands/core/category.py"
        self._generated_core_facade_path = f"{self._output_dir}/facades/command/core/category.py"
        self._generated_core_test_path = f"{self._output_dir}/test/commands/core/test_firewall_category.py"

    @patch('opnsense_cli.parser.xml.requests.get')
    def test_plugin(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_model_plugin_resp,
            self._mock_form_plugin_resp
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

        self.assertIn(
            f"generate new code: {self._generated_plugin_command_path}\n"
            f"generate new code: {self._generated_plugin_facade_path}\n"
            f"generate new code: {self._generated_plugin_test_path}\n",
            result.output
        )

        self.assertTrue(os.path.exists(self._generated_plugin_command_path))
        self.assertTrue(os.path.exists(self._generated_plugin_facade_path))
        self.assertTrue(os.path.exists(self._generated_plugin_test_path))

        command_file_content = self._read_file(self._generated_plugin_command_path)
        facade_file_content = self._read_file(self._generated_plugin_facade_path)
        test_file_content = self._read_file(self._generated_plugin_test_path)

        self.assertIn(
            "enabled,name,description,bind,bindOptions,mode,defaultBackend,ssl_enabled,ssl_certificates",
            command_file_content
        )

        self.assertIn(
            textwrap.dedent("""
                @click.option(
                    '--linkedCpuAffinityRules',
                    help=('Choose CPU affinity rules that should be applied to this Public Service.'),
                    show_default=True,
                    default=None
                )
            """),
            command_file_content
        )
        self.assertIn(
            textwrap.dedent("""
                @click.option(
                    '--linkedCpuAffinityRules',
                    help=('Choose CPU affinity rules that should be applied to this Public Service.'),
                    show_default=True,
                    default=None,
                    required=False,
                )
            """),
            command_file_content
        )

        self.assertIn(
            "class HaproxyFrontendFacade(HaproxyFacade):",
            facade_file_content
        )

        self.assertIn(
            "'defaultBackend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'Backend'},",
            facade_file_content
        )

        self.assertIn(
            "class TestHaproxyFrontendCommands(CommandTestCase):",
            test_file_content
        )

        self.assertIn(
            "@patch('opnsense_cli.commands.plugin.haproxy.frontend.ApiClient.execute')",
            test_file_content
        )

    @patch('opnsense_cli.parser.xml.requests.get')
    def test_plugin_without_form_url(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_model_plugin_resp,
        ]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                'plugin', 'haproxy', 'frontend', '--tag', 'frontends',
                '--model-url', 'https://fake.githubusercontent.com/model.xml',
            ],
            catch_exceptions=False
        )

        self.assertIn(
            f"generate new code: {self._generated_plugin_command_path}\n"
            f"generate new code: {self._generated_plugin_facade_path}\n"
            f"generate new code: {self._generated_plugin_test_path}\n",
            result.output
        )

        self.assertTrue(os.path.exists(self._generated_plugin_command_path))
        self.assertTrue(os.path.exists(self._generated_plugin_facade_path))
        self.assertTrue(os.path.exists(self._generated_plugin_test_path))

    @patch('opnsense_cli.parser.xml.requests.get')
    def test_core(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_model_core_resp,
            self._mock_form_core_resp
        ]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                'core', 'firewall', 'category', '--tag', 'categories',
                '--model-url', 'https://fake.githubusercontent.com/model.xml',
                '--form-url', 'https://fake.githubusercontent.com/form.xml'
            ],
            catch_exceptions=False
        )

        self.assertIn(
            f"generate new code: {self._generated_core_command_path}\n"
            f"generate new code: {self._generated_core_facade_path}\n"
            f"generate new code: {self._generated_core_test_path}\n",
            result.output
        )
