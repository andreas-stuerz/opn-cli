from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickText(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        default=${default},
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        show_default=True,
        default=None
    )
    '''

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=f"'{self._default}'" if self._default else self._default,
            help=self._help,
        ).strip()
