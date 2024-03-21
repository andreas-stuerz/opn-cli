from unittest.mock import patch
from opnsense_cli.commands.plugin.apibackup.backup import backup
from opnsense_cli.commands.test_base import CommandTestCase
import base64
import os

class TestApibackupCommands(CommandTestCase):
    def setUp(self):
        self._setup_fakefs()


        self._config_xml = self._read_fixture_file("fixtures/config.xml.sample", base_dir=os.path.dirname(__file__))
        self._api_data_fixtures_download = {
            "status": "success",
            "filename": "config.xml",
            "filetype": "application/xml",
            "content": base64.b64encode(bytes(self._config_xml, "utf-8)")),
        }

        self._api_client_args_fixtures = ["api_key", "api_secret", "https://127.0.0.1/api", True, "~/.opn-cli/ca.pem", 60]

    @patch("opnsense_cli.commands.plugin.apibackup.backup.ApiClient.execute")
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
