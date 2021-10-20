from opnsense_cli.facades.commands.plugin.haproxy.base import HaproxyFacade
from opnsense_cli.api.plugin.haproxy import Settings, Service


class HaproxyMailerFacade(HaproxyFacade):
    jsonpath_base = '$.haproxy.mailers.mailer'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_mailers(self):
        return self._get_mailers_list()

    def show_mailer(self, uuid):
        mailers = self._get_mailers_list()
        mailer = next((item for item in mailers if item["uuid"] == uuid), {})
        return mailer

    def _get_mailers_list(self):
        return self._api_mutable_model_get(self._complete_model_data, self.jsonpath_base, self.uuid_resolver_map)

    def create_mailer(self, json_payload: dict):
        result = self._settings_api.addmailer(json=json_payload)
        self._apply(result)
        return result

    def update_mailer(self, uuid, json_payload: dict):
        result = self._settings_api.setmailer(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_mailer(self, uuid):
        result = self._settings_api.delmailer(uuid)
        self._apply(result)
        return result
