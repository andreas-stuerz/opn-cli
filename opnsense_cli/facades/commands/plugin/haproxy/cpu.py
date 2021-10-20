from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyCpuFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.cpus.cpu'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_cpus(self):
        return self._get_cpus_list()

    def show_cpu(self, uuid):
        cpus = self._get_cpus_list()
        cpu = next((item for item in cpus if item["uuid"] == uuid), {})
        return cpu

    def _get_cpus_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

    def create_cpu(self, json_payload: dict):
        result = self._settings_api.addCpu(json=json_payload)
        self._apply(result)
        return result

    def update_cpu(self, uuid, json_payload: dict):
        result = self._settings_api.setCpu(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_cpu(self, uuid):
        result = self._settings_api.delCpu(uuid)
        self._apply(result)
        return result
