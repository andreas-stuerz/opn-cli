from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyServerFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.servers.server'
    uuid_resolver_map = {
        'linkedResolver': {'template': '$.haproxy.resolvers.resolver[{uuids}].name', 'insert_as_key': 'Resolver'},
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_servers(self):
        return self._get_servers_list()

    def show_server(self, uuid):
        servers = self._get_servers_list()
        server = next((item for item in servers if item["uuid"] == uuid), {})
        return server

    def _get_servers_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

    def create_server(self, json_payload: dict):
        result = self._settings_api.addServer(json=json_payload)
        self._apply(result)
        return result

    def update_server(self, uuid, json_payload: dict):
        result = self._settings_api.setServer(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_server(self, uuid):
        result = self._settings_api.delServer(uuid)
        self._apply(result)
        return result
