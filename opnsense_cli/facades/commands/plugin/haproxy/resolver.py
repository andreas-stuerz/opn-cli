from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyResolverFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_resolvers(self):
        return self._get_resolvers_list()

    def show_resolver(self, uuid):
        resolvers = self._get_resolvers_list()
        resolver = next((item for item in resolvers if item["uuid"] == uuid), {})
        return resolver

    def _get_resolvers_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.resolvers.resolver'
        uuid_resolver_map = {
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_resolver(self, json_payload: dict):
        result = self._settings_api.addresolver(json=json_payload)
        self._apply(result)
        return result

    def update_resolver(self, uuid, json_payload: dict):
        result = self._settings_api.setresolver(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_resolver(self, uuid):
        result = self._settings_api.delresolver(uuid)
        self._apply(result)
        return result
