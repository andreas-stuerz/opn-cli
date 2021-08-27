from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickChoice(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help='ToDo',
        type=click.Choice(${choices}),
        ${multiple}
        show_default=True,
        ${default}
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help='ToDo',
        type=click.Choice(${choices}),
        ${multiple}
        show_default=True,
        default=None
    )
    '''

    @property
    def _choices(self):
        options = self._tag_content.find('OptionValues').findChildren(recursive=False)
        choices = [option.name for option in options]

        if "False" in self._required:
            choices.insert(0, '')

        return repr(choices)

    @property
    def _default(self):
        if self._tag_content.find('default'):
            return f"default='{self._tag_content.default.string}',"
        return "default=None,"

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            choices=self._choices,
            multiple=self._multiple,
            required=self._required,
            default=self._default
        ).strip()
