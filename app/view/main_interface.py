# coding:utf-8
from PySide6.QtCore import QSize, QFile
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget
from qfluentwidgets import BodyLabel

from .designer.main_interface import Ui_Form as MainForm
from ..common import resource
from ..common.setting import VERSION


class MainInterface(QWidget, MainForm):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setObjectName('MainInterface')
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
        tipFile.open(QFile.ReadOnly | QFile.Text)
        BodyLabel_tip = BodyLabel()
        BodyLabel_tip.setText(str(tipFile.readAll(), "utf-8"))
        self.HeaderCardWidget.viewLayout.addWidget(BodyLabel_tip)
        tipFile.close()

        return None
