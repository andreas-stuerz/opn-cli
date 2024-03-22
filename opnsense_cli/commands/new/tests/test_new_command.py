import os
from unittest.mock import patch, Mock
from opnsense_cli.commands.new.command import command
from opnsense_cli.commands.test_base import CommandTestCase
from click.testing import CliRunner
import textwrap


class TestNewCommandCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._core_model_fixture = self._read_fixture_file(
            "fixtures/opn_cli/core_model.xml", base_dir=os.path.dirname(__file__)
        )
        self._core_form_fixture = self._read_fixture_file("fixtures/opn_cli/core_form.xml", base_dir=os.path.dirname(__file__))
        self._plugin_model_fixture = self._read_fixture_file(
            "fixtures/opn_cli/plugin_model.xml", base_dir=os.path.dirname(__file__)
        )
        self._plugin_form_fixture = self._read_fixture_file(
            "fixtures/opn_cli/plugin_form.xml", base_dir=os.path.dirname(__file__)
        )

        self._mock_model_core_resp = self._mock_response(content=self._core_model_fixture)
        self._mock_form_core_resp = self._mock_response(content=self._core_form_fixture)
        self._mock_model_plugin_resp = self._mock_response(content=self._plugin_model_fixture)
        self._mock_form_plugin_resp = self._mock_response(content=self._plugin_form_fixture)

        self._command_template = self._read_template_file("code_generators/opn_cli/command/template.py.j2")
        self._service_template = self._read_template_file("code_generators/opn_cli/service/template.py.j2")
        self._test_template = self._read_template_file("code_generators/opn_cli/unit_test/template.py.j2")

        self._output_dir = self._get_output_path()

        self._generated_plugin_command_path = f"{self._output_dir}/commands/plugin/haproxy/frontend.py"
        self._generated_plugin_service_path = (
            f"{self._output_dir}/commands/plugin/haproxy/services/haproxy_frontend_service.py"
        )
        self._generated_plugin_test_path = f"{self._output_dir}/commands/plugin/haproxy/tests/test_haproxy_frontend.py"

        self._generated_core_command_path = f"{self._output_dir}/commands/core/firewall/category.py"
        self._generated_core_service_path = f"{self._output_dir}/commands/core/firewall/services/firewall_category_service.py"
        self._generated_core_test_path = f"{self._output_dir}/commands/core/firewall/tests/test_firewall_category.py"

    @patch("opnsense_cli.parser.xml_parser.requests.get")
    def test_plugin(self, mock_model_get: Mock):
        mock_model_get.side_effect = [self._mock_model_plugin_resp, self._mock_form_plugin_resp]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                "plugin",
                "haproxy",
                "frontend",
                "--tag",
                "frontends",
                "--model-url",
                "https://fake.githubusercontent.com/model.xml",
                "--form-url",
                "https://fake.githubusercontent.com/form.xml",
            ],
            catch_exceptions=False,
        )

        self.assertIn(
            f"generate new code: {self._generated_plugin_command_path}\n"
            f"generate new code: {self._generated_plugin_service_path}\n"
            f"generate new code: {self._generated_plugin_test_path}\n",
            result.output,
        )

        self.assertTrue(os.path.exists(self._generated_plugin_command_path))
        self.assertTrue(os.path.exists(self._generated_plugin_service_path))
        self.assertTrue(os.path.exists(self._generated_plugin_test_path))

        command_file_content = self._read_file(self._generated_plugin_command_path)
        facade_file_content = self._read_file(self._generated_plugin_service_path)
        test_file_content = self._read_file(self._generated_plugin_test_path)

        self.assertIn(
            "enabled,name,description,bind,bindOptions,mode,defaultBackend,ssl_enabled,ssl_certificates", command_file_content
        )

        self.assertIn(
            textwrap.dedent(
                """
                @click.option(
                    '--linkedCpuAffinityRules',
                    help=('Choose CPU affinity rules that should be applied to this Public Service.'),
                    callback=resolve_linked_names_to_uuids,
                    type=CSV,
                    show_default=True,
                    default=None
                )
            """
            ),
            command_file_content,
        )
        self.assertIn(
            textwrap.dedent(
                """
                @click.option(
                    '--linkedCpuAffinityRules',
                    help=('Choose CPU affinity rules that should be applied to this Public Service.'),
                    callback=resolve_linked_names_to_uuids,
                    type=CSV,
                    show_default=True,
                    default=None,
                    required=False,
                )
            """
            ),
            command_file_content,
        )

        self.assertIn("class HaproxyFrontendService(CommandService):", facade_file_content)

        self.assertIn(
            "'defaultBackend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'Backend'},",
            facade_file_content,
        )

        self.assertIn("class TestHaproxyFrontendCommands(CommandTestCase):", test_file_content)

        self.assertIn("@patch('opnsense_cli.commands.plugin.haproxy.frontend.ApiClient.execute')", test_file_content)

    @patch("opnsense_cli.parser.xml_parser.requests.get")
    def test_plugin_without_form_url(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_model_plugin_resp,
        ]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                "plugin",
                "haproxy",
                "frontend",
                "--tag",
                "frontends",
                "--model-url",
                "https://fake.githubusercontent.com/model.xml",
            ],
            catch_exceptions=False,
        )

        self.assertIn(
            f"generate new code: {self._generated_plugin_command_path}\n"
            f"generate new code: {self._generated_plugin_service_path}\n"
            f"generate new code: {self._generated_plugin_test_path}\n",
            result.output,
        )

        self.assertTrue(os.path.exists(self._generated_plugin_command_path))
        self.assertTrue(os.path.exists(self._generated_plugin_service_path))
        self.assertTrue(os.path.exists(self._generated_plugin_test_path))

    @patch("opnsense_cli.parser.xml_parser.requests.get")
    def test_core(self, mock_model_get: Mock):
        mock_model_get.side_effect = [self._mock_model_core_resp, self._mock_form_core_resp]

        runner = CliRunner()
        result = runner.invoke(
            command,
            [
                "core",
                "firewall",
                "category",
                "--tag",
                "categories",
                "--model-url",
                "https://fake.githubusercontent.com/model.xml",
                "--form-url",
                "https://fake.githubusercontent.com/form.xml",
            ],
            catch_exceptions=False,
        )

        self.assertIn(
            f"generate new code: {self._generated_core_command_path}\n"
            f"generate new code: {self._generated_core_service_path}\n"
            f"generate new code: {self._generated_core_test_path}\n",
            result.output,
        )
