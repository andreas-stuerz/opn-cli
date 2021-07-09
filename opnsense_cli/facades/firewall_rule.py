from opnsense_cli.api.firewall import FirewallFilter
from opnsense_cli.facades.base import CommandFacade


class FirewallRuleFacade(CommandFacade):
    def __init__(self, firewall_rule_api: FirewallFilter):
        self._firewall_rule_api = firewall_rule_api

    def list_rules(self):
        return self._get_rules_list()

    def _get_rules_list(self):
        raw_rules = self._firewall_rule_api.get()['filter']['rules']['rule']
        rules = []
        for uuid, rule_raw in raw_rules.items():
            rule = self._api_mutable_model_get_items_to_json(rule_raw)
            rule.update({'uuid': uuid})
            rules.append(rule)

        rules = self._sort_dict(rules, 'sequence')
        return rules

    def show_rule(self, uuid):
        return self._get_details_for_rule(uuid)

    def _get_uuid_for_sequence(self, sequence):
        rules = self._firewall_rule_api.search_rule()['rows']
        uuid = next((rule['uuid'] for rule in rules if rule["sequence"] == sequence), None)
        return uuid

    def _get_details_for_rule(self, uuid):
        if not uuid:
            return {}
        rule_raw = self._firewall_rule_api.get_rule(uuid)['rule']
        return self._api_mutable_model_get_items_to_json(rule_raw)











