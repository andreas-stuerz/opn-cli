from opnsense_cli.api.base import ApiBase


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
