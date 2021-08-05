from opnsense_cli.facades.base import CommandFacade
from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.api.plugin.haproxy import Settings
from opnsense_cli.api.plugin.haproxy import Export


class HaproxyServerFacade(CommandFacade):
    def __init__(self, settings_api: Settings, export_api: Export):
        self._settings_api = settings_api
        self._export_api = export_api

    def list_server(self):
        return self._export_api.config()
