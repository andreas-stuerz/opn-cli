from opnsense_cli.api.firewall import FirewallAlias, FirewallAliasUtil
from opnsense_cli.facades.base import CommandFacade


class FirewallAliasFacade(CommandFacade):
    def __init__(self, firewall_alias_api: FirewallAlias, firewall_alias_util_api: FirewallAliasUtil):
        self._firewall_alias_api = firewall_alias_api
        self._firewall_alias_util_api = firewall_alias_util_api

    def show_pf_table(self, alias_name):
        return self._get_content_for_external(alias_name)

    def _get_content_for_external(self, alias_name):
        return self._firewall_alias_util_api.list(alias_name)['rows']

    def list_aliases(self):
        return self._get_alias_list()

    def show_alias(self, alias_name):
        return self._get_details_for_alias(alias_name)

    def update_alias(self, alias_name, json_payload: dict):
        uuid = self._get_uuid_for_name(alias_name)
        return self._firewall_alias_api.set_item(uuid, json=json_payload)

    def delete_alias(self, alias_name):
        uuid = self._get_uuid_for_name(alias_name)
        return self._firewall_alias_api.del_item(uuid)

    def _get_details_for_alias(self, alias_name):
        uuid = self._get_uuid_for_name(alias_name)
        aliases = self._get_alias_list()
        alias = next((item for item in aliases if item["uuid"] == uuid), {})
        return alias

    def _get_uuid_for_name(self, name):
        try:
            return self._firewall_alias_api.get_uuid_for_name(name).get('uuid', None)
        except AttributeError:
            return "null"

    def _get_alias_list(self):
        aliases = []
        aliases_raw = self._firewall_alias_api.export()['aliases']['alias']

        for alias_uuid, alias_data in aliases_raw.items():
            alias_data.update({'uuid': alias_uuid})
            alias_data['content'] = alias_data['content'].replace("\n", ",")
            aliases.append(alias_data)

        aliases = self._sort_dict_by_string(aliases, 'name')

        return aliases

    def create_alias(self, json_payload: dict):
        return self._firewall_alias_api.add_item(json=json_payload)
