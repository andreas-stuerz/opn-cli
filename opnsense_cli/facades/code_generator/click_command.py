from opnsense_cli.facades.code_generator.base import CommandCodeGenerator
from opnsense_cli.types.click_option.base import ClickOptionCodeFragment
from opnsense_cli.dataclasses.code_generator.command.command_vars import CommandTemplateVars


class ClickCommandCodeGenerator(CommandCodeGenerator):
    IGNORED_TYPES = ['UniqueIdField']
    IGNORED_TAG_NAMES_CREATE = ['name']

    def __init__(self, *args):
        super().__init__(*args)
        self.__help_messages = None

    @property
    def _help_messages(self):
        if self.__help_messages is None:
            return {}
        return self.__help_messages

    @_help_messages.setter
    def help_messages(self, messages: dict):
        self.__help_messages = messages

    def _get_template_vars(self):
        click_options_create = []
        click_options_update = []
        column_names = []

        for tag in self._tag_content.findChildren(recursive=False):
            if tag.attrs.get('type') in self.IGNORED_TYPES:
                continue

            column_names.append(tag.name)

            click_option_type: ClickOptionCodeFragment = self._click_option_factory.get_type_for_data(tag)
            click_option_type.help = self._help_messages.get(tag.name, None)

            create_option_code = self._get_click_option_create_code(tag, click_option_type)
            if create_option_code:
                click_options_create.append(create_option_code)

            update_option_code = self._get_click_option_update_code(click_option_type)
            if update_option_code:
                click_options_update.append(update_option_code)

        return CommandTemplateVars(
            click_command=self._click_command,
            click_group=self._click_group,
            click_options_create=click_options_create,
            click_options_update=click_options_update,
            column_names=column_names,
            column_list=repr(column_names),
            module_type=self._module_type
        )

    def _get_click_option_create_code(self, tag, click_option_type: ClickOptionCodeFragment):
        if tag.name in self.IGNORED_TAG_NAMES_CREATE:
            return None

        return click_option_type.get_code_for_create()

    def _get_click_option_update_code(self, click_option_type: ClickOptionCodeFragment):
        return click_option_type.get_code_for_update()
