from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.unbound import Settings, Service


class UnboundAliasFacade(CommandFacade):
    jsonpath_base = '$.unbound.aliases.alias'
    uuid_resolver_map = dict(
        host={
            'template': '$.unbound.hosts.host[{uuids}].hostname,domain,rr,mxprio,mx,server',
            'insert_as_key': 'Host',
            'join_by': '|'
        },
    )

    def __init__(self, settings_api: Settings, service_api: Service):
        super().__init__()
        self._complete_model_data_cache = None
        self._settings_api = settings_api
        self._service_api = service_api

    def list_aliass(self):
        return self._get_aliass_list()

    def show_alias(self, uuid):
        aliass = self._get_aliass_list()
        alias = next((item for item in aliass if item["uuid"] == uuid), {})
        return alias

    def _get_aliass_list(self):
        return self._api_mutable_model_get(
            self._complete_model_data,
            self.jsonpath_base,
            self.uuid_resolver_map,
            sort_by='uuid'
        )

    def create_alias(self, json_payload: dict):
        result = self._settings_api.addHostAlias(json=json_payload)
        self._apply(result)
        return result

    def update_alias(self, uuid, json_payload: dict):
        result = self._settings_api.setHostAlias(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_alias(self, uuid):
        result = self._settings_api.delHostAlias(uuid)
        self._apply(result)
        return result

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._service_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
