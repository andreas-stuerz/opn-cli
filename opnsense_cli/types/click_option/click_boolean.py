from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickBoolean(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}/--no-${name}',
        help='ToDo',
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        ${default}
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}/--no-${name}',
        help='ToDo',
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        default=None
    )
    '''

    @property
    def _default(self):
        if self._tag_content.find('default'):
            return f"default={bool(self._tag_content.default.string)},"
        return "default=None,"

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default
        ).strip()
