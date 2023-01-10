from unittest.mock import patch, Mock
from opnsense_cli.commands.core.unbound.domain import domain
from opnsense_cli.tests.commands.base import CommandTestCase


class TestUnboundDomainCommands(CommandTestCase):
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
            "validations": {'domain.server': 'A valid IP address must be specified, for example 192.168.100.10.'}
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
            "unbound": {
                "domains": {
                    "domain": []
                }
            }
        }
        self._api_data_fixtures_list = self._read_json_fixture('core/unbound/model_data.json')
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            domain,
            [
                'list', '-o', 'plain', '-c',
                'uuid,enabled,domain,server,description'
            ]
        )

        self.assertIn(
            (
                "1e4485f5-24d0-42de-8631-ab906f377e92 1 text.abc 192.168.50.2 another test domain ovveride\n"
                "3c3fb49d-9e90-4264-844b-cde9f1aeab4d 1 override.de 127.0.0.1 test domain override\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            domain,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            domain,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            domain,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            domain,
            [
                'show', '1e4485f5-24d0-42de-8631-ab906f377e92', '-o', 'plain', '-c',
                'uuid,enabled,domain,server,description'
            ]
        )

        self.assertIn(
            (
                "1e4485f5-24d0-42de-8631-ab906f377e92 1 text.abc 192.168.50.2 another test domain ovveride\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
            [
                "create",
                "--domain", "domain.xyz.de",
                "--server", "192.168.40.2",
                "--description", "domain ovveride"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
            [
                "create",
                "--domain", "domain.xyz.de",
                "--server", "invalid",
                "--description", "domain ovveride"
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': "
                "{'domain.server': 'A valid IP address must be specified, for example 192.168.100.10.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_create_APPLY_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
              self._api_data_fixtures_create_OK,
              self._api_data_fixtures_reconfigure_FAILED,
            ],
            domain,
            [
              "create",
              "--domain", "domain.xyz.de",
              "--server", "192.168.40.2",
              "--description", "domain ovveride"
            ]
        )

        self.assertIn(
          (
            "Error: Apply failed: {'status': 'failed'}\n"
          ),
          result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
            [
                "update", "1e4485f5-24d0-42de-8631-ab906f377e92",
                "--server", "192.168.56.1"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
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

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
            [
                "delete", "1e4485f5-24d0-42de-8631-ab906f377e92",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.domain.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_reconfigure_OK,
            ],
            domain,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
