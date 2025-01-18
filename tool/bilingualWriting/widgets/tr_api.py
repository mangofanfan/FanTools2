
from dataclasses import dataclass

from PySide6.QtCore import QObject


@dataclass
class TrAPI:
    name: str
    appid: str = None
    key: str = None


class APIs(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.apis = []
        self.__addApi(self.tr("BaiDuFanYi"))
        self.__addApi(self.tr("YouDaoFanYi"))

    def __addApi(self, name: str) -> None:
        self.apis.append(TrAPI(name))
        return None

    def getApis(self) -> list:
        return self.apis


apis = APIs()
