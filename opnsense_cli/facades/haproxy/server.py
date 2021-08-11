from opnsense_cli.facades.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service
from opnsense_cli.api.plugin.haproxy import Export


class HaproxyServerFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, export_api: Export, service_api: Service):
        self._settings_api = settings_api
        self._export_api = export_api
        self._service_api = service_api

    def list_server(self):
        return self._get_servers_list()

    def show_server(self, uuid):
        servers = self._get_servers_list()
        server = next((item for item in servers if item["uuid"] == uuid), {})
        return server

    def _get_servers_list(self):
        raw_servers = dict(self._settings_api.get()['haproxy']['servers']['server'])

        servers = []
        for uuid, server_raw in raw_servers.items():
            server = self._api_mutable_model_get_items_to_json(server_raw)
            server.update({'uuid': uuid})
            servers.append(server)

        servers = self._sort_dict_by_string(servers, 'name')
        return servers

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
