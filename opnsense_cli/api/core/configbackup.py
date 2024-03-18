from opnsense_cli.api.base import ApiBase


class Backup(ApiBase):
    MODULE = "core"
    CONTROLLER = "backup"
    """
    api-backup BackupController
    """

    @ApiBase._api_call
    def download(self, *args):
        self.method = "get"
        self.command = "download"
