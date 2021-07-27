import json
from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.json_output import JsonOutputFormat


class TestJsonOutputFormat(FormatTestCase):
    def test_with_json_array(self):
        format = JsonOutputFormat(self._api_data_json_array, ['name'])

        result = self._get_format_output(format)

        self.assertIn(
            f"{json.dumps(self._api_data_json_array)}\n",
            result
        )
