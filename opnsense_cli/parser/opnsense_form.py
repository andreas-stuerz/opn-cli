from opnsense_cli.parser.xml import XmlParser


class OpnsenseFormParser(XmlParser):
    def _parse_content(self):
        base_tag = super()._parse_content()
        return self.get_help_messages_with_id(base_tag)

    def get_help_messages_with_id(self, base_tag):
        messages = {}
        for field in base_tag.findChildren(recursive=False):
            if self._skip_field(field):
                continue

            field_id = field.id.string.split('.')[-1]
            field_help = field.help.string.replace("'", "\\'")

            messages.update({
                field_id: field_help
            })

        return messages

    def _skip_field(self, field):
        if field.find(name='type', text='header'):
            return True

        if not field.find(name='id'):
            return True

        if not field.find(name='help'):
            return True

        return False
