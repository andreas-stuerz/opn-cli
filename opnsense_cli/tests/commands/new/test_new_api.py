import os
from unittest.mock import patch, Mock
from opnsense_cli.commands.new.api import api
from opnsense_cli.tests.commands.base import CommandTestCase
from click.testing import CliRunner
import textwrap


class TestNewCommandApi(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._core_html_fixture = self._read_fixture_file('new/api/core/core.html')
        self._plugin_html_fixture = self._read_fixture_file('new/api/plugin/plugin.html')
        self._list_core_html_fixture = self._read_fixture_file('new/api/list/core.html')
        self._list_plugin_html_fixture = self._read_fixture_file('new/api/list/plugin.html')

        self._mock_html_core_resp = self._mock_response(content=self._core_html_fixture)
        self._mock_html_plugin_resp = self._mock_response(content=self._plugin_html_fixture)
        self._mock_module_list_core_resp = self._mock_response(content=self._list_core_html_fixture)
        self._mock_module_list_plugin_resp = self._mock_response(content=self._list_plugin_html_fixture)

        self._command_template = self._read_template_file('code_generator/api/api.py.j2')

        self._output_dir = self._get_output_path('')
        self._generated_plugin_api_path = f"{self._output_dir}/api/plugins/haproxy.py"
        self._generated_core_api_path = f"{self._output_dir}/api/core/cron.py"

    @patch('opnsense_cli.parser.html.requests.get')
    def test_plugin(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_module_list_plugin_resp,
            self._mock_html_plugin_resp
        ]

        runner = CliRunner()
        result = runner.invoke(
            api,
            [
                'plugin', 'haproxy',
                '--api-reference-url', 'https://fake.githubusercontent.com/plugin.html'
            ],
            catch_exceptions=False
        )
        self.assertIn(
            f"generate new code: {self._generated_plugin_api_path}\n",
            result.output
        )

        self.assertTrue(os.path.exists(self._generated_plugin_api_path))

        api_plugin_file_content = self._read_file(self._generated_plugin_api_path)

        self.assertIn(
            'self.method = "get"',
            api_plugin_file_content
        )

        self.assertIn(
            'self.method = "post"',
            api_plugin_file_content
        )

        self.assertIn(
            "@ApiBase._api_call",
            api_plugin_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Export(ApiBase):
                MODULE = "haproxy"
                CONTROLLER = "export"
                """
                Haproxy ExportController
                """
            '''),
            api_plugin_file_content
        )

        self.assertIn(
            "def diff(self, *args):",
            api_plugin_file_content
        )

        self.assertIn(
            'self.command = "diff"',
            api_plugin_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Maintenance(ApiBase):
                MODULE = "haproxy"
                CONTROLLER = "maintenance"
                """
                Haproxy MaintenanceController
                """
            '''),
            api_plugin_file_content
        )

        self.assertIn(
            "def certActions(self, *args):",
            api_plugin_file_content
        )

        self.assertIn(
            'self.command = "certActions"',
            api_plugin_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Service(ApiBase):
                MODULE = "haproxy"
                CONTROLLER = "service"
                """
                Haproxy ServiceController
                """
            '''),
            api_plugin_file_content
        )

        self.assertIn(
            "def configtest(self, *args):",
            api_plugin_file_content
        )

        self.assertIn(
            'self.command = "configtest"',
            api_plugin_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Settings(ApiBase):
                MODULE = "haproxy"
                CONTROLLER = "settings"
                """
                Haproxy SettingsController
                """
            '''),
            api_plugin_file_content
        )

        self.assertIn(
            "def addAcl(self, *args):",
            api_plugin_file_content
        )

        self.assertIn(
            'self.command = "addAcl"',
            api_plugin_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Statistics(ApiBase):
                MODULE = "haproxy"
                CONTROLLER = "statistics"
                """
                Haproxy StatisticsController
                """
            '''),
            api_plugin_file_content
        )

        self.assertIn(
            "def counters(self, *args):",
            api_plugin_file_content
        )

        self.assertIn(
            'self.command = "counters"',
            api_plugin_file_content
        )

    @patch('opnsense_cli.parser.html.requests.get')
    def test_core(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_module_list_core_resp,
            self._mock_html_core_resp
        ]

        runner = CliRunner()
        result = runner.invoke(
            api,
            [
                'core', 'cron',
                '--api-reference-url', 'https://fake.githubusercontent.com/core.html'
            ],
            catch_exceptions=False
        )

        self.assertIn(
            f"generate new code: {self._generated_core_api_path}\n",
            result.output
        )

        self.assertTrue(os.path.exists(self._generated_core_api_path))

        api_core_file_content = self._read_file(self._generated_core_api_path)

        self.assertIn(
            'self.method = "get"',
            api_core_file_content
        )

        self.assertIn(
            'self.method = "post"',
            api_core_file_content
        )

        self.assertIn(
            "@ApiBase._api_call",
            api_core_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Service(ApiBase):
                MODULE = "cron"
                CONTROLLER = "service"
                """
                Cron ServiceController
                """
            '''),
            api_core_file_content
        )

        self.assertIn(
            "def reconfigure(self, *args):",
            api_core_file_content
        )

        self.assertIn(
            'self.command = "reconfigure"',
            api_core_file_content
        )

        self.assertIn(
            textwrap.dedent('''
            class Settings(ApiBase):
                MODULE = "cron"
                CONTROLLER = "settings"
                """
                Cron SettingsController
                """
            '''),
            api_core_file_content
        )

        self.assertIn(
            "def addJob(self, *args):",
            api_core_file_content
        )

        self.assertIn(
            'self.command = "addJob"',
            api_core_file_content
        )

    @patch('opnsense_cli.parser.html.requests.get')
    def test_list(self, mock_model_get: Mock):
        mock_model_get.side_effect = [
            self._mock_module_list_core_resp,
        ]

        runner = CliRunner()
        result_core = runner.invoke(
            api,
            [
                'list', '--module-type', 'core',
                '--base-url', 'https://fake.githubusercontent.com/module/core.html'
            ],
            catch_exceptions=False
        )
        self.assertIn(
            "cron",
            result_core.output
        )

        self.assertIn(
            "ipsec",
            result_core.output
        )

        self.assertIn(
            "syslog",
            result_core.output
        )

        mock_model_get.side_effect = [
            self._mock_module_list_plugin_resp,
        ]

        runner = CliRunner()
        result_plugin = runner.invoke(
            api,
            [
                'list', '--module-type', 'plugin',
                '--base-url', 'https://fake.githubusercontent.com/module/plugin.html'
            ],
            catch_exceptions=False
        )
        self.assertIn(
            "haproxy",
            result_plugin.output
        )

        self.assertIn(
            "postfix",
            result_plugin.output
        )

        self.assertIn(
            "zabbixagent",
            result_plugin.output
        )
