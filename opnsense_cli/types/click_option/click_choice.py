from opnsense_cli.types.click_option.base import ClickOptionCodeFragment

class ClickChoice(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help='<TODO>',
        type=click.Choice(${choices}),
        show_default=True,
        ${default}
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help='<TODO>',
        type=click.Choice(${choices}),
        show_default=True,
        default=None
    )
    '''

    @property
    def _choices(self):
        choices = self._tag_content.find('OptionValues').findChildren(recursive=False)

        return repr([choice.name for choice in choices])

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            choices=self._choices,
            required=self._required,
            default=self._default
        ).strip()
