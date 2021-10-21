from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyGroupFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.groups.group'
    uuid_resolver_map = {
        'members': {'template': '$.haproxy.users.user[{uuids}].name', 'insert_as_key': 'Users'},
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_groups(self):
        return self._get_groups_list()

    def show_group(self, uuid):
        groups = self._get_groups_list()
        group = next((item for item in groups if item["uuid"] == uuid), {})
        return group

    def _get_groups_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

    def create_group(self, json_payload: dict):
        result = self._settings_api.addGroup(json=json_payload)
        self._apply(result)
        return result

    def update_group(self, uuid, json_payload: dict):
        result = self._settings_api.setGroup(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_group(self, uuid):
        result = self._settings_api.delGroup(uuid)
        self._apply(result)
        return result
