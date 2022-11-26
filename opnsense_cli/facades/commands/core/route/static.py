from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.routes import Routes, Gateway


class RoutesStaticFacade(CommandFacade):
    jsonpath_base = '$.route.route'
    uuid_resolver_map = {
    }

    def __init__(self, routes_api: Routes, gateway_api: Gateway):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = routes_api
        self._gateway_api = gateway_api

    def list_statics(self):
        return self._get_statics_list()

    def show_static(self, uuid):
        statics = self._get_statics_list()
        static = next((item for item in statics if item["uuid"] == uuid), {})
        return static

    def _get_statics_list(self):
        return self._api_mutable_model_get(
            self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map, sort_by='uuid'
        )

    def create_static(self, json_payload: dict):
        result = self._settings_api.addroute(json=json_payload)
        self._apply(result)
        return result

    def update_static(self, uuid, json_payload: dict):
        result = self._settings_api.setroute(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_static(self, uuid):
        result = self._settings_api.delroute(uuid)
        self._apply(result)
        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._settings_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
