
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.syslog import Service


class SyslogStatsFacade(CommandFacade):
    def __init__(self, service_api: Service):
        super().__init__()
        self._service_api = service_api

    def show_stats(self, search):
        stats_output = self._service_api.stats()['rows']

        if search:
            return self._search_list_of_dicts_by_val(stats_output, search)

        return stats_output
