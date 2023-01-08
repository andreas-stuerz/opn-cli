from unittest.mock import patch, Mock
from opnsense_cli.commands.core.unbound.alias import alias
from opnsense_cli.tests.commands.base import CommandTestCase


class TestUnboundAliasCommands(CommandTestCase):
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
            "validations": {'alias.domain': 'A valid domain must be specified.'}
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
                "aliases": {
                    "alias": []
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

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            alias,
            [
                'list', '-o', 'plain', '-c',
                'uuid,enabled,Host,hostname,domain,description'
            ]
        )

        self.assertIn(
            (
                "c2ab1046-6bc8-4b89-8542-2561f560424c 1 host01|example.com|A|||10.0.0.1 www example01.com \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            alias,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            alias,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            alias,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            alias,
            [
                'show', 'c2ab1046-6bc8-4b89-8542-2561f560424c', '-o', 'plain', '-c',
                'uuid,Host,hostname,domain,description'
            ]
        )

        self.assertIn(
            (
                "c2ab1046-6bc8-4b89-8542-2561f560424c host01|example.com|A|||10.0.0.1 www example01.com \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
            [
                "create",
                "--host", "host01|example.com|A|||10.0.0.1",
                "--hostname", "alias01",
                "--domain", ".example.com",
                "--description", "important alias",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
            [
                "create",
                "--host", "host01|example.com|A|||10.0.0.1",
                "--hostname", "alias01",
                "--domain", "üüü.üüü.ze",
                "--description", "important alias",
            ], catch_exceptions=True
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': "
                "{'alias.domain': 'A valid domain must be specified.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_create_APPLY_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                  self._api_data_fixtures_list,
                  self._api_data_fixtures_create_OK,
                  self._api_data_fixtures_reconfigure_FAILED,
            ],
            alias,
            [
              "create",
              "--host", "host01|example.com|A|||10.0.0.1",
              "--hostname", "alias01",
              "--domain", "example.com",
              "--description", "important alias",
            ]
        )

        self.assertIn(
          (
            "Error: Apply failed: {'status': 'failed'}\n"
          ),
          result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
            [
                "update", "c2ab1046-6bc8-4b89-8542-2561f560424c",
                "--host", "host01|example.com|A|||10.0.0.1"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
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

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
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

    @patch('opnsense_cli.commands.core.unbound.alias.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_reconfigure_OK,
            ],
            alias,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
