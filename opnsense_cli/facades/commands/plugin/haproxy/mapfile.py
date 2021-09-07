from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyMapfileFacade(HaproxyFacade):
    def __init__(self, settings_api: Settings, service_api: Service):
        self._settings_api = settings_api
        self._service_api = service_api

    def list_mapfiles(self):
        return self._get_mapfiles_list()

    def show_mapfile(self, uuid):
        mapfiles = self._get_mapfiles_list()
        mapfile = next((item for item in mapfiles if item["uuid"] == uuid), {})
        return mapfile

    def _get_mapfiles_list(self):
        complete_model_data = self._settings_api.get()
        jsonpath_base = '$.haproxy.mapfiles.mapfile'
        uuid_resolver_map = {
        }

        return self._api_mutable_model_get(complete_model_data, jsonpath_base, uuid_resolver_map)

    def create_mapfile(self, json_payload: dict):
        result = self._settings_api.addMapfile(json=json_payload)
        self._apply(result)
        return result

    def update_mapfile(self, uuid, json_payload: dict):
        result = self._settings_api.setMapfile(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_mapfile(self, uuid):
        result = self._settings_api.delMapfile(uuid)
        self._apply(result)
        return result
