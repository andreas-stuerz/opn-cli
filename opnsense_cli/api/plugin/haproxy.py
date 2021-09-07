from opnsense_cli.api.base import ApiBase


class Export(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "export"
    """
    Haproxy ExportController
    """

    @ApiBase._api_call
    def config(self, *args):
        self.method = "get"
        self.command = "config"

    @ApiBase._api_call
    def diff(self, *args):
        self.method = "get"
        self.command = "diff"

    @ApiBase._api_call
    def download(self, *args):
        self.method = "get"
        self.command = "download"


class Service(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "service"
    """
    Haproxy ServiceController
    """

    @ApiBase._api_call
    def configtest(self, *args):
        self.method = "get"
        self.command = "configtest"

    @ApiBase._api_call
    def reconfigure(self, *args):
        self.method = "post"
        self.command = "reconfigure"


class Settings(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "settings"
    """
    Haproxy SettingsController
    """

    @ApiBase._api_call
    def addAcl(self, *args):
        self.method = "post"
        self.command = "addAcl"

    @ApiBase._api_call
    def addAction(self, *args):
        self.method = "post"
        self.command = "addAction"

    @ApiBase._api_call
    def addBackend(self, *args, json=None):
        self.method = "post"
        self.command = "addBackend"

    @ApiBase._api_call
    def addCpu(self, *args):
        self.method = "post"
        self.command = "addCpu"

    @ApiBase._api_call
    def addErrorfile(self, *args):
        self.method = "post"
        self.command = "addErrorfile"

    @ApiBase._api_call
    def addFrontend(self, *args, json=None):
        self.method = "post"
        self.command = "addFrontend"

    @ApiBase._api_call
    def addGroup(self, *args):
        self.method = "post"
        self.command = "addGroup"

    @ApiBase._api_call
    def addHealthcheck(self, *args):
        self.method = "post"
        self.command = "addHealthcheck"

    @ApiBase._api_call
    def addLua(self, *args):
        self.method = "post"
        self.command = "addLua"

    @ApiBase._api_call
    def addMapfile(self, *args):
        self.method = "post"
        self.command = "addMapfile"

    @ApiBase._api_call
    def addServer(self, *args, json=None):
        self.method = "post"
        self.command = "addServer"

    @ApiBase._api_call
    def addUser(self, *args):
        self.method = "post"
        self.command = "addUser"

    @ApiBase._api_call
    def addmailer(self, *args):
        self.method = "post"
        self.command = "addmailer"

    @ApiBase._api_call
    def addresolver(self, *args):
        self.method = "post"
        self.command = "addresolver"

    @ApiBase._api_call
    def delAcl(self, *args):
        self.method = "post"
        self.command = "delAcl"

    @ApiBase._api_call
    def delAction(self, *args):
        self.method = "post"
        self.command = "delAction"

    @ApiBase._api_call
    def delBackend(self, *args, json=None):
        self.method = "post"
        self.command = "delBackend"

    @ApiBase._api_call
    def delCpu(self, *args):
        self.method = "post"
        self.command = "delCpu"

    @ApiBase._api_call
    def delErrorfile(self, *args):
        self.method = "post"
        self.command = "delErrorfile"

    @ApiBase._api_call
    def delFrontend(self, *args, json=None):
        self.method = "post"
        self.command = "delFrontend"

    @ApiBase._api_call
    def delGroup(self, *args):
        self.method = "post"
        self.command = "delGroup"

    @ApiBase._api_call
    def delHealthcheck(self, *args):
        self.method = "post"
        self.command = "delHealthcheck"

    @ApiBase._api_call
    def delLua(self, *args):
        self.method = "post"
        self.command = "delLua"

    @ApiBase._api_call
    def delMapfile(self, *args):
        self.method = "post"
        self.command = "delMapfile"

    @ApiBase._api_call
    def delServer(self, *args):
        self.method = "post"
        self.command = "delServer"

    @ApiBase._api_call
    def delUser(self, *args):
        self.method = "post"
        self.command = "delUser"

    @ApiBase._api_call
    def delmailer(self, *args):
        self.method = "post"
        self.command = "delmailer"

    @ApiBase._api_call
    def delresolver(self, *args):
        self.method = "post"
        self.command = "delresolver"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def setAcl(self, *args):
        self.method = "post"
        self.command = "setAcl"

    @ApiBase._api_call
    def setAction(self, *args):
        self.method = "post"
        self.command = "setAction"

    @ApiBase._api_call
    def setBackend(self, *args, json=None):
        self.method = "post"
        self.command = "setBackend"

    @ApiBase._api_call
    def setCpu(self, *args):
        self.method = "post"
        self.command = "setCpu"

    @ApiBase._api_call
    def setErrorfile(self, *args):
        self.method = "post"
        self.command = "setErrorfile"

    @ApiBase._api_call
    def setFrontend(self, *args, json=None):
        self.method = "post"
        self.command = "setFrontend"

    @ApiBase._api_call
    def setGroup(self, *args):
        self.method = "post"
        self.command = "setGroup"

    @ApiBase._api_call
    def setHealthcheck(self, *args):
        self.method = "post"
        self.command = "setHealthcheck"

    @ApiBase._api_call
    def setLua(self, *args):
        self.method = "post"
        self.command = "setLua"

    @ApiBase._api_call
    def setMapfile(self, *args):
        self.method = "post"
        self.command = "setMapfile"

    @ApiBase._api_call
    def setServer(self, *args, json=None):
        self.method = "post"
        self.command = "setServer"

    @ApiBase._api_call
    def setUser(self, *args):
        self.method = "post"
        self.command = "setUser"

    @ApiBase._api_call
    def setmailer(self, *args):
        self.method = "post"
        self.command = "setmailer"

    @ApiBase._api_call
    def setresolver(self, *args):
        self.method = "post"
        self.command = "setresolver"
