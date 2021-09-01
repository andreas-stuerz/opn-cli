from opnsense_cli.types.click_option.base import ClickOptionCodeFragment


class ClickChoice(ClickOptionCodeFragment):
    TEMPLATE_CREATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        type=click.Choice(${choices}),
        multiple=${multiple},
        callback=tuple_to_csv,
        show_default=True,
        default=${default},
        ${required}
    )
    '''
    TEMPLATE_UPDATE = '''
    @click.option(
        '--${name}',
        help=('${help}'),
        type=click.Choice(${choices}),
        multiple=${multiple},
        callback=tuple_to_csv,
        show_default=True,
        default=None
    )
    '''

    @property
    def _default(self):
        default_for_multiple = self._get_default_for_multiple()

        if default_for_multiple:
            return default_for_multiple

        if super()._default:
            return f"'{super()._default}'"
        else:
            return super()._default

    def _get_default_for_multiple(self):
        if self._multiple:
            if super()._default:
                return super()._default.split(",")
            else:
                return []
        return None

    @property
    def _choices(self):
        options = self._tag_content.find('OptionValues').findChildren(recursive=False)
        choices = [option.name for option in options]

        if "False" in self._required:
            choices.insert(0, '')

        return repr(choices)

    def _render_template(self):
        return self._template.substitute(
            name=self._name,
            choices=self._choices,
            multiple=self._multiple,
            required=self._required,
            default=self._default,
            help=self._help,
        ).strip()
