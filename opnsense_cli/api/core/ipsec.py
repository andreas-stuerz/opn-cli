from opnsense_cli.api.base import ApiBase


class Tunnel(ApiBase):
    MODULE = "ipsec"
    CONTROLLER = "tunnel"
    """
    Ipsec TunnelController
    """

    @ApiBase._api_call
    def searchPhase1(self, *args):
        self.method = "get"
        self.command = "searchPhase1"

    @ApiBase._api_call
    def searchPhase2(self, *args):
        self.method = "post"
        self.command = "searchPhase2"
