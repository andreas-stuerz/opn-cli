from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.unbound import Settings, Service


class UnboundDomainFacade(CommandFacade):
    jsonpath_base = '$.unbound.domains.domain'
    uuid_resolver_map = {
    }

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_domains(self):
        return self._get_domains_list()

    def show_domain(self, uuid):
        domains = self._get_domains_list()
        domain = next((item for item in domains if item["uuid"] == uuid), {})
        return domain

    def _get_domains_list(self):
        return self._api_mutable_model_get(
            self._complete_model_data,
            self.jsonpath_base,
            self.uuid_resolver_map,
            sort_by='uuid'
        )

    def create_domain(self, json_payload: dict):
        result = self._settings_api.addDomainOverride(json=json_payload)
        self._apply(result)
        return result

    def update_domain(self, uuid, json_payload: dict):
        result = self._settings_api.setDomainOverride(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_domain(self, uuid):
        result = self._settings_api.delDomainOverride(uuid)
        self._apply(result)
        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._service_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
