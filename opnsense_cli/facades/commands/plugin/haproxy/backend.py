from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyBackendFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_backends(self):
        return self._get_backend_list()

    def show_backend(self, uuid):
        backends = self._get_backend_list()
        backend = next((item for item in backends if item["uuid"] == uuid), {})
        return backend

    def _get_backend_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.backends.backend'
        uuid_resolver_map = {
            "linkedServers": {
                "template": "$.haproxy.servers.server[{uuids}].name",
                "insert_as_key": "Servers"
            },
            "linkedResolver": {
                "template": "$.haproxy.resolvers.resolver[{uuids}].name",
                "insert_as_key": "Resolver"
            },
            "linkedMailer": {
                "template": "$.haproxy.mailers.mailer[{uuids}].name",
                "insert_as_key": "Mailer"
            },
            "linkedActions": {
                "template": "$.haproxy.actions.action[{uuids}].name",
                "insert_as_key": "Actions"
            },
            "linkedErrorfiles": {
                "template": "$.haproxy.errorfiles.errorfile[{uuids}].name",
                "insert_as_key": "Errorfiles"
            },
            "healthCheck": {
                "template": "$.haproxy.healthchecks.healthcheck[{uuids}].name",
                "insert_as_key": "health_check"
            },
        }
        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_backend(self, json_payload: dict):
        result = self._settings_api.addBackend(json=json_payload)
        self._apply(result)
        return result

    def update_backend(self, uuid, json_payload: dict):
        result = self._settings_api.setBackend(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_backend(self, uuid):
        result = self._settings_api.delBackend(uuid)
        self._apply(result)
        return result
