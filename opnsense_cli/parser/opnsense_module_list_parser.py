from opnsense_cli.parser.base import Parser
import json
from bs4.element import Tag


class OpnsenseModuleListParser(Parser):
    def __init__(self, parsed_html_tag_from_gh: Tag):
        self._parsed_html_tag_from_gh = parsed_html_tag_from_gh
    def _set_content(self):
        json_content = self._parsed_html_tag_from_gh.string.strip()
        self._content = json.loads(json_content)
    def _parse_content(self) -> dict:
        return [item["name"].split(".")[0] for item in self._content["payload"]["tree"]["items"]]
