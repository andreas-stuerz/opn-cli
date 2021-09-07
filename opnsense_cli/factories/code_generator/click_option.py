from bs4.element import Tag
from opnsense_cli.types.click_option.base import ClickOptionCodeFragment
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.exceptions.factory import FactoryException
from opnsense_cli.types.click_option.click_boolean import ClickBoolean
from opnsense_cli.types.click_option.click_text import ClickText
from opnsense_cli.types.click_option.click_integer import ClickInteger
from opnsense_cli.types.click_option.click_choice import ClickChoice


class ClickOptionCodeTypeFactory(ObjectTypeFromDataFactory):
    _keymap = {
        'BooleanField': ClickBoolean,
        'TextField': ClickText,
        'IntegerField': ClickInteger,
        'OptionField': ClickChoice,
        'ModelRelationField': ClickText,
        'CertificateField': ClickText,
        'CSVListField': ClickText,
        'EmailField': ClickText,
        'HostnameField': ClickText,
        'NetworkField': ClickText,
        'PortField': ClickText,
    }

    def _get_class(self, key) -> ClickOptionCodeFragment:
        click_option_class = self._keymap.get(key, None)
        if not click_option_class:
            raise FactoryException(f"Could not find class for {key} in keymap")

        return click_option_class

    def get_type_for_data(self, tag: Tag) -> ClickOptionCodeFragment:
        field_type = tag.attrs.get('type', None)
        click_option_type_class = self._get_class(field_type)

        return click_option_type_class(tag)
