from bs4.element import Tag
from opnsense_cli.parser.xml import XmlParser


class OpnsenseModelParser(XmlParser):
    def _parse_content(self) -> Tag:
        return self._content.find(self._tag, type=None).findChild()
