from opnsense_cli.facades.code_generator.base import CodeGenerator
from opnsense_cli.parser.base import Parser
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.types.click_option.base import ClickOptionCodeFragment
from bs4.element import Tag


class ClickCommandCodeGenerator(CodeGenerator):
    IGNORED_TYPES = ['UniqueIdField']

    def __init__(self, parser: Parser, option_factory: ObjectTypeFromDataFactory, group, command):
        self._parser = parser
        self._group = group
        self._command = command
        self._tag_content: Tag = parser.parse()
        self._click_option_factory = option_factory

    def generate_code(self):
        click_options_create = []
        click_options_update = []

        for tag in self._tag_content.findChildren(recursive=False):
            if tag.attrs.get('type') in self.IGNORED_TYPES:
                continue

            click_option_type: ClickOptionCodeFragment = self._click_option_factory.get_type_for_data(tag)
            code_fragment_create = click_option_type.get_code_for_create()
            code_fragment_update = click_option_type.get_code_for_update()

            click_options_create.append(code_fragment_create)
            click_options_update.append(code_fragment_update)

            print(code_fragment_create)
            #print(code_fragment_update)

            #exit()




