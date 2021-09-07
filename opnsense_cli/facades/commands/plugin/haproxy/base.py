from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade


class HaproxyFacade(CommandFacade):
    def _apply(self, result_admin_action=None):
        if result_admin_action and result_admin_action['result'] not in ['saved', 'deleted']:
            raise CommandException(result_admin_action)

        result_config_test = self._service_api.configtest()
        if result_config_test['result'].find('Configuration file is valid') == -1:
            raise CommandException(f"Configtest failed: {result_config_test}")

        result_apply = self._service_api.reconfigure()
        if result_apply['status'] != 'ok':
            raise CommandException(f"Apply failed: {result_apply}")
