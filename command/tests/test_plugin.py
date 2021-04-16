import unittest
from unittest.mock import patch
from click.testing import CliRunner
from api.client import ApiClient
from command.plugin import plugin


class TestPluginCommands(unittest.TestCase):
    @patch('command.plugin.ApiClient.execute')
    def test_list(self, api_response_mock):
        api_response_mock.return_value = {
            "plugin": [
                {
                    'name': 'os-zerotier',
                    'version': '1.3.2_3',
                    'comment': 'Virtual Networks That Just Work',
                    'flatsize': '47.9KiB',
                    'locked': 'N/A',
                    'license': 'BSD2CLAUSE',
                    'repository': 'OPNsense',
                    'origin': 'opnsense/os-zerotier',
                    'provided': '1',
                    'installed': '0',
                    'path': 'OPNsense/opnsense/os-zerotier',
                    'configured': '0'
                }
            ]
        }
        client_args = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['list'], obj=client)

        self.assertIn('os-zerotier 1.3.2_3 Virtual Networks That Just Work 0', result.output)
        self.assertEqual(0, result.exit_code)

