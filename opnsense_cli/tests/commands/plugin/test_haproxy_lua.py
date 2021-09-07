from unittest.mock import patch, Mock
from opnsense_cli.commands.plugin.haproxy.lua import lua
from opnsense_cli.tests.commands.base import CommandTestCase


class TestHaproxyLuaCommands(CommandTestCase):
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
            "validations": {'lua.description': 'Should be a string between 1 and 255 characters.'}
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
            "haproxy": {
                "luas": {
                    "lua": []
                }
            }
        }
        self._api_data_fixtures_list = self._read_json_fixture('plugin/haproxy/model_data.json')
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_list(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            lua,
            [
                'list', '-o', 'plain', '-c',
                'uuid,enabled,name,description,content'
            ]
        )

        self.assertIn(
            (
                'ffe95743-837c-4a38-98bd-6beafcbd6fa5 1 my_lua_script test '
                'core.register_action("verify_request", { "http-req" }, function(txn)\n'
                '   -- Verify that the request is authorized\n'
                '   -- Obviously stupid in this case without additional information being sent\n'
                '   local s = core.tcp()\n\n'
                '   -- Should be pointing to an HAProxy frontend with balancing/health checks/etc.\n'
                '   s:connect("127.0.0.1:8080")\n\n'
                '   -- We use HTTP 1.0 because we don\'t support keepalive or any '
                'other advanced features in this script.\n'
                '   s:send("GET /verify.php?url=" .. txn.sf:path() .. " HTTP/1.1\\r\\n'
                'Host: veriy.example.com\\r\\n\\r\\n")\n'
                '   local msg = s:receive("*l")\n\n'
                '   -- Indicates a connection failure\n'
                '   if msg == nil then\n'
                '      -- This leave txn.request_verified unset for potentially diffrent handling\n'
                '      return\n   end\n\n'
                '   msg = tonumber(string.sub(msg, 9, 12)) -- Read code from \'HTTP/1.0 XXX\'\n\n'
                '   -- Makes it easy to test by making any file to be denied.\n'
                '   if msg == 404 then\n      txn.set_var(txn,"txn.request_verified",true)\n'
                '   else\n      txn.set_var(txn,"txn.request_verified",false)\n   end\n\n'
                '   -- Read the response body, though in this example we aren\'t using it.\n'
                '   msg = s:receive("*l")\nend)\n'
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_list_EMPTY(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list_EMPTY,
            ],
            lua,
            ['list', '-o', 'plain']
        )

        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_show_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            lua,
            ['show', 'b468c719-89db-45a8-bd02-b081246dc002']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_show_EMPTY_STRING(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            lua,
            ['show', '']
        )
        self.assertIn("", result.output)

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_show(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            lua,
            [
                'show', 'ffe95743-837c-4a38-98bd-6beafcbd6fa5', '-o', 'plain', '-c',
                'enabled,name,description,content'
            ]
        )

        self.assertIn(
            (
                '1 my_lua_script test '
                'core.register_action("verify_request", { "http-req" }, function(txn)\n'
                '   -- Verify that the request is authorized\n'
                '   -- Obviously stupid in this case without additional information being sent\n'
                '   local s = core.tcp()\n\n'
                '   -- Should be pointing to an HAProxy frontend with balancing/health checks/etc.\n'
                '   s:connect("127.0.0.1:8080")\n\n'
                '   -- We use HTTP 1.0 because we don\'t support keepalive or any '
                'other advanced features in this script.\n'
                '   s:send("GET /verify.php?url=" .. txn.sf:path() .. " HTTP/1.1\\r\\n'
                'Host: veriy.example.com\\r\\n\\r\\n")\n'
                '   local msg = s:receive("*l")\n\n'
                '   -- Indicates a connection failure\n'
                '   if msg == nil then\n'
                '      -- This leave txn.request_verified unset for potentially diffrent handling\n'
                '      return\n   end\n\n'
                '   msg = tonumber(string.sub(msg, 9, 12)) -- Read code from \'HTTP/1.0 XXX\'\n\n'
                '   -- Makes it easy to test by making any file to be denied.\n'
                '   if msg == 404 then\n      txn.set_var(txn,"txn.request_verified",true)\n'
                '   else\n      txn.set_var(txn,"txn.request_verified",false)\n   end\n\n'
                '   -- Read the response body, though in this example we aren\'t using it.\n'
                '   msg = s:receive("*l")\nend)\n'
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_create_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
            [
                "create", "my_test_lua",
                "--content", "-- a comment"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_create_ERROR(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_create_ERROR,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
            [
                "create", "my_test_lua",
                "--content", "-- a comment",
                "--description",
                "12001201200201200210202100210210201032183902140479314713905734095703457043570347503927504325702"
                "43957032457023475092357034257024357042375042382374t385784735238562586853498573957340957035734059"
                "7430573405943709750439754039754035974035743057403957403570439574390570435704397504375094375043975"
            ]
        )

        self.assertIn(
            (
                "Error: {'result': 'failed', 'validations': "
                "{'lua.description': 'Should be a string between 1 and 255 characters.'}}\n"
            ),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_update_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
            [
                "update", "ffe95743-837c-4a38-98bd-6beafcbd6fa5",
                "--content", "-- another comment"
            ]
        )

        self.assertIn(
            (
                "saved \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_update_NOT_EXISTS(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_update_NOT_EXISTS,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
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

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_delete_OK(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_OK,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
            [
                "delete", "ffe95743-837c-4a38-98bd-6beafcbd6fa5",
            ]
        )

        self.assertIn(
            (
                "deleted \n"
            ),
            result.output
        )

    @patch('opnsense_cli.commands.plugin.haproxy.lua.ApiClient.execute')
    def test_delete_NOT_FOUND(self, api_response_mock: Mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_delete_NOT_FOUND,
                self._api_data_fixtures_configtest_OK,
                self._api_data_fixtures_reconfigure_OK,
            ],
            lua,
            [
                "delete", "99282721-934c-42be-ba4d-a93cbfda2644",
            ]
        )

        self.assertIn("Error: {'result': 'not found'}\n", result.output)
        self.assertEqual(1, result.exit_code)
