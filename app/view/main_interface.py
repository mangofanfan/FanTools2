# coding:utf-8
from PySide6.QtCore import QSize, QFile, QIODevice, Slot
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget
from qfluentwidgets import BodyLabel, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIC

from .designer.main_interface import Ui_Form as MainForm
from .widgets.account_edit_info_box import AccountEditInfoBox
from ..common import resource
from ..common.license_service import LicenseService
from ..common.hitokoto import HitokotoManager
from ..common.setting import VERSION
from ..common.signal_bus import signalBus
from ..common.logger import logger


class MainInterface(QWidget, MainForm):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        self.setObjectName('MainInterface')
        self.ls = LicenseService()
        self.hm = HitokotoManager()
        self.initWindow()

    def initWindow(self) -> None:
        # 设置头像
        self.AvatarWidget.setImage(QImage(':/app/images/avatar.png'))
        self.AvatarWidget.setScaledSize(QSize(96, 96))
        self.AvatarWidget.setRadius(48)

        # 设置信息卡片组
        self.BodyLabel_SoftwareInfo.setText(self.tr("Software Version:") + VERSION)
        self.BodyLabel_AccountInfo.setText(self.tr("Account UUID:") + "Unknown QAQ")

        # 设置软件简介卡片
        self.HeaderCardWidget.setTitle(self.tr("Software Information"))
        tipFile = QFile(":/app/texts/main_tip.md")
        tipFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        BodyLabel_tip = BodyLabel()
        BodyLabel_tip.setText(str(tipFile.readAll(), "utf-8"))
        self.HeaderCardWidget.viewLayout.addWidget(BodyLabel_tip)
        tipFile.close()

        # 初始化一言卡片
        self._loadYiYan()
        self.ElevatedCardWidget_YiYan.clicked.connect(self._updateYiYan)
        signalBus.hitokotoUpdate.connect(self._loadYiYan)

        # 允许编辑用户资料
        self.ToolButton_EditAccount.setIcon(FIC.EDIT)
        self.ToolButton_EditAccount.clicked.connect(self._openEditAccountInfoBox)

        logger.info("工具箱主页初始化完毕。")

        self._loadUserInfo()
        logger.success("工具箱主页加载完毕。")

        return None

    def _loadUserInfo(self) -> None:
        self.ls.getUserInfo(self.AvatarWidget.setImage, self.LargeTitleLabel_AccountName.setText)
        logger.info("已将用户信息应用在工具箱主页上。")
        return None

    def _openEditAccountInfoBox(self) -> None:
        infoBox = AccountEditInfoBox(self.ls.datas["name"],
                                     self.ls.datas["id"],
                                     self.ls.email,
                                     self._parent)
        infoBox.successSignal.connect(self._closeEditAccountInfoBox)
        infoBox.show()
        logger.info("打开工具箱主页的用户信息编辑框。")
        return None

    def _closeEditAccountInfoBox(self) -> None:
        InfoBar.success(
            self.tr("Success"),
            self.tr("Your Account Info has been changed."),
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self._parent
        )
        logger.success("成功更新用户信息并关闭用户信息编辑框。")
        self._loadUserInfo()
        return None

    def _updateYiYan(self) -> None:
        logger.trace("从工具箱主页立即刷新一言。")
        self.hm.updateNow()
        return None

    @Slot()
    def _loadYiYan(self) -> None:
        logger.trace("更新工具箱主页的一言卡片。")
        self.BodyLabel_YiYan.setText(self.hm.hitokoto.text)
        self.StrongBodyLabel_YiYan.setText(self.hm.hitokoto.by)
        return None
