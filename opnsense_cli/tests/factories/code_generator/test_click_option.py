from bs4 import BeautifulSoup
from opnsense_cli.factories.code_generator.click_option import ClickOptionCodeTypeFactory, ClickText, ClickBoolean, \
    ClickInteger, ClickChoice
from opnsense_cli.tests.base import BaseTestCase
from opnsense_cli.exceptions.factory import FactoryException


class TestClickOptionCodeTypeFactory(BaseTestCase):
    def setUp(self):
        self._factory = ClickOptionCodeTypeFactory()
        self._model_data_file = self._read_fixture_file('new/command/plugin/model.xml')
        self._model_content = BeautifulSoup(self._model_data_file, "xml")

        self._UnkownField = BeautifulSoup('<enabled type="UnkownField"></enabled>', "xml")
        self._BooleanField = self._model_content.find(type="BooleanField")
        self._TextField = self._model_content.find(type="TextField")
        self._IntegerField = self._model_content.find(type="IntegerField")
        self._OptionField = self._model_content.find(type="OptionField")
        self._ModelRelationField = self._model_content.find(type="ModelRelationField")
        self._CertificateField = self._model_content.find(type="CertificateField")
        self._CSVListField = self._model_content.find(type="CSVListField")
        self._EmailField = self._model_content.find(type="EmailField")
        self._HostnameField = self._model_content.find(type="HostnameField")

    def test_UnkownField(self):
        self.assertRaises(FactoryException, self._factory.get_type_for_data, self._UnkownField)

    def test_BooleanField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._BooleanField)
        self.assertIsInstance(click_option_type_obj, ClickBoolean)

    def test_TextField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._TextField)
        self.assertIsInstance(click_option_type_obj, ClickText)

    def test_IntegerField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._IntegerField)
        self.assertIsInstance(click_option_type_obj, ClickInteger)

    def test_OptionField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._OptionField)
        self.assertIsInstance(click_option_type_obj, ClickChoice)

    def test_ModelRelationField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._ModelRelationField)
        self.assertIsInstance(click_option_type_obj, ClickText)

    def test_CertificateField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._CertificateField)
        self.assertIsInstance(click_option_type_obj, ClickText)

    def test_CSVListField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._CSVListField)
        self.assertIsInstance(click_option_type_obj, ClickText)

    def test_EmailField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._EmailField)
        self.assertIsInstance(click_option_type_obj, ClickText)

    def test_HostnameField(self):
        click_option_type_obj = self._factory.get_type_for_data(self._HostnameField)
        self.assertIsInstance(click_option_type_obj, ClickText)
