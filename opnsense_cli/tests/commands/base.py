import json
import os
from unittest.mock import Mock
from click.testing import CliRunner, Result
from click.core import Group
from opnsense_cli.api.client import ApiClient
from pyfakefs.fake_filesystem_unittest import TestCase


class CommandTestCase(TestCase):
    def _read_json_fixture(self, relative_path, fixture_dir='../fixtures'):
        path = os.path.join(os.path.dirname(__file__), fixture_dir, relative_path)
        with open(path) as json_file:
            fixture = json.load(json_file)
        return fixture

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
