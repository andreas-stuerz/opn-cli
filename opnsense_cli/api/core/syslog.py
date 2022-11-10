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
    def stats(self, *args):
        self.method = "get"
        self.command = "stats"


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
    def setDestination(self, *args):
        self.method = "post"
        self.command = "setDestination"
