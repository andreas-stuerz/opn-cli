from opnsense_cli.api.plugin.haproxy import Settings
from opnsense_cli.api.plugin.haproxy import Export
from opnsense_cli.api.plugin.haproxy import Service
from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade


class HaproxyConfigFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, export_api: Export, service_api: Service):
        self._settings_api = settings_api
        self._export_api = export_api
        self._service_api = service_api

    def show_config(self):
        return self._export_api.config()

    def test_config(self):
        return self._service_api.configtest()

    def apply_config(self):
        self._apply()
        return {"status": "ok"}

    def show_diff(self):
        return self._export_api.diff()

    def download_config(self, path):
        config = self._export_api.download('all')
        self._write_base64_string_to_zipfile(path, config['content'])
        return {
            "status": f"sucessfully saved zip to: {path}"
        }
