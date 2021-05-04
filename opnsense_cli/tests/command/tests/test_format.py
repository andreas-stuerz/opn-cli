import io
import sys
import unittest
from opnsense_cli.command.format import JsonFormat, TableFormat


class TestFormatter(unittest.TestCase):
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
            'result': 'ok', 'changed': False, 'filename': 'Dial_In_VPN.ovpn', 'filetype': 'text/plain',
            'content': 'ZUVXXXXHR1bYYYwZXJzaXN0LXR1bgpwZXJzaXN0LWt=='
        }

    def test_JsonFormat(self):
        """
        JSON Formatter always return all columns
        """
        formatter = JsonFormat(self._api_data_json_obj_list['plugin'], ['name'])

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            '[{\'name\': \'os-acme-client\', \'version\': \'2.4\', ' +
            '\'comment\': "Let\'s Encrypt client", \'flatsize\': \'575KiB\', \'locked\': \'N/A\', ' +
            '\'license\': \'BSD2CLAUSE\', \'repository\': \'OPNsense\', \'origin\': \'opnsense/os-acme-client\', ' +
            '\'provided\': \'1\', \'installed\': \'0\', \'path\': \'OPNsense/opnsense/os-acme-client\', ' +
            '\'configured\': \'0\'}]\n',
            result
        )

    def test_TableFormat_with_json_obj_list(self):
        formatter = TableFormat(self._api_data_json_obj_list['plugin'], ['name', 'version'])
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
        formatter = TableFormat(self._api_data_json_nested, ['<ID>', 'name', 'supportedOptions'])
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
        formatter = TableFormat(self._api_data_json_obj, ['result', 'changed', 'filename'])
        formatter.separator = "|"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        formatter.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        self.assertIn(
            "ok|False|Dial_In_VPN.ovpn\n",
            result
        )

    def test_TableFormat_not_implemented(self):
        formatter = TableFormat("Just a String", [])
        formatter.separator = "|"

        self.assertRaises(NotImplementedError, formatter.echo)
