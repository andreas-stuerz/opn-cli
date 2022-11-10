from unittest.mock import patch, Mock
from opnsense_cli.commands.core.syslog.stats import stats
from opnsense_cli.tests.commands.base import CommandTestCase


class TestSyslogStatsCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_list = {
            'total': 2,
            'rowCount': 9999,
            'current': 1,
            'rows': [
                {
                    '#': 'e28eb856223592f3e11f8dcbb30f6dae',
                    'Description': 'Test Syslog host',
                    'SourceName': 'dst.network',
                    'SourceId': 'd_4dd6f818e9754136bf7eed2559675ef9#0',
                    'SourceInstance': 'tcp,10.0.0.1:514',
                    'State': 'a',
                    'Type': 'msg_size_max',
                    'Number': '0'
                },
                {
                    '#': '88caaaa1a6c05d7bb525289dfa7e7cb8',
                    'Description': '',
                    'SourceName': 'dst.network',
                    'SourceId': 'd_f2c748b815b745178ea14ab5d9423e8f#0',
                    'SourceInstance': 'udp,syslog.example.com:514',
                    'State': 'o',
                    'Type': 'msg_size_max',
                    'Number': '0'
                },
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

    @patch('opnsense_cli.commands.core.syslog.stats.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            stats,
            [
                'list', '-o', 'plain', '-c',
                '#,SourceName,SourceInstance'
            ],
        )

        self.assertIn(
            (
                "e28eb856223592f3e11f8dcbb30f6dae dst.network tcp,10.0.0.1:514\n"
                "88caaaa1a6c05d7bb525289dfa7e7cb8 dst.network udp,syslog.example.com:514\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.core.syslog.stats.ApiClient.execute')
    def test_list_SEARCH(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            stats,
            [
                'list',
                '--search', '10.0.0.1',
                '-o', 'plain',
                '-c', '#,SourceName,SourceInstance'
            ],
        )

        self.assertIn(
            (
                "e28eb856223592f3e11f8dcbb30f6dae dst.network tcp,10.0.0.1:514\n"
            ),
            result.output
        )
