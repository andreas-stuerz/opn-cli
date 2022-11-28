from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.plugin.nodeexporter import General, Service


class NodeexporterConfigFacade(CommandFacade):
    jsonpath_base = '$.general'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: General, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def show_config(self):
        return self._settings_api.get()['general']

    def edit_config(self, json_payload: dict):
        result = self._settings_api.set(json=json_payload)
        self._apply(result)

        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._service_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
