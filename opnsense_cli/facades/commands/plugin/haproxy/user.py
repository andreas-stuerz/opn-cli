from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyUserFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.users.user'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_users(self):
        return self._get_users_list()

    def show_user(self, uuid):
        users = self._get_users_list()
        user = next((item for item in users if item["uuid"] == uuid), {})
        return user

    def _get_users_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

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
