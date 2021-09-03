from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickBoolean(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}/--no-${name}',
        help=('${help}'),
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        default=${default},
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}/--no-${name}',
        help=('${help}'),
        show_default=True,
        is_flag=True,
        callback=bool_as_string,
        default=None
    )
    '''

    @property
    def _default(self):
        default = super()._default
        if default:
            return bool(default)

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()
