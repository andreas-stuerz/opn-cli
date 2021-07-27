from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.table_output import TableOutputFormat


class TestTableOutputFormat(FormatTestCase):
    def test_with_json_array(self):
        format = TableOutputFormat(self._api_data_json_array, ['name', 'version'])
        result = self._get_format_output(format)

        self.assertIn(
            (
                "+----------------+---------+\n"
                "|      name      | version |\n"
                "+----------------+---------+\n"
                "| os-acme-client |   2.4   |\n"
                "| os-virtualbox  |  1.0_1  |\n"
                "+----------------+---------+\n"
            ), result)
