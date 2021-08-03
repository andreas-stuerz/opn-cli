from opnsense_cli.api.base import ApiBase


class Firmware(ApiBase):
    MODULE = "Core"
    CONTROLLER = "Firmware"
    """
    FIRMWARE
    """

    @ApiBase._api_call
    def info(self, *args):
        self.method = "get"
        self.command = "info"

    @ApiBase._api_call
    def upgradestatus(self, *args):
        self.method = "get"
        self.command = "upgradestatus"

    """
    PACKAGES
    """

    @ApiBase._api_call
    def install(self, *args):
        self.method = "post"
        self.command = "install"

    @ApiBase._api_call
    def reinstall(self, *args):
        self.method = "post"
        self.command = "reinstall"

    @ApiBase._api_call
    def remove(self, *args):
        self.method = "post"
        self.command = "remove"

    @ApiBase._api_call
    def lock(self, *args):
        self.method = "post"
        self.command = "lock"

    @ApiBase._api_call
    def unlock(self, *args):
        self.method = "post"
        self.command = "unlock"

    @ApiBase._api_call
    def details(self, *args):
        self.method = "post"
        self.command = "details"
