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

    def test_output_all_columns_with_json_obj(self):
        format = ColsOutputFormat(self._api_data_json_obj, [''])

        result = self._get_format_output(format)

        self.assertIn(
            'enabled,name,type,proto,counters,updatefreq,content,description,uuid\n',
            result
        )

    def test_output_all_columns_with_json_array(self):
        format = ColsOutputFormat(self._api_data_json_array, [''])

        result = self._get_format_output(format)

        self.assertIn(
            'name,version,comment,flatsize,locked,license,repository,origin,provided,installed,path,configured\n',
            result
        )

    def test_output_all_columns_with_json_nested(self):
        format = ColsOutputFormat(self._api_data_json_nested, [''])

        result = self._get_format_output(format)

        self.assertIn(
            '<ID>,name,supportedOptions\n',
            result
        )
