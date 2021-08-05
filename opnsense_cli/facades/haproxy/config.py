from opnsense_cli.facades.base import CommandFacade
from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.api.plugin.haproxy import Settings
from opnsense_cli.api.plugin.haproxy import Export


class HaproxyConfigFacade(CommandFacade):
    def __init__(self, settings_api: Settings, export_api: Export):
        self._settings_api = settings_api
        self._export_api = export_api

    def show_config(self):
        return self._export_api.config()

    def show_diff(self):
        return self._export_api.diff()

    def download_config(self, path):
        config = self._export_api.download('all')
        self._write_base64_string_to_zipfile(path, config['content'])
        return {
            "status": f"sucessfully saved zip to: {path}"
        }
