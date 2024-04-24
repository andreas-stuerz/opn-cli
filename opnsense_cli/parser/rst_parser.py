from bs4 import BeautifulSoup
import requests
from opnsense_cli.parser.base import Parser
from docutils import core

class RstParser(Parser):
    def __init__(self, url, html_selector, find_all=True):
        self._url = url
        self._html_selector = html_selector
        self._find_all = find_all

    def _set_content(self):
        webpage_response = requests.get(self._url, verify=True)
        rst_content = webpage_response.content
        html_content = core.publish_string(rst_content, writer_name='html')
        self._content = BeautifulSoup(html_content, "html.parser")

    def _parse_content(self):
        elements = self._content.select(self._html_selector) if self._find_all else self._content.select_one(self._html_selector)
        return elements
