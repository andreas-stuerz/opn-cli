from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyActionFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.actions.action'
    uuid_resolver_map = {
        'linkedAcls': {'template': '$.haproxy.acls.acl[{uuids}].name', 'insert_as_key': 'Acls'},
        'use_backend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'Backend'},
        'use_server': {'template': '$.haproxy.servers.server[{uuids}].name', 'insert_as_key': 'Server'},
        'useBackend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'Backends'},
        'useServer': {'template': '$.haproxy.servers.server[{uuids}].name', 'insert_as_key': 'Servers'},
        'map_use_backend_file':
            {'template': '$.haproxy.mapfiles.mapfile[{uuids}].name', 'insert_as_key': 'Mapfile'},
        'map_use_backend_default':
            {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'BackendDefault'},
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_actions(self):
        return self._get_actions_list()

    def show_action(self, uuid):
        actions = self._get_actions_list()
        action = next((item for item in actions if item["uuid"] == uuid), {})
        return action

    def _get_actions_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

    def create_action(self, json_payload: dict):
        result = self._settings_api.addAction(json=json_payload)
        self._apply(result)
        return result

    def update_action(self, uuid, json_payload: dict):
        result = self._settings_api.setAction(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_action(self, uuid):
        result = self._settings_api.delAction(uuid)
        self._apply(result)
        return result
