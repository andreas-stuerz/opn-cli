from unittest.mock import patch, Mock
from opnsense_cli.commands.core.firewall.alias import alias
from opnsense_cli.tests.commands.base import CommandTestCase


class TestFirewallAliasCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_apply_OK = {
            "status": "ok"
        }
        self._api_data_fixtures_apply_FAILED = {
            "status": "failed"
        }
        self._api_data_fixtures_create_OK = {
            "result": "saved",
            "uuid": "5c2163a8-a429-4226-a3b8-dd2b1560b12b"
        }
        self._api_data_fixtures_create_ERROR = {
            "result": "failed",
            "validations": {"alias.content": "Entry \"test\" is not a valid alias."}
        }
        self._api_data_fixtures_create_EXISTS = {
            "result": "failed",
            "validations": {"alias.name": "An alias with this name already exists."}
        }
        self._api_data_fixtures_update_NOT_EXISTS = {
            "result": "failed"
        }
        self._api_data_fixtures_update_OK = {
            "result": "saved"
        }
        self._api_data_fixtures_delete_NOT_FOUND = {
            "result": "not found"
        }
        self._api_data_fixtures_delete_OK = {
            "result": "deleted"
        }
        self._api_data_uuid_for_name = {
            'uuid': '23636461-dfd1-46cf-9d60-ee46f6aeb04a'
        }
        self._api_data_fixtures_list = {
            "aliases": {
                "alias": {
                    "bogons": {
                        "enabled": "1",
                        "name": "bogons",
                        "type": "external",
                        "proto": "",
                        "counters": "",
                        "updatefreq": "",
                        "content": "",
                        "description": "bogon networks (internal)",
                        "uuid": "bogons"
                    },
                    "bogonsv6": {
                        "enabled": "1",
                        "name": "bogonsv6",
                        "type": "external",
                        "proto": "",
                        "counters": "",
                        "updatefreq": "",
                        "content": "",
                        "description": "bogon networks IPv6 (internal)",
                        "uuid": "bogonsv6"
                    },
                    "23636461-dfd1-46cf-9d60-ee46f6aeb04a": {
                        "enabled": "1",
                        "name": "example_alias",
                        "type": "host",
                        "proto": "",
                        "counters": "1",
                        "updatefreq": "",
                        "content": "www.example.com",
                        "description": "test alias",
                        "uuid": "23636461-dfd1-46cf-9d60-ee46f6aeb04a"
                    },
                    "sshlockout": {
                        "enabled": "1",
                        "name": "sshlockout",
                        "type": "external",
                        "proto": "",
                        "counters": "",
                        "updatefreq": "",
                        "content": "",
                        "description": "abuse lockout table (internal)",
                        "uuid": "sshlockout"
                    },
                    "virusprot": {
                        "enabled": "1",
                        "name": "virusprot",
                        "type": "external",
                        "proto": "",
                        "counters": "",
                        "updatefreq": "",
                        "content": "",
                        "description": "overload table for rate limitting (internal)",
                        "uuid": "virusprot"
                    }
                }
            }
        }
        self._api_data_fixtures_table = {
            'total': 4,
            'rowCount': -1,
            'current': 1,
            'rows': [
                {'ip': '193.99.144.85'},
                {'ip': '2606:2800:220:1:248:1893:25c8:1946'},
                {'ip': '2a02:2e0:3fe:1001:7777:772e:2:85'},
                {'ip': '93.184.216.34'}
            ]
        }

        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            alias,
            ['list', '-o', 'plain']
        )

        self.assertIn(
            (
                "bogons external bogon networks (internal)  1\n"
                "bogonsv6 external bogon networks IPv6 (internal)  1\n"
                "example_alias host test alias www.example.com 1\n"
                "sshlockout external abuse lockout table (internal)  1\n"
                "virusprot external overload table for rate limitting (internal)  1\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_show_(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_uuid_for_name,
                self._api_data_fixtures_list
            ],
            alias,
            ['show', 'example_alias', '-o', 'plain']
        )

        self.assertIn(
            (
                "23636461-dfd1-46cf-9d60-ee46f6aeb04a example_alias host  1 test alias  www.example.com 1\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_table(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_table
            ],
            alias,
            ['table', 'example_alias', '-o', 'plain']
        )

        self.assertIn(
            (
                "193.99.144.85\n"
                "2606:2800:220:1:248:1893:25c8:1946\n"
                "2a02:2e0:3fe:1001:7777:772e:2:85\n"
                "93.184.216.34\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_apply_OK,
            ],
            alias,
            [
                "create", "new_url_table",
                "-t", "urltable",
                "-C", "'https://www.spamhaus.org/drop/drop.txt,https://www.spamhaus.org/drop/edrop.txt'",
                "-d", "Spamhaus block list",
                "-u", 0.5,
                "--counters",
                "--disabled",
                "-o", "plain"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
            ],
            alias,
            [
                "create", "error_alias",
                "-t", "networkgroup",
                "-C", "non_existing_alias",
                "-d", "error alias",
            ]
        )

        self.assertIn(
            (
                "Error: {\'result\': \'failed\', \'validations\': {\'alias.content\': "
                "\'Entry \"test\" is not a valid alias.\'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_create_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_EXISTS,
            ],
            alias,
            [
                "create", "existing_url_table",
                "-t", "urltable",
                "-C", "'https://www.spamhaus.org/drop/drop.txt,https://www.spamhaus.org/drop/edrop.txt'",
                "-d", "Spamhaus block list",
                "-u", 0.6,
                "--no-counters",
                "--enabled",
            ]
        )

        self.assertIn(
            (
                "Error: "
                "{'result': 'failed', 'validations': {'alias.name': 'An alias with this name already exists.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_uuid_for_name,
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_apply_OK,
            ],
            alias,
            [
                "update", "rename_geo_ip",
                "-n", "my_geo_ip",
                "-t", "geoip",
                "-C", "DE,GR",
                "-d", "blocked countries",
                "-p", "IPv4,IPv6",
                "--no-counters",
                "--enabled",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                [],
                self._api_data_fixtures_update_NOT_EXISTS,
            ],
            alias,
            [
                "update", "not_existing_geo_ip",
                "-t", "geoip",
                "-C", "DE,GR",
                "-d", "blocked countries",
                "-p", "IPv4,IPv6",
                "--counters",
                "--disabled",
            ]
        )

        self.assertIn("Error: {'result': 'failed'}\n", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_uuid_for_name,
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_apply_OK,
            ],
            alias,
            [
                "delete", "existing_alias",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                [],
                self._api_data_fixtures_delete_NOT_FOUND,
            ],
            alias,
            [
                "delete", "not_existing_alias",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.firewall.alias.ApiClient.execute')
    def test_alias_apply_FAILED(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_uuid_for_name,
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_apply_FAILED,

            ],
            alias,
            [
                "delete", "existing_alias",
            ],
            True
        )

        self.assertIn("Error: Apply failed: {'status': 'failed'}\n", result.output)
        self.assertEqual(1, result.exit_code)
