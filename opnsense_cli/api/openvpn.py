from opnsense_cli.api.base import ApiBase


class Openvpn(ApiBase):
    MODULE = "openvpn"
    CONTROLLER = "export"
    """
    OPENVPN EXPORT
    """

    @ApiBase._api_call
    def accounts(self, *args, **kwargs):
        self.method = "get"
        self.command = "accounts"

    @ApiBase._api_call
    def download(self, *args, json=None, **kwargs):
        self.method = "post"
        self.command = "download"

    @ApiBase._api_call
    def providers(self, *args, **kwargs):
        self.method = "get"
        self.command = "providers"

    @ApiBase._api_call
    def storePresets(self, *args, **kwargs):
        self.method = "post"
        self.command = "storePresets"

    @ApiBase._api_call
    def templates(self, *args, **kwargs):
        self.method = "get"
        self.command = "templates"

    @ApiBase._api_call
    def validatePresets(self, *args, **kwargs):
        self.method = "post"
        self.command = "validatePresets"
