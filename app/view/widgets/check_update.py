from enum import Enum

from app.common.license_service import LicenseService, Singleton
from app.common.setting import VERSION


class UpdateStatus(Enum):
    Latest = "Latest"
    Dev = "Dev"
    NeedUpdate = "NeedUpdate"


@Singleton
class UpdateChecker:
    def __init__(self):
        ls = LicenseService()
        data = ls.getVersion()
        self.latest: str = data["latest"]
        try:
            self.dev: str = data["dev"]
        except KeyError:
            self.dev = self.latest
        self.desc: dict = data["desc"]

    def getLatestVersion(self):
        return self.latest

    def getDevVersion(self):
        return self.dev

    def getDesc(self):
        return self.desc

    def isNeedUpdate(self) -> UpdateStatus:
        if VERSION == self.dev:
            return UpdateStatus.Dev
        return UpdateStatus.NeedUpdate if VERSION != self.getLatestVersion() else UpdateStatus.Latest

