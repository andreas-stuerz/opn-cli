from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.unbound import Settings, Service


class UnboundHostFacade(CommandFacade):
    jsonpath_base = '$.unbound.hosts.host'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_hosts(self):
        return self._get_hosts_list()

    def show_host(self, uuid):
        hosts = self._get_hosts_list()
        host = next((item for item in hosts if item["uuid"] == uuid), {})
        return host

    def _get_hosts_list(self):
        return self._api_mutable_model_get(
            self._complete_model_data,
            self.jsonpath_base,
            self.uuid_resolver_map,
            sort_by='uuid'
        )

    def create_host(self, json_payload: dict):
        result = self._settings_api.addHostOverride(json=json_payload)
        self._apply(result)
        return result

    def update_host(self, uuid, json_payload: dict):
        result = self._settings_api.setHostOverride(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_host(self, uuid):
        result = self._settings_api.delHostOverride(uuid)
        self._apply(result)
        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._service_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
