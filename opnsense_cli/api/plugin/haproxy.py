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

class Maintenance(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "maintenance"
    """
    Haproxy MaintenanceController
    """

    @ApiBase._api_call
    def certActions(self, *args):
        self.method = "get"
        self.command = "certActions"

    @ApiBase._api_call
    def certDiff(self, *args):
        self.method = "get"
        self.command = "certDiff"

    @ApiBase._api_call
    def certSync(self, *args):
        self.method = "get"
        self.command = "certSync"

    @ApiBase._api_call
    def certSyncBulk(self, *args):
        self.method = "get"
        self.command = "certSyncBulk"

    @ApiBase._api_call
    def fetchCronIntegration(self, *args):
        self.method = "post"
        self.command = "fetchCronIntegration"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"

    @ApiBase._api_call
    def searchCertificateDiff(self, *args):
        self.method = "get"
        self.command = "searchCertificateDiff"

    @ApiBase._api_call
    def searchServer(self, *args):
        self.method = "get"
        self.command = "searchServer"

    @ApiBase._api_call
    def serverState(self, *args):
        self.method = "get"
        self.command = "serverState"

    @ApiBase._api_call
    def serverStateBulk(self, *args):
        self.method = "get"
        self.command = "serverStateBulk"

    @ApiBase._api_call
    def serverWeight(self, *args):
        self.method = "get"
        self.command = "serverWeight"

    @ApiBase._api_call
    def serverWeightBulk(self, *args):
        self.method = "get"
        self.command = "serverWeightBulk"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "get"
        self.command = "set"

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
        self.method = "get"
        self.command = "reconfigure"

    @ApiBase._api_call
    def restart(self, *args):
        self.method = "get"
        self.command = "restart"

    @ApiBase._api_call
    def start(self, *args):
        self.method = "get"
        self.command = "start"

    @ApiBase._api_call
    def status(self, *args):
        self.method = "get"
        self.command = "status"

    @ApiBase._api_call
    def stop(self, *args):
        self.method = "get"
        self.command = "stop"

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
    def addBackend(self, *args):
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
    def addFrontend(self, *args):
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
    def addServer(self, *args):
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
    def delBackend(self, *args):
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
    def delFrontend(self, *args):
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
    def getAcl(self, *args):
        self.method = "get"
        self.command = "getAcl"

    @ApiBase._api_call
    def getAction(self, *args):
        self.method = "get"
        self.command = "getAction"

    @ApiBase._api_call
    def getBackend(self, *args):
        self.method = "get"
        self.command = "getBackend"

    @ApiBase._api_call
    def getCpu(self, *args):
        self.method = "get"
        self.command = "getCpu"

    @ApiBase._api_call
    def getErrorfile(self, *args):
        self.method = "get"
        self.command = "getErrorfile"

    @ApiBase._api_call
    def getFrontend(self, *args):
        self.method = "get"
        self.command = "getFrontend"

    @ApiBase._api_call
    def getGroup(self, *args):
        self.method = "get"
        self.command = "getGroup"

    @ApiBase._api_call
    def getHealthcheck(self, *args):
        self.method = "get"
        self.command = "getHealthcheck"

    @ApiBase._api_call
    def getLua(self, *args):
        self.method = "get"
        self.command = "getLua"

    @ApiBase._api_call
    def getMapfile(self, *args):
        self.method = "get"
        self.command = "getMapfile"

    @ApiBase._api_call
    def getServer(self, *args):
        self.method = "get"
        self.command = "getServer"

    @ApiBase._api_call
    def getUser(self, *args):
        self.method = "get"
        self.command = "getUser"

    @ApiBase._api_call
    def getmailer(self, *args):
        self.method = "get"
        self.command = "getmailer"

    @ApiBase._api_call
    def getresolver(self, *args):
        self.method = "get"
        self.command = "getresolver"

    @ApiBase._api_call
    def searchAcls(self, *args):
        self.method = "*"
        self.command = "searchAcls"

    @ApiBase._api_call
    def searchActions(self, *args):
        self.method = "*"
        self.command = "searchActions"

    @ApiBase._api_call
    def searchBackends(self, *args):
        self.method = "*"
        self.command = "searchBackends"

    @ApiBase._api_call
    def searchCpus(self, *args):
        self.method = "*"
        self.command = "searchCpus"

    @ApiBase._api_call
    def searchErrorfiles(self, *args):
        self.method = "*"
        self.command = "searchErrorfiles"

    @ApiBase._api_call
    def searchFrontends(self, *args):
        self.method = "*"
        self.command = "searchFrontends"

    @ApiBase._api_call
    def searchGroups(self, *args):
        self.method = "*"
        self.command = "searchGroups"

    @ApiBase._api_call
    def searchHealthchecks(self, *args):
        self.method = "*"
        self.command = "searchHealthchecks"

    @ApiBase._api_call
    def searchLuas(self, *args):
        self.method = "*"
        self.command = "searchLuas"

    @ApiBase._api_call
    def searchMapfiles(self, *args):
        self.method = "*"
        self.command = "searchMapfiles"

    @ApiBase._api_call
    def searchServers(self, *args):
        self.method = "*"
        self.command = "searchServers"

    @ApiBase._api_call
    def searchUsers(self, *args):
        self.method = "*"
        self.command = "searchUsers"

    @ApiBase._api_call
    def searchmailers(self, *args):
        self.method = "*"
        self.command = "searchmailers"

    @ApiBase._api_call
    def searchresolvers(self, *args):
        self.method = "*"
        self.command = "searchresolvers"

    @ApiBase._api_call
    def set(self, *args):
        self.method = "get"
        self.command = "set"

    @ApiBase._api_call
    def setAcl(self, *args):
        self.method = "post"
        self.command = "setAcl"

    @ApiBase._api_call
    def setAction(self, *args):
        self.method = "post"
        self.command = "setAction"

    @ApiBase._api_call
    def setBackend(self, *args):
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
    def setFrontend(self, *args):
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
    def setServer(self, *args):
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

    @ApiBase._api_call
    def toggleBackend(self, *args):
        self.method = "post"
        self.command = "toggleBackend"

    @ApiBase._api_call
    def toggleCpu(self, *args):
        self.method = "post"
        self.command = "toggleCpu"

    @ApiBase._api_call
    def toggleFrontend(self, *args):
        self.method = "post"
        self.command = "toggleFrontend"

    @ApiBase._api_call
    def toggleGroup(self, *args):
        self.method = "post"
        self.command = "toggleGroup"

    @ApiBase._api_call
    def toggleLua(self, *args):
        self.method = "post"
        self.command = "toggleLua"

    @ApiBase._api_call
    def toggleServer(self, *args):
        self.method = "post"
        self.command = "toggleServer"

    @ApiBase._api_call
    def toggleUser(self, *args):
        self.method = "post"
        self.command = "toggleUser"

    @ApiBase._api_call
    def togglemailer(self, *args):
        self.method = "post"
        self.command = "togglemailer"

    @ApiBase._api_call
    def toggleresolver(self, *args):
        self.method = "post"
        self.command = "toggleresolver"

class Statistics(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "statistics"
    """
    Haproxy StatisticsController
    """

    @ApiBase._api_call
    def counters(self, *args):
        self.method = "get"
        self.command = "counters"

    @ApiBase._api_call
    def info(self, *args):
        self.method = "get"
        self.command = "info"

    @ApiBase._api_call
    def tables(self, *args):
        self.method = "get"
        self.command = "tables"
