import unittest
from unittest.mock import patch
from click.testing import CliRunner
from opnsense_cli.api.client import ApiClient
from opnsense_cli.commands.plugin import plugin


class TestPluginCommands(unittest.TestCase):
    def setUp(self):
        self._api_data_fixtures = {
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
        result = runner.invoke(plugin, ['list'], obj=client)

        self.assertIn(
            "os-acme-client 2.4 Let's Encrypt client 0\n" +
            "os-haproxy 3.1 Reliable, high performance TCP/HTTP load balancer 0\n"
            "os-virtualbox 1.0_1 VirtualBox guest additions 0\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_installed(self, api_response_mock):
        data = self._api_data_fixtures
        data['plugin'][0]['installed'] = '1'
        data['plugin'][0]['configured'] = '1'

        api_response_mock.return_value = data
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['installed'], obj=client)

        self.assertIn(
            "os-acme-client 2.4 Let's Encrypt client N/A\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_show(self, api_response_mock):
        api_response_mock.return_value = {
            "details": "The xyz plugin\n\n" +
                       "The xyz example plugin\n\n" +
                       "Maintainer: maintainer@example.com"
        }
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['show', 'os-haproxy'], obj=client)

        self.assertIn(
            "The xyz plugin\n\nThe xyz example plugin\n\nMaintainer: maintainer@example.com\n",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_install(self, api_response_mock):
        api_response_mock.return_value = {"status": "ok", "msg_uuid": "ce9c554b-5cc2-4d98-a559-3bc10a2f99ab"}
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['install', 'os-haproxy'], obj=client)

        self.assertIn("ok\n", result.output)
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_uninstall(self, api_response_mock):
        api_response_mock.return_value = {"status": "ok", "msg_uuid": "de9c554b-5cc2-4d98-a559-3bc10a2f99ab"}
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['uninstall', 'os-haproxy'], obj=client)

        self.assertIn("ok\n", result.output)
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_reinstall(self, api_response_mock):
        api_response_mock.return_value = {"status": "ok", "msg_uuid": "xe9c554b-5cc2-4d98-a559-3bc10a2f99ab"}
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['reinstall', 'os-haproxy'], obj=client)

        self.assertIn("ok\n", result.output)
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_lock(self, api_response_mock):
        api_response_mock.return_value = {"status": "ok", "msg_uuid": "xe9c554b-5cc2-4d98-a559-3bc10a2f99ab"}
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['lock', 'os-haproxy'], obj=client)

        self.assertIn("ok\n", result.output)
        self.assertEqual(0, result.exit_code)

    @patch('opnsense_cli.commands.plugin.ApiClient.execute')
    def test_unlock(self, api_response_mock):
        api_response_mock.return_value = {"status": "ok", "msg_uuid": "ze9c554b-5cc2-4d98-a559-3bc10a2f99ab"}
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        result = runner.invoke(plugin, ['unlock', 'os-haproxy'], obj=client)

        self.assertIn("ok\n", result.output)
        self.assertEqual(0, result.exit_code)
