from unittest.mock import patch
from opnsense_cli.commands.core.configbackup.backup import backup
from opnsense_cli.tests.commands.base import CommandTestCase


class TestApibackupCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()

        self._api_data_fixtures_download = self._read_fixture_file("core/configbackup/config.xml.sample")
        self._api_client_args_fixtures = ["api_key", "api_secret", "https://127.0.0.1/api", True, "~/.opn-cli/ca.pem", 60]

    @patch("opnsense_cli.commands.core.configbackup.backup.ApiClient.execute")
    def test_download(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_download,
            ],
            backup,
            ["download"],
        )

        self.assertIn("successfully saved to: ./config.xml\n", result.output)
