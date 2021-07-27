import io
import sys
import unittest

from opnsense_cli.formats.base import Format


class FormatTestCase(unittest.TestCase):
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

    def _get_format_output(self, format: Format):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        format.echo()
        sys.stdout = sys.__stdout__
        result = capturedOutput.getvalue()

        return result
