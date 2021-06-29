import unittest
from unittest.mock import patch
from click.testing import CliRunner
from opnsense_cli.api.client import ApiClient
from opnsense_cli.commands.firewall.alias import firewall, alias


class TestFirewallAliasCommands(unittest.TestCase):
    def setUp(self):
        self._api_data_fixtures = {
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
                        "name": "new_alias",
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
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_list(self, api_response_mock):
        api_response_mock.return_value = self._api_data_fixtures
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(alias, ['list'], obj=client)

        self.assertIn(
            (
                "bogons external bogon networks (internal)  1\n"
                "bogonsv6 external bogon networks IPv6 (internal)  1\n"
                "new_alias host test alias www.example.com 1\n"
                "sshlockout external abuse lockout table (internal)  1\n"
                "virusprot external overload table for rate limitting (internal)  1\n"
            ),
            result.output
        )

    def test_show(self):
        pass
