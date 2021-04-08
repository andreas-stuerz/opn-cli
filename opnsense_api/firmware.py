from opnsense_api.base import ApiBase


class Firmware(ApiBase):
    MODULE = "Core"
    CONTROLLER = "Firmware"

    @ApiBase._api_call
    def info(self, *args):
        self.method = "get"
        self.command = "info"

    @ApiBase._api_call
    def changelog(self, *args):
        self.method = "post"
        self.command = "changelog"

