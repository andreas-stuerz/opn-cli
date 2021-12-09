from bs4 import BeautifulSoup
import requests
from opnsense_cli.parser.html import HtmlParser


class OpnsenseApiReferenceParser(HtmlParser):
    def __init__(self, url, tag, module_name):
        super().__init__(url, tag)
        self._module_name = module_name

    def _parse_content(self) -> dict:
        controller_html_tables = super()._parse_content()
        return self._get_api_endpoints(controller_html_tables)

    def _set_content(self):
        super()._set_content()
        github_url = 'https://github.com'
        links = self._content.find_all('a', href=True)
        for link in links:
            if link["href"].endswith(".rst"):
                url_component_list = link['href'].split("/")
                if self._check_url_components(url_component_list):
                    webpage_plugin_response = requests.get(github_url + link['href'], verify=True)
                    webpage_plugin = webpage_plugin_response.content
                    self._content = BeautifulSoup(webpage_plugin, 'html.parser')

    def _check_url_components(self, url_components):
        if len(url_components) > 2:
            module_type = url_components[-2]
            if (module_type == "plugins" or module_type == "core"):
                if url_components[-1].split(".")[0] == self._module_name:
                    return True

    def _get_controller_names_dict(self, tables):
        controllers = {}
        for table in tables:
            controller = table.find("tbody").find_next("tr").find_all("td")[2].get_text(strip=True)
            if controller != '':
                controllers[controller] = []
        return controllers

    def _get_table_rows(self, tables):
        table_rows = []
        for table in tables:
            for table_body in table.find_all("tbody"):
                table_rows.append(table_body.find_all("tr"))
        return table_rows

    def _make_api_endpoint(self, row_content):
        api_endpoint = {}
        api_endpoint['method'] = row_content[0].get_text(strip=True)
        api_endpoint['module'] = row_content[1].get_text(strip=True)
        api_endpoint['controller'] = row_content[2].get_text(strip=True)
        api_endpoint['command'] = row_content[3].get_text(strip=True)
        parameters = row_content[4].get_text(strip=True)
        if parameters:
            api_endpoint['parameters'] = self._get_parameters(parameters)
        return api_endpoint

    def _get_api_endpoints(self, tables):
        controllers = self._get_controller_names_dict(tables)
        table_rows_list = self._get_table_rows(tables)
        for table_rows in table_rows_list:
            for table_row in table_rows:
                row_content = table_row.find_all("td")
                controller = row_content[2].get_text(strip=True)
                if self._skip_empty_row(row_content[0].get_text(strip=True)):
                    continue
                api_endpoint = self._make_api_endpoint(row_content)
                controllers[controller].append(api_endpoint)
        return controllers

    def _skip_empty_row(self, table_data_cell):
        if table_data_cell == '' or "uses" in table_data_cell:
            return True

    def _get_parameters(self, parameters):
        if "," in parameters:
            return parameters.split(',')
        else:
            return parameters
