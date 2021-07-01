import unittest
from unittest.mock import Mock
from click.testing import CliRunner
from opnsense_cli.api.client import ApiClient


class CommandTestCase(unittest.TestCase):
    def _opn_cli_command_result(self, api_mock: Mock, api_return_values: list, click_group, click_params: list):
        api_mock.side_effect = api_return_values
        client_args = self._api_client_args_fixtures
        client = ApiClient(*client_args)

        runner = CliRunner()
        return runner.invoke(click_group, click_params, obj=client)
