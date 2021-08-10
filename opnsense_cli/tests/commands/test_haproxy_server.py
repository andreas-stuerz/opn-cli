from unittest.mock import patch, Mock
from opnsense_cli.commands.haproxy.server import server
from opnsense_cli.tests.commands.base import CommandTestCase


class TestHaproxyServerCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_reconfigure_OK = {
            "status": "ok"
        }
        self._api_data_fixtures_reconfigure_FAILED = {
            "status": "failed"
        }
        self._api_data_fixtures_configtest_OK = {
            "result": "Configuration file is valid\n\n\n"
        }
        self._api_data_fixtures_configtest_FAILED = {
            "result": "Configuration file is invalid\n\n\n"
        }

        self._api_data_fixtures_create_OK = {
            "result": "saved",
            "uuid": "85282721-934c-42be-ba4d-a93cbfda26af"
        }
        self._api_data_fixtures_create_ERROR = {
            "result": "failed",
            "validations": {"server.weight": "Please specify a value between 0 and 256."}
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
        self._api_data_fixtures_list = {
            "haproxy": {
                "servers": {
                    "server": {
                        "dd74172b-d5c7-4d44-9ce3-667675a1e780": {
                            "id": "61126a6eaa9e37.48182479",
                            "enabled": "1",
                            "name": "server1",
                            "description": "",
                            "address": "192.168.56.1",
                            "port": "8081",
                            "checkport": "",
                            "mode": {
                                "": {
                                    "value": "none",
                                    "selected": False
                                },
                                "active": {
                                    "value": "active [default]",
                                    "selected": 1
                                },
                                "backup": {
                                    "value": "backup",
                                    "selected": 0
                                },
                                "disabled": {
                                    "value": "disabled",
                                    "selected": 0
                                }
                            },
                            "type": {
                                "static": {
                                    "value": "static",
                                    "selected": 1
                                },
                                "template": {
                                    "value": "template",
                                    "selected": 0
                                }
                            },
                            "serviceName": "",
                            "number": "",
                            "linkedResolver": {
                                "": {
                                    "value": "none",
                                    "selected": 0
                                },
                                "cea8f031-9aba-4f6e-86c2-f5f5f27a10b8": {
                                    "value": "my_resolver",
                                    "selected": 0
                                }
                            },
                            "resolverOpts": {
                                "allow-dup-ip": {
                                    "value": "allow-dup-ip",
                                    "selected": 0
                                },
                                "ignore-weight": {
                                    "value": "ignore-weight",
                                    "selected": 0
                                },
                                "prevent-dup-ip": {
                                    "value": "prevent-dup-ip",
                                    "selected": 0
                                }
                            },
                            "resolvePrefer": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "ipv4": {
                                    "value": "prefer IPv4",
                                    "selected": 0
                                },
                                "ipv6": {
                                    "value": "prefer IPv6 [default]",
                                    "selected": 0
                                }
                            },
                            "ssl": "1",
                            "sslVerify": "1",
                            "sslCA": {
                                "60cc45d3d7530": {
                                    "value": "internal ca",
                                    "selected": 0
                                },
                                "610d3779926d6": {
                                    "value": "special-ca",
                                    "selected": 0
                                }
                            },
                            "sslCRL": {
                                "": {
                                    "value": "",
                                    "selected": 1
                                }
                            },
                            "sslClientCertificate": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "610d37950266d": {
                                    "value": "special-cert",
                                    "selected": 0
                                },
                                "60cc4641eb577": {
                                    "value": "Web Gui Certificate",
                                    "selected": 0
                                },
                                "5eba6f0f352e3": {
                                    "value": "Web GUI SSL certificate",
                                    "selected": 0
                                }
                            },
                            "weight": "",
                            "checkInterval": "",
                            "checkDownInterval": "",
                            "source": "",
                            "advanced": ""
                        },
                        "28cfa25d-74b2-4a22-9f4a-d5923fb1394d": {
                            "id": "61126a714a0045.92956936",
                            "enabled": "1",
                            "name": "server2",
                            "description": "",
                            "address": "",
                            "port": "",
                            "checkport": "",
                            "mode": {
                                "": {
                                    "value": "none",
                                    "selected": False
                                },
                                "active": {
                                    "value": "active [default]",
                                    "selected": 1
                                },
                                "backup": {
                                    "value": "backup",
                                    "selected": 0
                                },
                                "disabled": {
                                    "value": "disabled",
                                    "selected": 0
                                }
                            },
                            "type": {
                                "static": {
                                    "value": "static",
                                    "selected": 1
                                },
                                "template": {
                                    "value": "template",
                                    "selected": 0
                                }
                            },
                            "serviceName": "",
                            "number": "",
                            "linkedResolver": {
                                "": {
                                    "value": "none",
                                    "selected": 0
                                },
                                "cea8f031-9aba-4f6e-86c2-f5f5f27a10b8": {
                                    "value": "my_resolver",
                                    "selected": 0
                                }
                            },
                            "resolverOpts": {
                                "allow-dup-ip": {
                                    "value": "allow-dup-ip",
                                    "selected": 0
                                },
                                "ignore-weight": {
                                    "value": "ignore-weight",
                                    "selected": 0
                                },
                                "prevent-dup-ip": {
                                    "value": "prevent-dup-ip",
                                    "selected": 0
                                }
                            },
                            "resolvePrefer": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "ipv4": {
                                    "value": "prefer IPv4",
                                    "selected": 0
                                },
                                "ipv6": {
                                    "value": "prefer IPv6 [default]",
                                    "selected": 0
                                }
                            },
                            "ssl": "0",
                            "sslVerify": "1",
                            "sslCA": {
                                "60cc45d3d7530": {
                                    "value": "internal ca",
                                    "selected": 0
                                },
                                "610d3779926d6": {
                                    "value": "special-ca",
                                    "selected": 0
                                }
                            },
                            "sslCRL": {
                                "": {
                                    "value": "",
                                    "selected": 1
                                }
                            },
                            "sslClientCertificate": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "610d37950266d": {
                                    "value": "special-cert",
                                    "selected": 0
                                },
                                "60cc4641eb577": {
                                    "value": "Web Gui Certificate",
                                    "selected": 0
                                },
                                "5eba6f0f352e3": {
                                    "value": "Web GUI SSL certificate",
                                    "selected": 0
                                }
                            },
                            "weight": "",
                            "checkInterval": "",
                            "checkDownInterval": "",
                            "source": "",
                            "advanced": ""
                        },
                        "46e159c3-c96d-45a1-8c81-f963c40e1e9f": {
                            "id": "61126a743fa570.29363631",
                            "enabled": "1",
                            "name": "server4",
                            "description": "",
                            "address": "10.0.0.1",
                            "port": "9000",
                            "checkport": "",
                            "mode": {
                                "": {
                                    "value": "none",
                                    "selected": False
                                },
                                "active": {
                                    "value": "active [default]",
                                    "selected": 1
                                },
                                "backup": {
                                    "value": "backup",
                                    "selected": 0
                                },
                                "disabled": {
                                    "value": "disabled",
                                    "selected": 0
                                }
                            },
                            "type": {
                                "static": {
                                    "value": "static",
                                    "selected": 1
                                },
                                "template": {
                                    "value": "template",
                                    "selected": 0
                                }
                            },
                            "serviceName": "",
                            "number": "",
                            "linkedResolver": {
                                "": {
                                    "value": "none",
                                    "selected": 0
                                },
                                "cea8f031-9aba-4f6e-86c2-f5f5f27a10b8": {
                                    "value": "my_resolver",
                                    "selected": 0
                                }
                            },
                            "resolverOpts": {
                                "allow-dup-ip": {
                                    "value": "allow-dup-ip",
                                    "selected": 0
                                },
                                "ignore-weight": {
                                    "value": "ignore-weight",
                                    "selected": 0
                                },
                                "prevent-dup-ip": {
                                    "value": "prevent-dup-ip",
                                    "selected": 0
                                }
                            },
                            "resolvePrefer": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "ipv4": {
                                    "value": "prefer IPv4",
                                    "selected": 0
                                },
                                "ipv6": {
                                    "value": "prefer IPv6 [default]",
                                    "selected": 0
                                }
                            },
                            "ssl": "0",
                            "sslVerify": "1",
                            "sslCA": {
                                "60cc45d3d7530": {
                                    "value": "internal ca",
                                    "selected": 0
                                },
                                "610d3779926d6": {
                                    "value": "special-ca",
                                    "selected": 0
                                }
                            },
                            "sslCRL": {
                                "": {
                                    "value": "",
                                    "selected": 1
                                }
                            },
                            "sslClientCertificate": {
                                "": {
                                    "value": "none",
                                    "selected": True
                                },
                                "610d37950266d": {
                                    "value": "special-cert",
                                    "selected": 0
                                },
                                "60cc4641eb577": {
                                    "value": "Web Gui Certificate",
                                    "selected": 0
                                },
                                "5eba6f0f352e3": {
                                    "value": "Web GUI SSL certificate",
                                    "selected": 0
                                }
                            },
                            "weight": "",
                            "checkInterval": "",
                            "checkDownInterval": "",
                            "source": "",
                            "advanced": ""
                        }
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

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            server,
            ['list', '-o', 'plain']
        )

        self.assertIn(
            (
                "dd74172b-d5c7-4d44-9ce3-667675a1e780 server1 static 192.168.56.1 8081  1 1  1\n"
                "28cfa25d-74b2-4a22-9f4a-d5923fb1394d server2 static    0 1  1\n"
                "46e159c3-c96d-45a1-8c81-f963c40e1e9f server4 static 10.0.0.1 9000  0 1  1\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            server,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            server,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            server,
            ['show', 'dd74172b-d5c7-4d44-9ce3-667675a1e780', '-o', 'plain']
        )

        self.assertIn(
            (
                "61126a6eaa9e37.48182479 server1 static 192.168.56.1 8081  1\n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
            [
                "create", "my_test_server",
                "--disabled",
                "--type", "template",
                "--description", "test",
                "--address", "10.0.0.1",
                "--port", "9091",
                "--mode", "backup",
                "--no-ssl",
                "--no-ssl",
                "--no-ssl-verify",
                "--weight", "10",
                "--checkInterval", "10",
                "--source", "10.0.0.5",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
            [
                "create", "my_test_server",
                "--weight", "10000",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', "
                "'validations': {'server.weight': 'Please specify a value between 0 and 256.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
            [
                "update", "85282721-934c-42be-ba4d-a93cbfda26af",
                "--enabled",
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
            [
                "update", "99282721-934c-42be-ba4d-a93cbfda2644",
                "--disabled",
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed'}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
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

    @patch('opnsense_cli.commands.firewall.rule.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            server,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
