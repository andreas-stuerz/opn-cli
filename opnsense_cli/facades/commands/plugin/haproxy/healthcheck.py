from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyHealthcheckFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_healthchecks(self):
        return self._get_healthchecks_list()

    def show_healthcheck(self, uuid):
        healthchecks = self._get_healthchecks_list()
        healthcheck = next((item for item in healthchecks if item["uuid"] == uuid), {})
        return healthcheck

    def _get_healthchecks_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.healthchecks.healthcheck'
        uuid_resolver_map = {
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_healthcheck(self, json_payload: dict):
        result = self._settings_api.addHealthcheck(json=json_payload)
        self._apply(result)
        return result

    def update_healthcheck(self, uuid, json_payload: dict):
        result = self._settings_api.setHealthcheck(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_healthcheck(self, uuid):
        result = self._settings_api.delHealthcheck(uuid)
        self._apply(result)
        return result
