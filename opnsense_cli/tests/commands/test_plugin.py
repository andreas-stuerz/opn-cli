from unittest.mock import patch
from opnsense_cli.commands.core.plugin import plugin
from opnsense_cli.tests.commands.base import CommandTestCase


class TestPluginCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_list = {
            "plugin": [
                {
                    'name': 'os-acme-client', 'version': '2.4', 'comment': "Let's Encrypt client",
                    'flatsize': '575KiB', 'locked': 'N/A', 'license': 'BSD2CLAUSE',
                    'repository': 'OPNsense', 'origin': 'opnsense/os-acme-client',
                    'provided': '1', 'installed': '0', 'path': 'OPNsense/opnsense/os-acme-client', 'configured': '0'
                },
                {
                    'name': 'os-haproxy', 'version': '3.1',
                    'comment': 'Reliable, high performance TCP/HTTP load balancer', 'flatsize': '658KiB',
                    'locked': 'N/A', 'license': 'BSD2CLAUSE', 'repository': 'OPNsense',
                    'origin': 'opnsense/os-haproxy', 'provided': '1', 'installed': '0',
                    'path': 'OPNsense/opnsense/os-haproxy', 'configured': '0'
                },
                {
                    'name': 'os-virtualbox', 'version': '1.0_1', 'comment': 'VirtualBox guest additions',
                    'flatsize': '525B', 'locked': 'N/A', 'license': 'BSD2CLAUSE', 'repository': 'OPNsense',
                    'origin': 'opnsense/os-virtualbox', 'provided': '1',
                    'installed': '0', 'path': 'OPNsense/opnsense/os-virtualbox', 'configured': '0'
                },
            ],
        }
        self._api_data_fixtures_OK = {
            "msg_uuid": "26abc5c9-8a38-4582-9736-a1b1bf867982",
            "status": "ok"
        }
        self._api_data_fixtures_upgrade_status_RUNNING = {
            "status": "running",
            "log": "Whatever....."
        }
        self._api_data_fixtures_upgrade_status_OK = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO INSTALL***\n"
                "Updating OPNsense repository catalogue...\n"
                "OPNsense repository is up to date.\n"
                "All repositories are up to date.\n"
                "Checking integrity... done (0 conflicting)\n"
                "The most recent versions of packages are already installed\n"
                "Checking integrity... done (0 conflicting)\n"
                "Nothing to do.\n"
                "***DONE***"
            )
        }
        self._api_data_fixtures_install_ERROR = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO INSTALL***\n"
                "Updating OPNsense repository catalogue...\n"
                "OPNsense repository is up to date.\n"
                "All repositories are up to date.\n"
                "pkg: No packages available to install matching 'os-helloworld2' have been found in the repositories\n"
                "Checking integrity... done (0 conflicting)\n"
                "Nothing to do.\n"
                "***DONE***"
            )
        }
        self._api_data_fixtures_uninstall_NOT_FOUND = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO REMOVE***\n"
                "No packages matched for pattern 'os-helloworld2'\n\n"
                "Checking integrity... done (0 conflicting)\n"
                "1 packages requested for removal: 0 locked, 1 missing"
            )
        }
        self._api_data_fixtures_reinstall_NOT_FOUND = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO REINSTALL***\n"
                "Package 'os-helloworld2' is not installed"
            )
        }
        self._api_data_fixtures_lock_NOT_FOUND = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO LOCK***\n"
                "***DONE***"
            )
        }
        self._api_data_fixtures_unlock_NOT_FOUND = {
            "status": "done",
            "log": (
                "***GOT REQUEST TO UNLOCK***\n"
                "***DONE***"
            )
        }

        self._api_data_fixtures_show = {
            "details": (
                "The xyz plugin\n\n"
                "The xyz example plugin\n\n"
                "Maintainer: maintainer@example.com"
            )
        }

        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_list(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_list,
            ],
            plugin,
            ['list', '-o', 'plain']
        )

        self.assertIn(
            "os-acme-client 2.4 Let's Encrypt client 0\n" +
            "os-haproxy 3.1 Reliable, high performance TCP/HTTP load balancer 0\n"
            "os-virtualbox 1.0_1 VirtualBox guest additions 0\n",
            result.output
        )

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_installed(self, api_response_mock):
        data = self._api_data_fixtures_list
        data['plugin'][0]['installed'] = '1'
        data['plugin'][0]['configured'] = '1'

        result = self._opn_cli_command_result(
            api_response_mock,
            [
                data,
            ],
            plugin,
            ['installed', '-o', 'plain']
        )

        self.assertIn(
            "os-acme-client 2.4 Let's Encrypt client N/A\n",
            result.output
        )

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_show(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_show,
            ],
            plugin,
            ['show', 'os-haproxy', '-o', 'plain']
        )

        self.assertIn(
            "The xyz plugin\n\nThe xyz example plugin\n\nMaintainer: maintainer@example.com\n",
            result.output
        )

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_install_OK(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_OK,
            ],
            plugin,
            ['install', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_install_ERROR(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_install_ERROR,
            ],
            plugin,
            ['install', 'does_not_exists']
        )

        self.assertIn("Error:", result.output)
        self.assertEqual(1, result.exit_code)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_uninstall_OK(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_OK,
            ],
            plugin,
            ['uninstall', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_uninstall_NOT_FOUND(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_uninstall_NOT_FOUND,
            ],
            plugin,
            ['uninstall', 'is_not_installed_plugin']
        )

        self.assertIn("not found\n", result.output)
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_reinstall_OK(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_OK,
            ],
            plugin,
            ['reinstall', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_reinstall_NOT_FOUND(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_reinstall_NOT_FOUND,
            ],
            plugin,
            ['reinstall', 'os-haproxy12121']
        )

        self.assertIn("not found\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_lock_OK(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_OK,
            ],
            plugin,
            ['lock', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_lock_NOT_FOUND(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_lock_NOT_FOUND,
            ],
            plugin,
            ['lock', 'os-haproxy12121']
        )

        self.assertIn("not found\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_unlock_OK(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_OK,
            ],
            plugin,
            ['unlock', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_unlock_NOT_FOUND(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_unlock_NOT_FOUND,
            ],
            plugin,
            ['unlock', 'os-haproxy_1212']
        )

        self.assertIn("not found\n", result.output)

    @patch('opnsense_cli.commands.core.plugin.ApiClient.execute')
    def test_upgrade_status_RUNNING(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_OK,
                self._api_data_fixtures_upgrade_status_RUNNING,
                self._api_data_fixtures_upgrade_status_OK,

            ],
            plugin,
            ['-t', 0, 'install', 'os-haproxy']
        )

        self.assertIn("done\n", result.output)
