from opnsense_cli.api.base import ApiBase


class FirewallFilter(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "filter"
    """
    Firewall Filter (needs plugin: os-firewall)
    """
    @ApiBase._api_call
    def add_rule(self, *args, json=None):
        self.method = "post"
        self.command = "addRule"

    @ApiBase._api_call
    def del_rule(self, *args):
        self.method = "post"
        self.command = "delRule"

    @ApiBase._api_call
    def get_rule(self, *args):
        self.method = "get"
        self.command = "getRule"

    @ApiBase._api_call
    def set_rule(self, *args):
        self.method = "post"
        self.command = "setRule"

    @ApiBase._api_call
    def apply(self, *args):
        self.method = "post"
        self.command = "apply"

    @ApiBase._api_call
    def savepoint(self, *args):
        self.method = "post"
        self.command = "savepoint"

    @ApiBase._api_call
    def cancel_rollback(self, *args):
        self.method = "post"
        self.command = "cancelRollback"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"


class FirewallAlias(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias"
    """
    Firewall Alias Util
    """
    @ApiBase._api_call
    def export(self, *args):
        self.method = "get"
        self.command = "export"

    @ApiBase._api_call
    def get_uuid_for_name(self, *args):
        self.method = "get"
        self.command = "getAliasUUID"

    @ApiBase._api_call
    def add_item(self, *args, json=None):
        self.method = "post"
        self.command = "addItem"

    @ApiBase._api_call
    def del_item(self, *args):
        self.method = "post"
        self.command = "delItem"

    @ApiBase._api_call
    def set_item(self, *args, json=None):
        self.method = "post"
        self.command = "setItem"

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"


class FirewallAliasUtil(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias_util"
    """
    Firewall Alias Util
    """
    @ApiBase._api_call
    def list(self, *args):
        self.method = "get"
        self.command = "list"
