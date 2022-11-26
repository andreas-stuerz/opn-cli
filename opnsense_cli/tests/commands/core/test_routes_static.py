from unittest.mock import patch, Mock
from opnsense_cli.commands.core.route.static import static
from opnsense_cli.tests.commands.base import CommandTestCase


class TestRoutesStaticCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_reconfigure_OK = {
            "status": "ok"
        }
        self._api_data_fixtures_reconfigure_FAILED = {
            "status": "failed"
        }
        self._api_data_fixtures_configtest_OK = {
            "result": "Configuration file is valid\n\n\n"
        }
        self._api_data_fixtures_configtest_FAILED = {
            "result": "Configuration file is invalid\n\n\n"
        }
        self._api_data_fixtures_create_OK = {
            "result": "saved",
            "uuid": "85282721-934c-42be-ba4d-a93cbfda26af"
        }
        self._api_data_fixtures_create_ERROR = {
            "result": "failed",
            "validations": {
                'route.gateway': ['Specify a valid gateway from the list matching the networks ip protocol.'],
                'route.network': 'Specify a valid network matching the gateways ip protocol.'
            }
        }
        self._api_data_fixtures_update_OK = {
            "result": "saved"
        }
        self._api_data_fixtures_update_NOT_EXISTS = {
            "result": "failed"
        }
        self._api_data_fixtures_delete_NOT_FOUND = {
            "result": "not found"
        }
        self._api_data_fixtures_delete_OK = {
            "result": "deleted"
        }
        self._api_data_fixtures_list_EMPTY = {
            "route": {
                "route": []
            }
        }
        self._api_data_fixtures_list = self._read_json_fixture('core/route/model_data.json')
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            static,
            [
                'list', '-o', 'plain', '-c',
                'network,gateway'
            ]
        )

        self.assertIn(
            (
                "10.50.2.2/24 Null4\n10.0.0.98/24 WAN_DHCP\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            static,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            static,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            static,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            static,
            [
                'show', '7905f696-4692-47aa-b39f-1a8cda5d60c1', '-o', 'plain', '-c',
                'network,gateway,descr,disabled'
            ]
        )

        self.assertIn(
            (
                "10.0.0.98/24 WAN_DHCP Test route 2 0\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "create",
                "--network", "10.0.5.1/24",
                "--gateway", "Null4"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "create",
                "--network", "10.0.5.1/24",
                "--gateway", "Null5"
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': "
                "{'route.gateway': ['Specify a valid gateway from the list matching the networks ip protocol.'], "
                "'route.network': 'Specify a valid network matching the gateways ip protocol.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_create_APPLY_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_FAILED,
            ],
            static,
            [
                "create",
                "--network", "10.0.5.1/24",
                "--gateway", "Null4"
            ]
        )

        self.assertIn(
            (
                "Error: Apply failed: {'status': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "update", "7905f696-4692-47aa-b39f-1a8cda5d60c1",
                "--disabled",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "update", "99282721-934c-42be-ba4d-a93cbfda2644",
                "--no-disabled",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "delete", "85282721-934c-42be-ba4d-a93cbfda26af",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_reconfigure_OK,
            ],
            static,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
