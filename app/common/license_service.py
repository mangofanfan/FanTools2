# coding: utf-8
import hashlib

from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

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

    def validate(self, license: str, email: str) -> bool:
        """ 验证是否允许登录 """
        if email == "" or email is None:
            return False

        self.email = email
        self.license = license

        return True

    def getUserInfo(self, avatarFunc, nameFunc) -> None:
        """
        在主程序初始化之后，使用此方法获取email的头像和用户名。
        :return: None
        """
        self.getAvatar(avatarFunc, 96)

        # TODO 用户名系统！

        return None

    def getAvatar(self, avatarFunc, size: int) -> None:
        image = QImage()

        (QRequestReady(QApplication.instance())
         .get(f"https://cravatar.cn/avatar/{self.__md5(self.email.lower())}?s={size}")
         .then(lambda t: image.loadFromData(t))
         .then(lambda t: avatarFunc(image))
         .done())

        return None

    @staticmethod
    def __md5(email: str):
        h = hashlib.md5()
        h.update(email.encode("utf-8"))
        return h.hexdigest()

