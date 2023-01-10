from opnsense_cli.api.base import ApiBase


class Service(ApiBase):
    MODULE = "unbound"
    CONTROLLER = "service"
    """
    Unbound ServiceController
    """

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"


class Settings(ApiBase):
    MODULE = "unbound"
    CONTROLLER = "settings"
    """
    Unbound SettingsController
    """

    @ApiBase._api_call
    def addDomainOverride(self, *args):
        self.method = "post"
        self.command = "addDomainOverride"

    @ApiBase._api_call
    def addHostAlias(self, *args):
        self.method = "post"
        self.command = "addHostAlias"

    @ApiBase._api_call
    def addHostOverride(self, *args):
        self.method = "post"
        self.command = "addHostOverride"

    @ApiBase._api_call
    def delDomainOverride(self, *args):
        self.method = "post"
        self.command = "delDomainOverride"

    @ApiBase._api_call
    def delHostAlias(self, *args):
        self.method = "post"
        self.command = "delHostAlias"

    @ApiBase._api_call
    def delHostOverride(self, *args):
        self.method = "post"
        self.command = "delHostOverride"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def setDomainOverride(self, *args):
        self.method = "post"
        self.command = "setDomainOverride"

    @ApiBase._api_call
    def setHostAlias(self, *args):
        self.method = "post"
        self.command = "setHostAlias"

    @ApiBase._api_call
    def setHostOverride(self, *args):
        self.method = "post"
        self.command = "setHostOverride"
