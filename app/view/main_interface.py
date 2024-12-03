# coding:utf-8
from PySide6.QtCore import QSize, QFile, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget
from qfluentwidgets import BodyLabel
from qfluentwidgets import FluentIcon as FIC

from .designer.main_interface import Ui_Form as MainForm
from .widgets.account_edit_info_box import AccountEditInfoBox
from ..common import resource
from ..common.license_service import LicenseService
from ..common.setting import VERSION


class MainInterface(QWidget, MainForm):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        self.setObjectName('MainInterface')
        self.ls = LicenseService()
        self.initWindow()

    def initWindow(self) -> None:
        # 设置头像
        self.AvatarWidget.setImage(QImage(':/app/images/avatar.png'))
        self.AvatarWidget.setScaledSize(QSize(96, 96))
        self.AvatarWidget.setRadius(48)

        # 设置信息卡片组
        self.BodyLabel_AccountInfo.setText(self.tr("Account UUID:") + "123456789")
        self.BodyLabel_SoftwareInfo.setText(self.tr("Software Version:") + VERSION)

        # 设置软件简介卡片
        self.HeaderCardWidget.setTitle(self.tr("Software Information"))
        tipFile = QFile(":/app/texts/main_tip.md")
        tipFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        BodyLabel_tip = BodyLabel()
        BodyLabel_tip.setText(str(tipFile.readAll(), "utf-8"))
        self.HeaderCardWidget.viewLayout.addWidget(BodyLabel_tip)
        tipFile.close()

        # 允许编辑用户资料
        self.ToolButton_EditAccount.setIcon(FIC.EDIT)
        self.ToolButton_EditAccount.clicked.connect(self._openEditAccountInfoBox)

        self._loadUserInfo()

        return None

    def _loadUserInfo(self) -> None:
        self.ls.getUserInfo(self.AvatarWidget.setImage, None)
        return None

    def _openEditAccountInfoBox(self) -> None:
        infoBox = AccountEditInfoBox("MangoFanFan",
                                     "1234567898",
                                     self.ls.email,
                                     self._parent)
        infoBox.show()
        return None

    def _closeEditAccountInfoBox(self) -> None:
        return None
