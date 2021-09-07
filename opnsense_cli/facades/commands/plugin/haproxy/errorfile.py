from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyErrorfileFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_errorfiles(self):
        return self._get_errorfiles_list()

    def show_errorfile(self, uuid):
        errorfiles = self._get_errorfiles_list()
        errorfile = next((item for item in errorfiles if item["uuid"] == uuid), {})
        return errorfile

    def _get_errorfiles_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.errorfiles.errorfile'
        uuid_resolver_map = {
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_errorfile(self, json_payload: dict):
        result = self._settings_api.addErrorfile(json=json_payload)
        self._apply(result)
        return result

    def update_errorfile(self, uuid, json_payload: dict):
        result = self._settings_api.setErrorfile(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_errorfile(self, uuid):
        result = self._settings_api.delErrorfile(uuid)
        self._apply(result)
        return result
