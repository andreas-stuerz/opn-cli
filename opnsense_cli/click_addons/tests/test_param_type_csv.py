import unittest
import click
from click.testing import CliRunner
from opnsense_cli.click_addons.param_type_csv import CSV


class TestClickParamTypeCsv(unittest.TestCase):
    def setUp(self):
        @click.command()
        @click.option("--csv", type=CSV, help="a String with comma separated values.")
        def cvs(csv):
            click.echo(f"csv={csv}")

        self._cli_cvs = cvs

    def test_csv_returns_csv(self):
        runner = CliRunner()
        result = runner.invoke(self._cli_cvs, ["--csv", "a,b,c"])
        print(result.output)
        self.assertEqual(result.output, "csv=a,b,c\n")

    def test_csv_has_correct_repr(self):
        self.assertEqual(repr(CSV), "CSV")
