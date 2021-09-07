from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyUserFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_users(self):
        return self._get_users_list()

    def show_user(self, uuid):
        users = self._get_users_list()
        user = next((item for item in users if item["uuid"] == uuid), {})
        return user

    def _get_users_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.users.user'
        uuid_resolver_map = {
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_user(self, json_payload: dict):
        result = self._settings_api.addUser(json=json_payload)
        self._apply(result)
        return result

    def update_user(self, uuid, json_payload: dict):
        result = self._settings_api.setUser(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_user(self, uuid):
        result = self._settings_api.delUser(uuid)
        self._apply(result)
        return result
