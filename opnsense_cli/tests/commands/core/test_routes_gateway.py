from unittest.mock import patch, Mock
from opnsense_cli.commands.core.route.gateway import gateway
from opnsense_cli.tests.commands.base import CommandTestCase


class TestRoutesStaticCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_list_EMPTY = {
            "items": [],
            'status': 'ok'
        }
        self._api_data_fixtures_list = {
            "items": [
                {
                    "name": "WAN_DHCP6",
                    "address": "~",
                    "status": "none",
                    "status_translated": "Online",
                    "loss": "~",
                    "stddev": "~",
                    "delay": "~"
                },
                {
                    "name": "WAN_DHCP",
                    "address": "10.0.2.2",
                    "status": "none",
                    "status_translated": "Online",
                    "loss": "~",
                    "stddev": "~",
                    "delay": "~"
                }
            ],
            "status": "ok"
        }
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_status(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            gateway,
            [
                'status', '-o', 'plain', '-c',
                'name,address,status,status_translated,loss,stddev,delay'
            ]
        )

        self.assertIn(
            (
                "WAN_DHCP6 ~ none Online ~ ~ ~\n"
                "WAN_DHCP 10.0.2.2 none Online ~ ~ ~\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.route.static.ApiClient.execute')
    def test_show_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            gateway,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)
