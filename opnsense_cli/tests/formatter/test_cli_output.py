import json
from opnsense_cli.formats.json_filter_output import JsonFilterOutputFormat
from opnsense_cli.tests.formatter.base import FormatterTestCase
from opnsense_cli.formats.json_output import JsonOutputFormat
from opnsense_cli.formats.table_output import TableOutputFormat
from opnsense_cli.formats.yaml_output import YamlOutputFormat


class TestCliOutputFormatter(FormatterTestCase):
    def setUp(self):
        self._api_data_json_empty = []
        self._api_data_json_array = [
            {
                "name": "os-acme-client",
                "version": "2.4",
                "comment": "Let's Encrypt client",
                "flatsize": "575KiB",
                "locked": "N/A",
                "license": "BSD2CLAUSE",
                "repository": "OPNsense",
                "origin": "opnsense/os-acme-client",
                "provided": "1",
                "installed": "0",
                "path": "OPNsense/opnsense/os-acme-client",
                "configured": "0"
            },
            {
                "name": "os-virtualbox",
                "version": "1.0_1",
                "comment": "VirtualBox guest additions",
                "flatsize": "525B",
                "locked": "N/A",
                "automatic": "N/A",
                "license": "BSD2CLAUSE",
                "repository": "OPNsense",
                "origin": "opnsense/os-virtualbox",
                "provided": "1",
                "installed": "1",
                "path": "OPNsense/opnsense/os-virtualbox",
                "configured": "1"
            }
        ]

        self._api_data_json_nested = {
            "ArchiveOpenVPN": {"name": "Archive", "supportedOptions": ["plain_config", "p12_password"]},
            "PlainOpenVPN": {"name": "File Only", "supportedOptions": ["auth_nocache", "cryptoapi"]},
            "TheGreenBow": {"name": "TheGreenBow", "supportedOptions": []},
            "ViscosityVisz": {"name": "Viscosity (visz)", "supportedOptions": ["plain_config", "random_local_port"]}
        }

        self._api_data_json_obj = {
            "enabled": "1",
            "name": "zabbix_host",
            "type": "host",
            "proto": "IPv4",
            "counters": "0",
            "updatefreq": "0.5",
            "content": "www.example.com,www.heise.de",
            "description": "Test",
            "uuid": "24948d07-8525-4276-b497-108a0c55fcc2"
        }

    def test_YamlFormat_with_json_array(self):
        format = YamlOutputFormat(self._api_data_json_array, ['name', 'version'])
        result = self._get_format_output(format)

        self.assertIn("- name: os-acme-client\n  version: '2.4'\n- name: os-virtualbox\n  version: '1.0_1'\n\n", result)

    def test_YamlFormat_with_json_nested(self):
        format = YamlOutputFormat(self._api_data_json_nested, ['<ID>', 'name', 'supportedOptions'])
        result = self._get_format_output(format)

        self.assertIn(
            (
                "- <ID>: ArchiveOpenVPN\n  name: Archive\n  supportedOptions: '[''plain_config'', ''p12_password'']'\n"
                "- <ID>: PlainOpenVPN\n  name: File Only\n  supportedOptions: '[''auth_nocache'', ''cryptoapi'']'\n"
                "- <ID>: TheGreenBow\n  name: TheGreenBow\n  supportedOptions: '[]'\n"
                "- <ID>: ViscosityVisz\n  name: Viscosity (visz)\n"
                "  supportedOptions: '[''plain_config'', ''random_local_port'']'\n\n"
            ),
            result
        )

    def test_YamlFormat_with_json_obj(self):
        format = YamlOutputFormat(self._api_data_json_obj, [
            'uuid', 'name', 'type', 'proto', 'counters', 'description', 'updatefreq', 'content', 'enabled'
        ])
        result = self._get_format_output(format)

        self.assertIn(
            (
                "uuid: 24948d07-8525-4276-b497-108a0c55fcc2\nname: zabbix_host\ntype: host\nproto: IPv4\n"
                "counters: '0'\ndescription: Test\nupdatefreq: '0.5'\ncontent: www.example.com,www.heise.de\n"
                "enabled: '1'\n\n"
            ),
            result
        )

    def test_YamlFormat_with_empty_data(self):
        format = YamlOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                "{}\n\n"
            ),
            result
        )

    def test_JsonFormat(self):
        format = JsonOutputFormat(self._api_data_json_array, ['name'])

        result = self._get_format_output(format)

        self.assertIn(
            f"{json.dumps(self._api_data_json_array)}\n",
            result
        )

    def test_JsonFilterFormat_with_json_array(self):
        format = JsonFilterOutputFormat(self._api_data_json_array, ['name', 'version'])

        result = self._get_format_output(format)

        self.assertIn(
            '[{"name": "os-acme-client", "version": "2.4"}, {"name": "os-virtualbox", "version": "1.0_1"}]\n',
            result
        )

    def test_JsonFilterFormat_with_json_obj(self):
        format = JsonFilterOutputFormat(self._api_data_json_obj, ['uuid', 'name'])

        result = self._get_format_output(format)

        self.assertIn(
            '{"uuid": "24948d07-8525-4276-b497-108a0c55fcc2", "name": "zabbix_host"}\n',
            result
        )

    def test_JsonFormat_with_empty_data(self):
        format = JsonOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                "[]"
            ),
            result
        )

    def test_TableFormat_with_json_array(self):
        format = TableOutputFormat(self._api_data_json_array, ['name', 'version'])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "os-acme-client|2.4\n",
            result
        )

    def test_TableFormat_with_json_nested(self):
        format = TableOutputFormat(self._api_data_json_nested, ['<ID>', 'name', 'supportedOptions'])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "ArchiveOpenVPN|Archive|['plain_config', 'p12_password']\n"
            + "PlainOpenVPN|File Only|['auth_nocache', 'cryptoapi']\n"
            + "TheGreenBow|TheGreenBow|[]\n"
            + "ViscosityVisz|Viscosity (visz)|['plain_config', 'random_local_port']",
            result
        )

    def test_TableFormat_with_json_obj(self):
        format = TableOutputFormat(self._api_data_json_obj, [
            'uuid', 'name', 'type', 'proto', 'counters', 'description', 'updatefreq', 'content', 'enabled'
        ])
        format.separator = "|"

        result = self._get_format_output(format)

        self.assertIn(
            "24948d07-8525-4276-b497-108a0c55fcc2|zabbix_host|host|IPv4|0|Test|0.5|www.example.com,www.heise.de|1\n",
            result
        )

    def test_TableFormat_with_empty_data(self):
        format = TableOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                ""
            ),
            result
        )

    def test_TableFormat_not_implemented(self):
        format = TableOutputFormat("Just a String", [])
        format.separator = "|"

        self.assertRaises(NotImplementedError, format.echo)
