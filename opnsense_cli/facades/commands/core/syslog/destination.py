from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.syslog import Settings, Service


class SyslogDestinationFacade(CommandFacade):
    jsonpath_base = '$.syslog.destinations.destination'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_destinations(self):
        return self._get_destinations_list()

    def show_destination(self, uuid):
        destinations = self._get_destinations_list()
        destination = next((item for item in destinations if item["uuid"] == uuid), {})
        return destination

    def _get_destinations_list(self):
        return self._api_mutable_model_get(
            self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map, sort_by='uuid'
        )

    def create_destination(self, json_payload: dict):
        result = self._settings_api.addDestination(json=json_payload)
        self._apply(result)
        return result

    def update_destination(self, uuid, json_payload: dict):
        result = self._settings_api.setDestination(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_destination(self, uuid):
        result = self._settings_api.delDestination(uuid)
        self._apply(result)
        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._service_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
