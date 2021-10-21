from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickTextLinkedItem(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        callback=resolve_linked_names_to_uuids,
        show_default=True,
        default=${default},
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        callback=resolve_linked_names_to_uuids,
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
