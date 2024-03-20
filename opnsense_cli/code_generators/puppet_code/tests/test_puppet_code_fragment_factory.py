from opnsense_cli.code_generators.puppet_code.factories import PuppetCodeFragmentFactory
from opnsense_cli.tests.base import BaseTestCase
from opnsense_cli.factories import FactoryException


class TestPuppetCodeFragmentTypeFactory(BaseTestCase):
    def setUp(self):
        self._factory = PuppetCodeFragmentFactory()
        self._unknown_key = "unknown_key"

    def test_unknown_key(self):
        self.assertRaises(FactoryException, self._factory._get_class, self._unknown_key)
