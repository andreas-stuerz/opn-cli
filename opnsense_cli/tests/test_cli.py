import yaml
from unittest import TestCase
from unittest.mock import patch
from click.testing import CliRunner
from opnsense_cli.cli import cli


class TestCli(TestCase):
    def setUp(self):
        self._cli_config = {
            "api_key": "xxx",
            "api_secret": "yyy",
            "url": "https://127.0.0.1/api",
            "timeout": 40,
            "ssl_verify": True,
            "ca": "ca.pem",
            "test": "test"
        }

    @patch('opnsense_cli.cli.ApiClient.__init__')
    def test_cli(self, api_client_mock):
        api_client_mock.return_value = None
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('config.yaml', 'w') as f:
                yaml.dump(self._cli_config, f)

            result = runner.invoke(cli, ['-c', 'config.yaml', 'version'])

            api_client_mock.assert_called_once_with(
                self._cli_config['api_key'],
                self._cli_config['api_secret'],
                self._cli_config['url'],
                self._cli_config['ssl_verify'],
                self._cli_config['ca'],
                self._cli_config['timeout'],
            )
            self.assertEqual(0, result.exit_code)
