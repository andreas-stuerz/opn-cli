from unittest.mock import patch, Mock
from opnsense_cli.commands.plugin.node_exporter.config import config
from opnsense_cli.tests.commands.base import CommandTestCase


class TestNodeExporterCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_reconfigure_OK = {
            "status": "ok"
        }
        self._api_data_fixtures_reconfigure_FAILED = {
            "status": "failed"
        }
        self._api_data_fixtures_edit_ERROR = {
            "result": "failed",
            "validations": {
                'general.listenport': 'Please provide a valid port number between 1 and 65535. Port 9100 is the default.'
            }
        }
        self._api_data_fixtures_update_OK = {
            "result": "saved"
        }

        self._api_data_fixtures_list = self._read_json_fixture('plugin/node_exporter/model_data.json')
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.plugin.node_exporter.config.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        print(self._api_data_fixtures_list)
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            config,
            [
                'show', '-o', 'plain'
            ]
        )

        self.assertIn(
            (
                "0 0.0.0.0 9100 1 1 1 1 1 1 1 1 0 0 0\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.node_exporter.config.ApiClient.execute')
    def test_edit_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            config,
            [
                "edit",
                "--listenport", "9101",
                "--listenaddress", "127.0.0.1",
                "--enabled",
                "--cpu",
                "--no-filesystem"

            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.node_exporter.config.ApiClient.execute')
    def test_edit_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_edit_ERROR,
            ],
            config,
            [
                "edit",
                "--listenport", "-1000",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': {'general.listenport': "
                "'Please provide a valid port number between 1 and 65535. Port 9100 is the default.'}}\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.node_exporter.config.ApiClient.execute')
    def test_edit_APPLY_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_FAILED,
            ],
            config,
            [
                "edit",
                "--listenport", "9101",
                "--listenaddress", "127.0.0.1",
                "--enabled",
                "--cpu",
                "--no-filesystem"
            ]
        )

        self.assertIn(
            (
                "Error: Apply failed: {'status': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)
