from opnsense_cli.api.plugin.firewall import FirewallFilter
from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.exceptions.command import CommandException


class FirewallRuleFacade(CommandFacade):
    def __init__(self, firewall_rule_api: FirewallFilter):
        self._firewall_rule_api = firewall_rule_api

    def list_rules(self):
        return self._get_rules_list()

    def _get_rules_list(self):
        raw_rules = dict(self._firewall_rule_api.get()['filter']['rules']['rule'])
        rules = []
        for uuid, rule_raw in raw_rules.items():
            rule = self._api_mutable_model_get_items_to_json(rule_raw)
            rule.update({'uuid': uuid})
            rules.append(rule)

        rules = self._sort_dict_by_number(rules, 'sequence')
        return rules

    def show_rule(self, uuid):
        return self._get_details_for_rule(uuid)

    def _get_details_for_rule(self, uuid):
        if not uuid:
            return {}

        rule_raw = dict(self._firewall_rule_api.get_rule(uuid)).get('rule', {})
        return self._api_mutable_model_get_items_to_json(rule_raw)

    def create_rule(self, json_payload: dict):
        timestamp = self._start_transaction()
        result = self._firewall_rule_api.add_rule(json=json_payload)
        self._commit_transaction(timestamp, result)
        return result

    def update_rule(self, uuid, json_payload: dict):
        timestamp = self._start_transaction()
        result = self._firewall_rule_api.set_rule(uuid, json=json_payload)
        self._commit_transaction(timestamp, result)
        return result

    def delete_rule(self, uuid):
        timestamp = self._start_transaction()
        result = self._firewall_rule_api.del_rule(uuid)
        self._commit_transaction(timestamp, result)
        return result

    def _start_transaction(self):
        result = self._firewall_rule_api.savepoint()
        if result['status'] != 'ok':
            raise CommandException(f"Savepoint creation failed: {result}")
        return result['revision']

    def _commit_transaction(self, timestamp, result_admin_action):
        if result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_apply = self._firewall_rule_api.apply(timestamp)
        if result_apply['status'].replace("\n", "") != 'OK':
            raise CommandException(f"firewall rule apply failed: {result_apply}")

        result_cancel = self._firewall_rule_api.cancel_rollback(timestamp)
        if result_cancel['status'].replace("\n", "") != '':
            raise CommandException(
                f"firewall rule cancel rollback failed. Rollback configuration after 60 seconds: {result_cancel}"
            )
