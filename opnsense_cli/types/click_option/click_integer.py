from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickInteger(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        type=int,
        callback=int_as_string,
        default=${default},
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        type=int,
        callback=int_as_string,
        default=None
    )
    '''

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()
