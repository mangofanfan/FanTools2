# coding: utf-8
import hashlib
import json

from PySide6.QtCore import QEventLoop
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from .error import UserCodeWrongError, APIError
from .function import Singleton
from .network import QRequestReady
from .logger import logger


@Singleton
class LicenseService:
    """ License service """

    def __init__(self):
        self.email: str = None
        self.license: str = None
        self.datas: dict = None

        # self.url = "http://127.0.0.1:5000"
        self.url = "https://api-fan.mangofanfan.cn"

        logger.trace("许可证管理器初始化完毕。")

    def validate_email(self, license: str, email: str, signup: bool = False) -> int:
        """ 验证是否允许登录 """
        if email == "" or email is None:
            return 1

        self.email = email
        self.license = license

        def thenDo(datas: dict) -> None:
            self.datas = datas
            logger.success("已获取到用户信息，登录成功。")
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
                logger.info(f"当前邮箱 {email} 未注册用户，再次使用该邮箱登录将自动注册用户并登录。")
                return 2
            else:
                ((request := QRequestReady(QApplication.instance()))
                 .get(f"{self.url}/v1/user/signup?email={self.email}")
                 .then(lambda _: request.get(f"{self.url}/v1/user/email?email={self.email}"))
                 .then(lambda res: thenDo(json.loads(res)))
                 .done()
                 )
                logger.trace("已经异步申请创建新账户。")
        elif self.datas["status"] == "Error" and self.datas["message"] == "Wrong code.":
            logger.error(f"邮箱 {email}] 的激活码错误，拒绝登录。")
            return 3

        return 0

    def validate_fan(self, datas: dict) -> None:
        self.email = datas["user_email"]
        self.license = None
        self.datas = {"_name": datas["user_login"],
                      "name": datas["display_name"],
                      "id": datas["ID"],
                      "other": datas["zib_other_data"]}
        logger.success("许可证管理器已保存帆域 Oauth 登录结果。")
        return None

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

        url = f"https://cravatar.cn/avatar/{self.__md5(self.email.lower())}?s={size}" if not self.license else self.datas["other"]["custom_avatar"]

        (
            QRequestReady(QApplication.instance())
            .get(url)
            .then(lambda t: image.loadFromData(t))
            .then(lambda t: avatarFunc(image))
            .done()
        )
        logger.trace(f"开始异步加载尺寸为 {size} 的用户头像。（若为 Oauth 登录方式无法指定大小）")

        return None

    def changeUserInfo(self, oldCode: str, name: str, newCode: str = "") -> int:
        if not self.license:
            logger.error("无法更改 Oauth 方式登录的用户信息！")
            return -2

        logger.debug("提交了用户信息更改。")

        global code
        eventLoop = QEventLoop()
        code = 0

        def thenDo(res: dict) -> None:
            global code
            if res["status"] == "SUCCESS":
                logger.success("用户信息更改成功。")
                return None
            elif res["status"] == "Error" and "get wrong code." in res["message"]:
                logger.error("用户信息更改失败，提供的激活码有误。")
                code = 1
            else:
                logger.error("未知原因，但是用户信息更改失败。")
                code = -1

        (
            QRequestReady(QApplication.instance())
            .get(
                f"{self.url}/v1/user/edit?email={self.email}&old={self.__md5(oldCode)}&name={name}&new={self.__md5(newCode)}"
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
            logger.debug(f"获取并更新了工具箱新闻 {_res}。")
            return None

        (
            QRequestReady(QApplication.instance())
            .get(f"{self.url}/v1/news")
            .then(lambda res: thenDo(json.loads(res)[0]))
            .done()
        )
        logger.trace("开始异步加载工具箱新闻。")
        return None

    def getVersion(self):
        global data

        def thenDo(_res: dict) -> None:
            global data
            data = _res

        eventLoop = QEventLoop()
        (
            QRequestReady(QApplication.instance())
            .get(f"{self.url}/v1/version")
            .then(lambda res: thenDo(json.loads(res)))
            .then(lambda _: eventLoop.exit())
            .done()
        )
        eventLoop.exec_()
        logger.debug(f"获取工具箱当前版本信息 {data} 。")
        return data

    @staticmethod
    def __md5(sth: str):
        if sth == "":
            return sth
        h = hashlib.md5()
        h.update(sth.encode("utf-8"))
        logger.trace(f"计算了邮箱 {sth} 的MD5。")
        return h.hexdigest()
