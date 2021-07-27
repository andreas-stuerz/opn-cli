from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.plain_output import PlainOutputFormat


class TestPlainOutputFormat(FormatTestCase):
    def test_with_json_array(self):
        format = PlainOutputFormat(self._api_data_json_array, ['name', 'version'])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "os-acme-client|2.4\n",
            result
        )

    def test_with_json_nested(self):
        format = PlainOutputFormat(self._api_data_json_nested, ['<ID>', 'name', 'supportedOptions'])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "ArchiveOpenVPN|Archive|['plain_config', 'p12_password']\n"
            + "PlainOpenVPN|File Only|['auth_nocache', 'cryptoapi']\n"
            + "TheGreenBow|TheGreenBow|[]\n"
            + "ViscosityVisz|Viscosity (visz)|['plain_config', 'random_local_port']",
            result
        )

    def test_with_json_obj(self):
        format = PlainOutputFormat(self._api_data_json_obj, [
            'uuid', 'name', 'type', 'proto', 'counters', 'description', 'updatefreq', 'content', 'enabled'
        ])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "24948d07-8525-4276-b497-108a0c55fcc2|zabbix_host|host|IPv4|0|Test|0.5|www.example.com,www.heise.de|1\n",
            result
        )

    def test_with_empty_data(self):
        format = PlainOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                ""
            ),
            result
        )

    def test_not_implemented(self):
        format = PlainOutputFormat("Just a String", [])
        format.separator = "|"

        self.assertRaises(NotImplementedError, format.echo)
