from unittest.mock import patch, Mock
from opnsense_cli.commands.core.syslog.destination import destination
from opnsense_cli.tests.commands.base import CommandTestCase


class TestSyslogDestinationCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_reconfigure_OK = {
            "status": "ok"
        }
        self._api_data_fixtures_reconfigure_FAILED = {
            "status": "failed"
        }
        self._api_data_fixtures_create_OK = {
            "result": "saved",
            "uuid": "85282721-934c-42be-ba4d-a93cbfda26af"
        }
        self._api_data_fixtures_create_ERROR = {
            "result": "failed",
            "validations": {'destination.program': 'Specify valid source applications.'}
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
            "syslog": {
                "destinations": {
                    "destination": []
                }
            }
        }
        self._api_data_fixtures_list = self._read_json_fixture('core/syslog/model_data.json')
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            destination,
            [
                'list', '-o', 'plain', '-c',
                'uuid,enabled,transport,program'
            ]
        )

        self.assertIn(
            (
                "4dd6f818-e975-4136-bf7e-ed2559675ef9 1 tcp4 firewall,charon,lighttpd,ntp\n"
                "7155fe8c-d878-4690-be73-e9811a7c7da4 1 udp4 configd.py\n"
                "c5d77479-0875-4f92-977a-05b3c23aceea 1 udp4 audit,openvpn\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            destination,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            destination,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            destination,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            destination,
            [
                'show', '4dd6f818-e975-4136-bf7e-ed2559675ef9', '-o', 'plain', '-c',
                'uuid,enabled,transport,program'
            ]
        )

        self.assertIn(
            (
                "4dd6f818-e975-4136-bf7e-ed2559675ef9 1 tcp4 firewall,charon,lighttpd,ntp\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            destination,
            [
                "create",
                "--hostname", "10.0.0.1"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_FAILED,
            ],
            destination,
            [
                "create",
                "--hostname", "xyz_something_strange",
                "--program", "doesnotexists"
            ],
        )

        self.assertIn(
            (
                "Error: Apply failed: {'status': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            destination,
            [
                "update", "7155fe8c-d878-4690-be73-e9811a7c7da4",
                "--port", "10001"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_reconfigure_OK,
            ],
            destination,
            [
                "update", "99282721-934c-42be-ba4d-a93cbfda2644",
                "--no-enabled",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            destination,
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

    @patch('opnsense_cli.commands.core.syslog.destination.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_reconfigure_OK,
            ],
            destination,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
