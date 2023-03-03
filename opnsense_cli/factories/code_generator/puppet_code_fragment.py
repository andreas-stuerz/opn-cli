from bs4.element import Tag
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.exceptions.factory import FactoryException
from opnsense_cli.types.puppet.base import PuppetCodeFragment
from opnsense_cli.types.puppet.puppet_boolean import PuppetBoolean
from opnsense_cli.types.puppet.puppet_choice import PuppetChoice
from opnsense_cli.types.puppet.puppet_string import PuppetString


class PuppetCodeFragmentFactory(ObjectTypeFromDataFactory):
    _keymap = {
        'String': PuppetString,
        'Bool': PuppetBoolean,
        'Choice': PuppetChoice,

    }

    def _get_class(self, key) -> PuppetCodeFragment:
        click_option_class = self._keymap.get(key, None)
        if not click_option_class:
            raise FactoryException(f"Could not find class for {key} in keymap")

        return click_option_class

    def get_type_for_data(self, params) -> PuppetCodeFragment:
        puppet_code_fragment_type_class = self._get_class(params['type']['param_type'])

        return puppet_code_fragment_type_class(params)
