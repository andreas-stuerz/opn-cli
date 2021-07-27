from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.cols_output import ColsOutputFormat


class TestColsOutputFormat(FormatTestCase):
    def test_output_specific_columns(self):
        format = ColsOutputFormat(self._api_data_json_array, ['name', 'version'])

        result = self._get_format_output(format)

        self.assertIn(
            'name,version\n',
            result
        )

    def test_output_all_columns(self):
        format = ColsOutputFormat(self._api_data_json_array, [''])

        result = self._get_format_output(format)

        self.assertIn(
            'name,version,comment,flatsize,locked,license,repository,origin,provided,installed,path,configured\n',
            result
        )
