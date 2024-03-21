from opnsense_cli.commands.service_base import CommandService
from opnsense_cli.api.core.routes import Gateway


class RoutesGatewayService(CommandService):
    def __init__(self, gateway_api: Gateway):
        super().__init__()
        self._gateway_api = gateway_api

    def show_status(self):
        return self._gateway_api.status()["items"]
