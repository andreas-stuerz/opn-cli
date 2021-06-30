import io
import sys
import unittest
from opnsense_cli.formats.json_output import JsonOutputFormat
from opnsense_cli.formats.table_output import TableOutputFormat


class TestCliOutputFormatter(unittest.TestCase):
    def setUp(self):
        self._api_data_json_obj_list = {
            "plugin": [
                {
                    'name': 'os-acme-client', 'version': '2.4', 'comment': "Let's Encrypt client",
                    'flatsize': '575KiB', 'locked': 'N/A', 'license': 'BSD2CLAUSE',
                    'repository': 'OPNsense', 'origin': 'opnsense/os-acme-client',
                    'provided': '1', 'installed': '0', 'path': 'OPNsense/opnsense/os-acme-client', 'configured': '0'
                },
            ],
        }

        self._api_data_json_nested = {
            'ArchiveOpenVPN': {'name': 'Archive', 'supportedOptions': ['plain_config', 'p12_password']},
            'PlainOpenVPN': {'name': 'File Only', 'supportedOptions': ['auth_nocache', 'cryptoapi']},
            'TheGreenBow': {'name': 'TheGreenBow', 'supportedOptions': []},
            'ViscosityVisz': {'name': 'Viscosity (visz)', 'supportedOptions': ['plain_config', 'random_local_port']}
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

    def test_JsonFormat(self):
        """
        JSON Formatter always return all columns
        """
        formatter = JsonOutputFormat(self._api_data_json_obj_list['plugin'], ['name'])

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            '[{"name": "os-acme-client", "version": "2.4", ' +
            '"comment": "Let\'s Encrypt client", "flatsize": "575KiB", "locked": "N/A", ' +
            '"license": "BSD2CLAUSE", "repository": "OPNsense", "origin": "opnsense/os-acme-client", ' +
            '"provided": "1", "installed": "0", "path": "OPNsense/opnsense/os-acme-client", ' +
            '"configured": "0"}]\n',
            result
        )

    def test_TableFormat_with_json_array(self):
        formatter = TableOutputFormat(self._api_data_json_obj_list['plugin'], ['name', 'version'])
        formatter.separator = "|"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            "os-acme-client|2.4\n",
            result
        )

    def test_TableFormat_with_json_nested(self):
        formatter = TableOutputFormat(self._api_data_json_nested, ['<ID>', 'name', 'supportedOptions'])
        formatter.separator = "|"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            "ArchiveOpenVPN|Archive|['plain_config', 'p12_password']\n"
            + "PlainOpenVPN|File Only|['auth_nocache', 'cryptoapi']\n"
            + "TheGreenBow|TheGreenBow|[]\n"
            + "ViscosityVisz|Viscosity (visz)|['plain_config', 'random_local_port']",
            result
        )

    def test_TableFormat_with_json_obj(self):
        formatter = TableOutputFormat(self._api_data_json_obj, [
            'uuid', 'name', 'type', 'proto', 'counters', 'description', 'updatefreq', 'content', 'enabled'
        ])
        formatter.separator = "|"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            "24948d07-8525-4276-b497-108a0c55fcc2|zabbix_host|host|IPv4|0|Test|0.5|www.example.com,www.heise.de|1\n",
            result
        )

    def test_TableFormat_not_implemented(self):
        formatter = TableOutputFormat("Just a String", [])
        formatter.separator = "|"

        self.assertRaises(NotImplementedError, formatter.echo)
