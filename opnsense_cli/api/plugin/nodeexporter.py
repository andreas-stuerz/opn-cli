from opnsense_cli.api.base import ApiBase


class General(ApiBase):
    MODULE = "nodeexporter"
    CONTROLLER = "general"
    """
    Nodeexporter GeneralController
    """

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "post"
        self.command = "set"


class Service(ApiBase):
    MODULE = "nodeexporter"
    CONTROLLER = "service"
    """
    Nodeexporter ServiceController
    """

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"
