from opnsense_cli.parser.html import HtmlParser


class OpnsenseModuleListParser(HtmlParser):
    def __init__(self, url):
        super().__init__(url, "a")
        self.module_list = self._list_all_modules()

    def _list_all_modules(self):
        super()._set_content()
        links = self._content.find_all(self._tag, href=True)
        module_list = []
        for link in links:
            if link['href'].endswith(".rst"):
                url_component_list = link['href'].split("/")
                module = self._get_module(url_component_list)
                module_list.append(module)
        return module_list

    def _get_module(self, url_components):
        if len(url_components) > 2:
            module_type = url_components[-2]
            if (module_type == "plugins" or module_type == "core"):
                return url_components[-1].split(".")[0]
