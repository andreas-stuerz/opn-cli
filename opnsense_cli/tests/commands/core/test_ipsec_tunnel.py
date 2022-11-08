from unittest.mock import patch, Mock
from opnsense_cli.commands.core.ipsec.tunnel_phase1 import phase1
from opnsense_cli.commands.core.ipsec.tunnel_phase2 import phase2
from opnsense_cli.tests.commands.base import CommandTestCase


class TestIpsecTunnelCommands(CommandTestCase):
    def setUp(self):

        self._api_data_fixtures_list_phase1 = {
            "total": 2,
            "rowCount": 2,
            "current": 1,
            "rows": [
                {
                    "id": 1,
                    "seqid": 0,
                    "enabled": "1",
                    "protocol": "IPv4",
                    "iketype": "IKEv2",
                    "interface": "WAN",
                    "remote_gateway": "10.50.1.216",
                    "mobile": False,
                    "mode": "",
                    "proposal": "256 bit AES-GCM with 128 bit ICV + SHA256 + DH Group 14,15",
                    "authentication": "Mutual PSK",
                    "description": "test tunnel",
                    "type": "IPv4 IKEv2"
                },
                {
                    "id": 2,
                    "seqid": 1,
                    "enabled": "1",
                    "protocol": "IPv4",
                    "iketype": "IKEv2",
                    "interface": "WAN",
                    "remote_gateway": "10.3.4.5",
                    "mobile": False,
                    "mode": "",
                    "proposal": "256 bit AES-GCM with 128 bit ICV + SHA256 + DH Group 14",
                    "authentication": "Mutual PSK",
                    "description": "test tunnel2",
                    "type": "IPv4 IKEv2"
                }
            ]
        }

        self._api_data_fixtures_list_phase2 = {
            "total": 2,
            "rowCount": 2,
            "current": 1,
            "rows": [
                {
                    "id": 0,
                    "uniqid": "63690e24f3a72",
                    "ikeid": 1,
                    "reqid": "1",
                    "enabled": "1",
                    "protocol": "ESP",
                    "mode": "IPv4 tunnel",
                    "local_subnet": "LAN",
                    "remote_subnet": "10.2.1.250/32",
                    "proposal": "aes256gcm16 + SHA256+ DH Group 1",
                    "description": "test 2"
                },
                {
                    "id": 1,
                    "uniqid": "63690e4ab1bcf",
                    "ikeid": 1,
                    "reqid": "2",
                    "enabled": "1",
                    "protocol": "ESP",
                    "mode": "IPv4 tunnel",
                    "local_subnet": "LAN",
                    "remote_subnet": "10.2.1.253/32",
                    "proposal": "aes256gcm16 + SHA256",
                    "description": ""
                }
            ]
        }

        self._api_data_fixtures_list_EMPTY = {
            "total": 0,
            "rowCount": 0,
            "current": 1,
            "rows": []
        }

        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase1.ApiClient.execute')
    def test_list_phase1(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_phase1,
            ],
            phase1,
            [
                'list', '-o', 'plain', '-c',
                'id,remote_gateway'
            ]
        )

        self.assertIn(
            (
                "1 10.50.1.216\n2 10.3.4.5\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase1.ApiClient.execute')
    def test_list_phase1_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            phase1,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase2.ApiClient.execute')
    def test_list_phase2(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_phase1,
                self._api_data_fixtures_list_phase2,
                self._api_data_fixtures_list_EMPTY
            ],
            phase2,
            [
                'list', '-o', 'plain', '-c',
                'id,ikeid,uniqid,remote_subnet'
            ],
            True
        )

        self.assertIn(
            (
                "0 1 63690e24f3a72 10.2.1.250/32\n"
                "1 1 63690e4ab1bcf 10.2.1.253/32\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase2.ApiClient.execute')
    def test_list_phase2_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            phase2,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase1.ApiClient.execute')
    def test_show_phase1(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_phase1,
            ],
            phase1,
            ['show', '1', '-o', 'plain', '-c', 'id,interface,remote_gateway']
        )
        self.assertIn(
            (
                "1 WAN 10.50.1.216\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.ipsec.tunnel_phase2.ApiClient.execute')
    def test_show_phase2(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_phase1,
                self._api_data_fixtures_list_phase2,
                self._api_data_fixtures_list_EMPTY
            ],
            phase2,
            ['show', '63690e24f3a72', '-o', 'plain']
        )
        self.assertIn(
            (
                "0 63690e24f3a72 1 1 1 ESP IPv4 tunnel LAN 10.2.1.250/32 aes256gcm16 + SHA256+ DH Group 1 test 2\n"
            ),
            result.output
        )
