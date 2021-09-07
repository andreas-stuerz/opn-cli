from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyGroupFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_groups(self):
        return self._get_groups_list()

    def show_group(self, uuid):
        groups = self._get_groups_list()
        group = next((item for item in groups if item["uuid"] == uuid), {})
        return group

    def _get_groups_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.groups.group'
        uuid_resolver_map = {
            'members': {'template': '$.haproxy.users.user[{uuids}].name', 'insert_as_key': 'Users'},
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

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
