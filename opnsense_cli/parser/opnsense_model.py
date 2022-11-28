from bs4.element import Tag
from opnsense_cli.parser.xml import XmlParser


class OpnsenseModelParser(XmlParser):
    def _parse_content(self) -> Tag:
        print(self._content)
        return self._content.find(self._tag, type=None).findChild()
