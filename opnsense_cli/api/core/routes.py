from opnsense_cli.api.base import ApiBase


class Gateway(ApiBase):
    MODULE = "routes"
    CONTROLLER = "gateway"
    """
    Routes GatewayController
    """

    @ApiBase._api_call
    def status(self, *args):
        self.method = "get"
        self.command = "status"


class Routes(ApiBase):
    MODULE = "routes"
    CONTROLLER = "routes"
    """
    Routes RoutesController
    """

    @ApiBase._api_call
    def addroute(self, *args):
        self.method = "post"
        self.command = "addroute"

    @ApiBase._api_call
    def delroute(self, *args):
        self.method = "post"
        self.command = "delroute"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def getroute(self, *args):
        self.method = "get"
        self.command = "getroute"

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"

    @ApiBase._api_call
    def searchroute(self, *args):
        self.method = "*"
        self.command = "searchroute"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "post"
        self.command = "set"

    @ApiBase._api_call
    def setroute(self, *args):
        self.method = "post"
        self.command = "setroute"

    @ApiBase._api_call
    def toggleroute(self, *args):
        self.method = "post"
        self.command = "toggleroute"

