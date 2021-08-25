from opnsense_cli.types.click_option.base import ClickOptionCodeFragment

class ClickText(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help='<TODO>',
        show_default=True,
        ${default}
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help='<TODO>',
        show_default=True,
        default=None
    )
    '''

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            required=self._required,
            default=self._default
        ).strip()
