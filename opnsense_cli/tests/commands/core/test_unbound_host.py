from unittest.mock import patch, Mock
from opnsense_cli.commands.core.unbound.host import host
from opnsense_cli.tests.commands.base import CommandTestCase


class TestUnboundHostCommands(CommandTestCase):
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
            "validations": {'host.domain': 'A valid domain must be specified.'}
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
                "hosts": {
                    "host": []
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

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            host,
            [
                'list', '-o', 'plain', '-c',
                'uuid,hostname,domain,rr,server'
            ]
        )

        self.assertIn(
            (
                "3d424da4-328a-40ec-99c4-ceef0cf3e2be host03 example.com A 10.0.0.3\n"
                "65da9ff2-dc95-48a4-82e0-a00428d64e39 host01 example.com A 10.0.0.1\n"
                "8111ce26-08f6-4b2b-95d8-4d27f1121ed9 host02 example.com A 10.0.0.2\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            host,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            host,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            host,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            host,
            [
                'show', '65da9ff2-dc95-48a4-82e0-a00428d64e39', '-o', 'plain', '-c',
                'uuid,hostname,domain,rr,server'
            ]
        )

        self.assertIn(
            (
                "65da9ff2-dc95-48a4-82e0-a00428d64e39 host01 example.com A 10.0.0.1\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
            [
                "create",
                "--hostname", "new_host",
                "--domain", "example.com",
                "--description", "new example hosts",
                "--rr", "A",
                "--server", "10.0.0.2"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
            [
                "create",
                "--hostname", "new_host",
                "--domain", "error_com",
                "--description", "new example hosts",
                "--rr", "A",
                "--server", "10.0.0.2"
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': "
                "{'host.domain': 'A valid domain must be specified.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_create_APPLY_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_reconfigure_FAILED,
            ],
            host,
            [
                "create",
                "--hostname", "new_host",
                "--domain", "example.com",
                "--description", "new example hosts",
                "--rr", "A",
                "--server", "10.0.0.2"
            ]
        )

        self.assertIn(
            (
                "Error: Apply failed: {'status': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
            [
                "update", "65da9ff2-dc95-48a4-82e0-a00428d64e39",
                "--description", "updated example host description",
                "--server", "10.0.10.1"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
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

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
            [
                "delete", "8111ce26-08f6-4b2b-95d8-4d27f1121ed9",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.unbound.host.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_reconfigure_OK,
            ],
            host,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
