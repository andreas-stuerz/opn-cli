from opnsense_api.client import ApiClient

MODULE = "Core"
CONTROLLER = "Firmware"

class Firmware():
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client

    def info(self, *args):
        method = "get"
        command = "info"
        return self._api_client.execute(*args, module=MODULE, controller=CONTROLLER, method=method, command=command)

    def changelog(self, *args):
        method = "post"
        command = "changelog"
        return self._api_client.execute(*args, module=MODULE, controller=CONTROLLER, method=method, command=command)



