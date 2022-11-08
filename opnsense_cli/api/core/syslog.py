from opnsense_cli.api.base import ApiBase


class Service(ApiBase):
    MODULE = "syslog"
    CONTROLLER = "service"
    """
    Syslog ServiceController
    """

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
    def stats(self, *args):
        self.method = "get"
        self.command = "stats"

    @ApiBase._api_call
    def status(self, *args):
        self.method = "get"
        self.command = "status"

    @ApiBase._api_call
    def stop(self, *args):
        self.method = "post"
        self.command = "stop"


class Settings(ApiBase):
    MODULE = "syslog"
    CONTROLLER = "settings"
    """
    Syslog SettingsController
    """

    @ApiBase._api_call
    def addDestination(self, *args):
        self.method = "post"
        self.command = "addDestination"

    @ApiBase._api_call
    def delDestination(self, *args):
        self.method = "post"
        self.command = "delDestination"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def getDestination(self, *args):
        self.method = "get"
        self.command = "getDestination"

    @ApiBase._api_call
    def searchDestinations(self, *args):
        self.method = "*"
        self.command = "searchDestinations"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "post"
        self.command = "set"

    @ApiBase._api_call
    def setDestination(self, *args):
        self.method = "post"
        self.command = "setDestination"

    @ApiBase._api_call
    def toggleDestination(self, *args):
        self.method = "post"
        self.command = "toggleDestination"

