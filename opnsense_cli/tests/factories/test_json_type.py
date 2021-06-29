import unittest
from opnsense_cli.factories.json_type import JsonTypeFactory, JsonObj, JsonArray, JsonObjNested


class TestJsonTypeFactory(unittest.TestCase):
    def setUp(self):
        self._factory = JsonTypeFactory()
        self._should_be_json_obj = [
            {
                "result": "failed",
                "validations": {
                    "alias.name": "An alias with this name already exists."
                }
            },
        ]
        self._should_be_json_array = [
            {
                "use_same_key_for_each_example": [
                    {
                        'name': 'os-acme-client', 'version': '2.4', 'comment': "Let's Encrypt client",
                        'flatsize': '575KiB', 'locked': 'N/A', 'license': 'BSD2CLAUSE',
                        'repository': 'OPNsense', 'origin': 'opnsense/os-acme-client',
                        'provided': '1', 'installed': '0', 'path': 'OPNsense/opnsense/os-acme-client', 'configured': '0'
                    },
                ],
            }
        ]
        self._should_be_json_nested = [
            {
                'ArchiveOpenVPN': {'name': 'Archive', 'supportedOptions': ['plain_config', 'p12_password']},
                'PlainOpenVPN': {'name': 'File Only', 'supportedOptions': ['auth_nocache', 'cryptoapi']},
                'TheGreenBow': {'name': 'TheGreenBow', 'supportedOptions': []},
                'ViscosityVisz': {'name': 'Viscosity (visz)', 'supportedOptions': ['plain_config', 'random_local_port']}
            }
        ]

    def test_JsonTypeFactory_returns_JsonObj(self):
        for json_data in self._should_be_json_obj:
            json_type_obj = self._factory.get_type_for_data(json_data)
            self.assertIsInstance(json_type_obj, JsonObj)

    def test_JsonTypeFactory_returns_JsonArray(self):
        for json_data in self._should_be_json_array:
            json_type_obj = self._factory.get_type_for_data(json_data['use_same_key_for_each_example'])
            self.assertIsInstance(json_type_obj, JsonArray)

    def test_JsonTypeFactory_returns_JsonObjNested(self):
        for json_data in self._should_be_json_nested:
            json_type_obj = self._factory.get_type_for_data(json_data)
            self.assertIsInstance(json_type_obj, JsonObjNested)
