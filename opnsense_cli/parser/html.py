from bs4 import BeautifulSoup
import requests
from opnsense_cli.parser.base import Parser


class HtmlParser(Parser):
    def __init__(self, url, tag):
        self._url = url
        self._tag = tag

    def _set_content(self):
        webpage_response = requests.get(self._url, verify=True)
        webpage = webpage_response.content
        self._content = BeautifulSoup(webpage, 'html.parser')

    def _parse_content(self):
        tags = self._content.find_all(self._tag)
        return tags
