# coding: utf-8
import hashlib
import json

from PySide6.QtCore import QEventLoop
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from .error import UserCodeWrongError, APIError
from .network import QRequestReady


class Singleton(object):
    """
    A singleton class that provides a singleton.
    """
    def __init__(self, cls):
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self):
        if self.uniqueInstance is None:
            self.uniqueInstance = self._cls()
        return self.uniqueInstance


@Singleton
class LicenseService:
    """ License service """
    def __init__(self):
        self.email: str = None
        self.license: str = None
        self.datas: dict = None

        # self.url = "http://127.0.0.1:5000"
        self.url = "https://api-fan.mangofanfan.cn"

    def validate(self, license: str, email: str, signup: bool = False) -> bool:
        """ 验证是否允许登录 """
        if email == "" or email is None:
            return 1

        self.email = email
        self.license = license

        def thenDo(datas: dict) -> None:
            self.datas = datas
            return None

        eventLoop = QEventLoop()

        (QRequestReady(QApplication.instance())
         .get(f"{self.url}/v1/user/email?email={self.email}&code={self.__md5(license)}"
                       if license != ""
                       else f"{self.url}/v1/user/email?email={self.email}")
         .then(lambda res: thenDo(json.loads(res)))
         .then(lambda res: eventLoop.exit())
         .done()
         )

        eventLoop.exec_()

        if self.datas["status"] == "Error" and self.datas["message"] == "User not found.":
            if signup is False:
                return 2
            else:
                ((request := QRequestReady(QApplication.instance()))
                 .get(f"{self.url}/v1/user/signup?email={self.email}")
                 .then(lambda _: request.get(f"{self.url}/v1/user/email?email={self.email}"))
                 .then(lambda res: thenDo(json.loads(res)))
                 .done()
                 )
        elif self.datas["status"] == "Error" and self.datas["message"] == "Wrong code.":
            return 3

        return 0

    def getUserInfo(self, avatarFunc, nameFunc) -> None:
        """
        在主程序初始化之后，使用此方法获取email的头像和用户名。
        :return: None
        """
        self.getAvatar(avatarFunc, 96)
        nameFunc(self.datas["name"])

        return None

    def getAvatar(self, avatarFunc: callable, size: int) -> None:
        image = QImage()

        (
            QRequestReady(QApplication.instance())
             .get(f"https://cravatar.cn/avatar/{self.__md5(self.email.lower())}?s={size}")
             .then(lambda t: image.loadFromData(t))
             .then(lambda t: avatarFunc(image))
             .done()
        )

        return None

    def changeUserInfo(self, oldCode: str, name: str, newCode: str = "") -> int:

        global code
        eventLoop = QEventLoop()
        code = 0

        def thenDo(res: dict) -> None:
            global code
            if res["status"] == "SUCCESS":
                return None
            elif res["status"] == "Error" and "get wrong code." in res["message"]:
                code = 1
            else:
                code = -1

        (
            QRequestReady(QApplication.instance())
            .get(f"{self.url}/v1/user/edit?email={self.email}&old={self.__md5(oldCode)}&name={name}&new={self.__md5(newCode)}"
                 if newCode != "" else f"{self.url}/v1/user/edit?email={self.email}&old={self.__md5(oldCode)}&name={name}")
            .then(lambda t: thenDo(json.loads(t)))
            .then(lambda _: eventLoop.exit())
            .done()
        )

        eventLoop.exec_()
        return code

    def getNews(self, newsFunc: callable) -> None:
        """获取芒果工具箱的特供新闻……？"""
        def thenDo(_res: dict) -> None:
            newsFunc(_res["time"], _res["title"], _res["body"])
            return None
        (
            QRequestReady(QApplication.instance())
            .get(f"{self.url}/v1/news")
            .then(lambda res: thenDo(json.loads(res)[0]))
            .done()
        )
        return None

    @staticmethod
    def __md5(sth: str):
        if sth == "":
            return sth
        h = hashlib.md5()
        h.update(sth.encode("utf-8"))
        return h.hexdigest()

