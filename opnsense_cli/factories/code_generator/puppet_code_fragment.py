from bs4.element import Tag
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.exceptions.factory import FactoryException
from opnsense_cli.types.puppet.base import PuppetCodeFragment
from opnsense_cli.types.puppet.puppet_boolean import PuppetBoolean
from opnsense_cli.types.puppet.puppet_choice import PuppetChoice
from opnsense_cli.types.puppet.puppet_choice_multiple import PuppetChoiceMultiple
from opnsense_cli.types.puppet.puppet_csv import PuppetCsv
from opnsense_cli.types.puppet.puppet_integer import PuppetInteger
from opnsense_cli.types.puppet.puppet_string import PuppetString


class PuppetCodeFragmentFactory(ObjectTypeFromDataFactory):
    _keymap = {
        'String': PuppetString,
        'Bool': PuppetBoolean,
        'Choice': PuppetChoice,
        'ChoiceMultiple': PuppetChoiceMultiple,
        'IntOrEmptyClick': PuppetInteger,
        'Csv': PuppetCsv,
    }

    def _get_class(self, key) -> PuppetCodeFragment:
        click_option_class = self._keymap.get(key, None)
        if not click_option_class:
            raise FactoryException(f"Could not find class for {key} in keymap")

        return click_option_class

    def get_type_for_data(self, params, find_uuid_by_column, click_group, click_command) -> PuppetCodeFragment:
        param_type = params['type']['param_type']
        if params['multiple']:
            param_type = f"{param_type}Multiple"

        puppet_code_fragment_type_class = self._get_class(param_type)

        return puppet_code_fragment_type_class(params, find_uuid_by_column, click_group, click_command)
