from opnsense_cli.api.plugin.firewall import FirewallAlias, FirewallAliasUtil
from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade


class FirewallAliasFacade(CommandFacade):
    def __init__(self, firewall_alias_api: FirewallAlias, firewall_alias_util_api: FirewallAliasUtil):
        self._firewall_alias_api = firewall_alias_api
        self._firewall_alias_util_api = firewall_alias_util_api

    def show_pf_table(self, alias_name):
        return self._firewall_alias_util_api.list(alias_name)['rows']

    def create_alias(self, json_payload: dict):
        result = self._firewall_alias_api.add_item(json=json_payload)
        self._apply(result)
        return result

    def update_alias(self, alias_name, json_payload: dict):
        uuid = self._get_uuid_for_name(alias_name)
        result = self._firewall_alias_api.set_item(uuid, json=json_payload)
        self._apply(result)
        return result

    def delete_alias(self, alias_name):
        uuid = self._get_uuid_for_name(alias_name)
        result = self._firewall_alias_api.del_item(uuid)
        self._apply(result)
        return result

    def show_alias(self, alias_name):
        uuid = self._get_uuid_for_name(alias_name)
        aliases = self._get_alias_list()
        alias = next((item for item in aliases if item["uuid"] == uuid), {})
        return alias

    def _get_uuid_for_name(self, name):
        try:
            return self._firewall_alias_api.get_uuid_for_name(name).get('uuid', None)
        except AttributeError:
            return "null"

    def _apply(self, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._firewall_alias_api.reconfigure()

        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")

    def list_aliases(self):
        return self._get_alias_list()

    def _get_alias_list(self):
        aliases = []
        aliases_raw = self._firewall_alias_api.export()['aliases']['alias']

        for alias_uuid, alias_data in aliases_raw.items():
            alias_data.update({'uuid': alias_uuid})
            alias_data['content'] = alias_data['content'].replace("\n", ",")
            aliases.append(alias_data)

        aliases = self._sort_dict_by_string(aliases, 'name')

        return aliases
