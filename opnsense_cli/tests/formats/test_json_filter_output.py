from opnsense_cli.formats.json_filter_output import JsonFilterOutputFormat
from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.json_output import JsonOutputFormat


class TestJsonFilterOutputFormat(FormatTestCase):
    def test_with_json_array(self):
        format = JsonFilterOutputFormat(self._api_data_json_array, ['name', 'version'])

        result = self._get_format_output(format)

        self.assertIn(
            '[{"name": "os-acme-client", "version": "2.4"}, {"name": "os-virtualbox", "version": "1.0_1"}]\n',
            result
        )

    def test_with_json_obj(self):
        format = JsonFilterOutputFormat(self._api_data_json_obj, ['uuid', 'name'])

        result = self._get_format_output(format)

        self.assertIn(
            '{"uuid": "24948d07-8525-4276-b497-108a0c55fcc2", "name": "zabbix_host"}\n',
            result
        )

    def test_with_empty_data(self):
        format = JsonOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                "[]"
            ),
            result
        )
