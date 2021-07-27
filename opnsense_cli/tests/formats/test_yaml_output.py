from opnsense_cli.tests.formats.base import FormatTestCase
from opnsense_cli.formats.yaml_output import YamlOutputFormat


class TestYamlOutputFormat(FormatTestCase):
    def test_with_json_array(self):
        format = YamlOutputFormat(self._api_data_json_array, ['name', 'version'])
        result = self._get_format_output(format)

        self.assertIn("- name: os-acme-client\n  version: '2.4'\n- name: os-virtualbox\n  version: '1.0_1'\n\n", result)

    def test_with_json_nested(self):
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

    def test_with_json_obj(self):
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

    def test_with_empty_data(self):
        format = YamlOutputFormat(self._api_data_json_empty, ['name', 'version'])
        result = self._get_format_output(format)
        self.assertIn(
            (
                "{}\n\n"
            ),
            result
        )
