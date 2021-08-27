from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from opnsense_cli.parser.base import Parser


class XmlParser(Parser):
    def __init__(self, url, tag):
        self._url = url
        self._tag = tag

    def _set_content(self):
        webpage_response = requests.get(self._url)
        webpage = webpage_response.content
        self._content = BeautifulSoup(webpage, "xml")

    def _parse_content(self) -> Tag:
        tag = self._content.find(self._tag)
        return tag
