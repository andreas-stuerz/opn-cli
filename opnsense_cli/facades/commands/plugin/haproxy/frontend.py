from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyFrontendFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_frontends(self):
        return self._get_frontends_list()

    def show_frontend(self, uuid):
        frontends = self._get_frontends_list()
        frontend = next((item for item in frontends if item["uuid"] == uuid), {})
        return frontend

    def _get_frontends_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.frontends.frontend'
        uuid_resolver_map = dict(
            defaultBackend={'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'Backend'},
            basicAuthUsers={'template': '$.haproxy.users.user[{uuids}].name', 'insert_as_key': 'Users'},
            basicAuthGroups={'template': '$.haproxy.groups.group[{uuids}].name', 'insert_as_key': 'Groups'},
            linkedCpuAffinityRules={'template': '$.haproxy.cpus.cpu[{uuids}].name', 'insert_as_key': 'Cpus'},
            linkedActions={'template': '$.haproxy.actions.action[{uuids}].name', 'insert_as_key': 'Actions'},
            linkedErrorfiles={'template': '$.haproxy.errorfiles.errorfile[{uuids}].name',
                              'insert_as_key': 'Errorfiles'})

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_frontend(self, json_payload: dict):
        result = self._settings_api.addFrontend(json=json_payload)
        self._apply(result)
        return result

    def update_frontend(self, uuid, json_payload: dict):
        result = self._settings_api.setFrontend(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_frontend(self, uuid):
        result = self._settings_api.delFrontend(uuid)
        self._apply(result)
        return result
