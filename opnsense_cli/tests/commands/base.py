import json
import os
from unittest.mock import Mock
from click.testing import CliRunner, Result
from click.core import Group
from opnsense_cli.api.client import ApiClient
from pyfakefs.fake_filesystem_unittest import TestCase


class CommandTestCase(TestCase):
    def _read_json_fixture(self, relative_path):
        path = self._get_fixture_path(relative_path)
        file_content = self._read_file(path)
        return json.loads(file_content)

    def _read_fixture_file(self, relative_path):
        path = self._get_fixture_path(relative_path)
        file_content = self._read_file(path)
        return file_content

    def _read_template_file(self, relative_path):
        path = self._get_template_path(relative_path)
        file_content = self._read_file(path)
        return file_content

    def _get_fixture_path(self, relative_path, fixture_dir='../../fixtures/tests/commands'):
        path = os.path.join(os.path.dirname(__file__), fixture_dir, relative_path)
        return os.path.abspath(path)

    def _get_template_path(self, relative_path, template_dir='../../templates'):
        path = os.path.join(os.path.dirname(__file__), template_dir, relative_path)
        return os.path.abspath(path)

    def _read_file(self, path):
        with open(path) as file:
            content = file.read()
        return content

    def _setup_fakefs(self):
        template_dir = self._get_template_path('')
        fixture_dir = self._get_fixture_path('')

        self.setUpPyfakefs()
        self.fs.add_real_directory(template_dir)
        self.fs.add_real_directory(fixture_dir)

    def _show_fakefs_contents(self):
        for file in os.walk('/'):
            print(file)

    def _opn_cli_command_result(self, api_mock: Mock, api_return_values: list, click_group: Group,
                                click_params: list, catch_exceptions=False) -> Result:
        """
        :param api_mock: Mock for the API Object, so we can safely test
        :param api_return_values: The values for the api mock in order they should be returned.
        :param click_group: The click group
        :param click_params: The params for the click group command
        :param catch_exceptions: Whether exceptions should be caught.
        :return: click.testing.Result
        """
        api_mock.side_effect = api_return_values
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        return runner.invoke(click_group, click_params, obj=client, catch_exceptions=catch_exceptions)

    def _mock_response(self, status=200, content="CONTENT", json_data=None, raise_for_status=None):
        mock_resp = Mock()

        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content

        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )

        return mock_resp
