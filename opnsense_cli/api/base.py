from opnsense_cli.api.client import ApiClient


class ApiBase():
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self.module = self.MODULE
        self.controller = self.CONTROLLER
        self._method = None
        self._command = None

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    def _api_call(api_function):
        def api_response(self, *args, json=None):
            api_function(self)
            return self._api_client.execute(
                *args,
                module=self.module, controller=self.controller, method=self.method, command=self.command,
                json=json
            )

        return api_response
