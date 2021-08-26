from opnsense_cli.facades.code_generator.base import CodeGenerator
from opnsense_cli.parser.base import Parser
from opnsense_cli.factories.base import ObjectTypeFromDataFactory
from opnsense_cli.types.click_option.base import ClickOptionCodeFragment
from opnsense_cli.facades.template_engines.base import TemplateEngine
from opnsense_cli.dataclasses.code_generator.command import CommandTemplateVars
from bs4.element import Tag


class ClickCommandCodeGenerator(CodeGenerator):
    IGNORED_TYPES = ['UniqueIdField']
    IGNORED_TAG_NAMES_CREATE = ['name']
    IGNORED_TAG_NAMES_UPDATE = []
    COMMAND_TEMPLATE = "'code_generator/command.py.j2'"

    def __init__(
            self,
            parser: Parser,
            template_engine: TemplateEngine,
            template_for_command,
            option_factory: ObjectTypeFromDataFactory,
            group,
            command,
    ):
        self._parser = parser
        self._template_engine = template_engine
        self._template_for_command = template_for_command
        self._click_group = group
        self._click_command = command
        self._tag_content: Tag = parser.parse()
        self._click_option_factory = option_factory

    def generate_code(self):
        command_code = self.generate_command()
        print(command_code)

    def generate_command(self):
        template_vars = self._get_template_vars()
        self._template_engine.vars = template_vars
        self._template_engine.set_template_from_file(self._template_for_command)
        return self._template_engine.render()

    def _get_template_vars(self):
        click_options_create = []
        click_options_update = []
        column_names = []

        for tag in self._tag_content.findChildren(recursive=False):
            if tag.attrs.get('type') in self.IGNORED_TYPES:
                continue

            column_names.append(tag.name)

            click_option_type: ClickOptionCodeFragment = self._click_option_factory.get_type_for_data(tag)

            create_option_code = self._get_click_option_create_code(tag, click_option_type)
            if create_option_code:
                click_options_create.append(create_option_code)

            update_option_code = self._get_click_option_create_code(tag, click_option_type)
            if update_option_code:
                click_options_update.append(update_option_code)

        return CommandTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            click_options_create=click_options_create,
            click_options_update=click_options_update,
            column_names=column_names,
            column_list=repr(column_names)
        )

    def _get_click_option_create_code(self, tag, click_option_type: ClickOptionCodeFragment):
        if tag.name in self.IGNORED_TAG_NAMES_CREATE:
            return None

        return click_option_type.get_code_for_create()

    def _get_click_option_update_code(self, tag, click_option_type: ClickOptionCodeFragment):
        if tag.name in self.IGNORED_TAG_NAMES_UPDATE:
            return None

        return click_option_type.get_code_for_update()
