import unittest
import click
from click.testing import CliRunner
from opnsense_cli.types.click_param_type.int_or_empty import INT_OR_EMPTY


class TestClickParamTypes(unittest.TestCase):
    def setUp(self):
        @click.command()
        @click.option(
            "--int_or_empty",
            type=INT_OR_EMPTY,
            help="Could be an int value or an empty string."
        )
        def cli_int_or_empty(int_or_empty):
            click.echo(f"int_or_empty={int_or_empty}")
        self._cli_int_or_empty = cli_int_or_empty

    def test_Int_or_Empty_returns_INT(self):
        runner = CliRunner()
        result = runner.invoke(self._cli_int_or_empty, ['--int_or_empty', '5'])
        print(result.output)
        self.assertEqual(result.output, "int_or_empty=5\n")

    def test_Int_or_Empty_returns_EMPTY_STRING(self):
        runner = CliRunner()
        result = runner.invoke(self._cli_int_or_empty, ['--int_or_empty', ''])
        print(result.output)
        self.assertEqual(result.output, "int_or_empty=\n")

    def test_Int_or_Empty_returns_ERROR(self):
        runner = CliRunner()
        result = runner.invoke(self._cli_int_or_empty, ['--int_or_empty', '0.5'])

        self.assertEqual(2, result.exit_code)
