from opnsense_cli.api.base import ApiBase


class Diagnostics(ApiBase):
    MODULE = "unbound"
    CONTROLLER = "diagnostics"
    """
    Unbound DiagnosticsController
    """

    @ApiBase._api_call
    def dumpcache(self, *args):
        self.method = "get"
        self.command = "dumpcache"

    @ApiBase._api_call
    def dumpinfra(self, *args):
        self.method = "get"
        self.command = "dumpinfra"

    @ApiBase._api_call
    def listinsecure(self, *args):
        self.method = "get"
        self.command = "listinsecure"

    @ApiBase._api_call
    def listlocaldata(self, *args):
        self.method = "get"
        self.command = "listlocaldata"

    @ApiBase._api_call
    def listlocalzones(self, *args):
        self.method = "get"
        self.command = "listlocalzones"

    @ApiBase._api_call
    def stats(self, *args):
        self.method = "get"
        self.command = "stats"


class Service(ApiBase):
    MODULE = "unbound"
    CONTROLLER = "service"
    """
    Unbound ServiceController
    """

    @ApiBase._api_call
    def dnsbl(self, *args):
        self.method = "get"
        self.command = "dnsbl"

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"

    @ApiBase._api_call
    def restart(self, *args):
        self.method = "post"
        self.command = "restart"

    @ApiBase._api_call
    def start(self, *args):
        self.method = "post"
        self.command = "start"

    @ApiBase._api_call
    def status(self, *args):
        self.method = "get"
        self.command = "status"

    @ApiBase._api_call
    def stop(self, *args):
        self.method = "post"
        self.command = "stop"


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
    def addForward(self, *args):
        self.method = "post"
        self.command = "addForward"

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
    def delForward(self, *args):
        self.method = "post"
        self.command = "delForward"

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
    def getDomainOverride(self, *args):
        self.method = "get"
        self.command = "getDomainOverride"

    @ApiBase._api_call
    def getForward(self, *args):
        self.method = "get"
        self.command = "getForward"

    @ApiBase._api_call
    def getHostAlias(self, *args):
        self.method = "get"
        self.command = "getHostAlias"

    @ApiBase._api_call
    def getHostOverride(self, *args):
        self.method = "get"
        self.command = "getHostOverride"

    @ApiBase._api_call
    def getNameservers(self, *args):
        self.method = "get"
        self.command = "getNameservers"

    @ApiBase._api_call
    def searchDomainOverride(self, *args):
        self.method = "*"
        self.command = "searchDomainOverride"

    @ApiBase._api_call
    def searchForward(self, *args):
        self.method = "*"
        self.command = "searchForward"

    @ApiBase._api_call
    def searchHostAlias(self, *args):
        self.method = "*"
        self.command = "searchHostAlias"

    @ApiBase._api_call
    def searchHostOverride(self, *args):
        self.method = "*"
        self.command = "searchHostOverride"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "post"
        self.command = "set"

    @ApiBase._api_call
    def setDomainOverride(self, *args):
        self.method = "post"
        self.command = "setDomainOverride"

    @ApiBase._api_call
    def setForward(self, *args):
        self.method = "post"
        self.command = "setForward"

    @ApiBase._api_call
    def setHostAlias(self, *args):
        self.method = "post"
        self.command = "setHostAlias"

    @ApiBase._api_call
    def setHostOverride(self, *args):
        self.method = "post"
        self.command = "setHostOverride"

    @ApiBase._api_call
    def toggleDomainOverride(self, *args):
        self.method = "post"
        self.command = "toggleDomainOverride"

    @ApiBase._api_call
    def toggleForward(self, *args):
        self.method = "post"
        self.command = "toggleForward"

    @ApiBase._api_call
    def toggleHostAlias(self, *args):
        self.method = "post"
        self.command = "toggleHostAlias"

    @ApiBase._api_call
    def toggleHostOverride(self, *args):
        self.method = "post"
        self.command = "toggleHostOverride"

