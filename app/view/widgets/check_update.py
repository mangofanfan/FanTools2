from app.common.license_service import LicenseService, Singleton
from app.common.setting import VERSION


@Singleton
class UpdateChecker:
    def __init__(self):
        ls = LicenseService()
        data = ls.getVersion()
        self.latest: str = data["latest"]
        self.desc: dict = data["desc"]

    def getLatestVersion(self):
        return self.latest

    def getDesc(self):
        return self.desc

    def isNeedUpdate(self):
        return True if VERSION != self.getLatestVersion() else False

