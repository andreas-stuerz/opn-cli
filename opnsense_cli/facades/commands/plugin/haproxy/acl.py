from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyAclFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_acls(self):
        return self._get_acls_list()

    def show_acl(self, uuid):
        acls = self._get_acls_list()
        acl = next((item for item in acls if item["uuid"] == uuid), {})
        return acl

    def _get_acls_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.acls.acl'
        uuid_resolver_map = {
            'nbsrv_backend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'BackendNrSrv'},
            'queryBackend': {'template': '$.haproxy.backends.backend[{uuids}].name', 'insert_as_key': 'BackendQuery'},
            'allowedUsers': {'template': '$.haproxy.users.user[{uuids}].name', 'insert_as_key': 'Users'},
            'allowedGroups': {'template': '$.haproxy.groups.group[{uuids}].name', 'insert_as_key': 'Groups'},
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_acl(self, json_payload: dict):
        result = self._settings_api.addAcl(json=json_payload)
        self._apply(result)
        return result

    def update_acl(self, uuid, json_payload: dict):
        result = self._settings_api.setAcl(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_acl(self, uuid):
        result = self._settings_api.delAcl(uuid)
        self._apply(result)
        return result
