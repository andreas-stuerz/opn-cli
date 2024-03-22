from opnsense_cli.api.core.configbackup import Backup
from opnsense_cli.commands.service_base import CommandService


class ConfigBackupService(CommandService):
    def __init__(self, backup_api: Backup):
        self._backup_api = backup_api

    def download_backup(self, path):
        config = self._backup_api.download("this")
        self._write_xml_string_to_file(path, config)
        return {"status": f"successfully saved to: {path}"}
