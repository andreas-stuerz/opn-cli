import time

from opnsense_cli.facades.commands.base import CommandFacade
from opnsense_cli.api.core.firmware import Firmware
from opnsense_cli.exceptions.command import CommandException


class FirmwareFacade(CommandFacade):
    def __init__(self, _firmware_api: Firmware, _query_upgrade_status_interval):
        self._firmware_api = _firmware_api
        self._query_upgrade_status_interval = _query_upgrade_status_interval

    def plugin_list(self):
        return self._list_plugins()

    def plugin_installed(self):
        all_plugins = self._list_plugins()
        installed_plugins = [plugin for plugin in all_plugins if plugin['installed'] == "1"]
        return installed_plugins

    def _list_plugins(self):
        return self._firmware_api.info()['plugin']

    def plugin_show(self, name):
        return self._firmware_api.details(name)

    def plugin_install(self, name):
        self._firmware_api.install(name)
        return self.get_last_upgrade_status()

    def plugin_uninstall(self, name):
        self._firmware_api.remove(name)
        return self.get_last_upgrade_status()

    def plugin_reinstall(self, name):
        self._firmware_api.reinstall(name)
        return self.get_last_upgrade_status()

    def plugin_lock(self, name):
        self._firmware_api.lock(name)
        return self.get_last_upgrade_status()

    def plugin_unlock(self, name):
        self._firmware_api.unlock(name)
        return self.get_last_upgrade_status()

    def get_last_upgrade_status(self):
        while True:
            log = self._firmware_api.upgradestatus()
            self._upgrade_status_error_handling(log)
            if log['status'] != 'running':
                return log
            time.sleep(self._query_upgrade_status_interval)

    def _upgrade_status_error_handling(self, log):
        if 'No packages available to install' in log['log']:
            log['status'] = 'error'
            raise CommandException(log)

        if 'No packages matched for pattern' in log['log']:
            log['status'] = 'not found'

        if 'is not installed' in log['log']:
            log['status'] = 'not found'

        if '***GOT REQUEST TO LOCK***\n***DONE***' in log['log']:
            log['status'] = 'not found'

        if '***GOT REQUEST TO UNLOCK***\n***DONE***' in log['log']:
            log['status'] = 'not found'
