import io
import sys
import unittest
from opnsense_cli.command.format import JsonFormat, TableFormat


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self._api_data_fixtures = {
            "plugin": [
                {
                    'name': 'os-acme-client', 'version': '2.4', 'comment': "Let's Encrypt client",
                    'flatsize': '575KiB', 'locked': 'N/A', 'license': 'BSD2CLAUSE',
                    'repository': 'OPNsense', 'origin': 'opnsense/os-acme-client',
                    'provided': '1', 'installed': '0', 'path': 'OPNsense/opnsense/os-acme-client', 'configured': '0'
                },
            ],
        }

    def test_JsonFormat(self):
        # JSON Formatter always return all columns
        formatter = JsonFormat(self._api_data_fixtures['plugin'], ['name'])

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

    def test_TableFormat(self):
        formatter = TableFormat(self._api_data_fixtures['plugin'], ['name', 'version'])
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
