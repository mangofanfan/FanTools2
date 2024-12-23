# coding:utf-8
import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (MSFluentTitleBar, isDarkTheme, ImageLabel, BodyLabel, LineEdit,
                            PasswordLineEdit, PrimaryPushButton, HyperlinkButton, CheckBox, InfoBar,
                            InfoBarPosition, setThemeColor)
from ..common import resource
from ..common.license_service import LicenseService
from ..common.config import cfg
from .main_window import MainWindow


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class RegisterWindow(Window):
    """ Register window """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        setThemeColor('#28afe9')
        self.setTitleBar(MSFluentTitleBar(self))
        self.register = LicenseService()
        self.signupFlag = False

        self.imageLabel = ImageLabel(':/app/images/background.jpg', self)
        self.iconLabel = ImageLabel(':/app/images/logo.png', self)

        self.emailLabel = BodyLabel(self.tr('Email'), self)
        self.emailLineEdit = LineEdit(self)
        self.emailLineEdit.textEdited.connect(self._emailChanged)

        self.activateCodeLabel = BodyLabel(self.tr('Activation Code'))
        self.activateCodeLineEdit = PasswordLineEdit(self)

        self.rememberCheckBox = CheckBox(self.tr('Remember me'), self)

        self.loginButton = PrimaryPushButton(self.tr('Login'), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.__initWidgets()

    def __initWidgets(self):
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.rememberCheckBox.setChecked(cfg.get(cfg.rememberMe))

        self.emailLineEdit.setPlaceholderText('example@example.com')
        self.activateCodeLineEdit.setPlaceholderText(self.tr('Type in here if you have ...'))

        if self.rememberCheckBox.isChecked():
            self.emailLineEdit.setText(cfg.get(cfg.email))
            self.activateCodeLineEdit.setText(cfg.get(cfg.activationCode))

        self.__connectSignalToSlot()
        self.__initLayout()

        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            color = QColor(25, 33, 42) if isDarkTheme(
            ) else QColor(240, 244, 249)
            self.setStyleSheet(f"RegisterWindow{{background: {color.name()}}}")

        self.setWindowTitle(self.tr('FanTools-Login'))
        self.setWindowIcon(QIcon(":/app/images/logo.png"))
        self.resize(1000, 650)

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.titleBar.raise_()

    def __initLayout(self):
        self.imageLabel.scaledToHeight(650)
        self.iconLabel.scaledToHeight(100)

        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(0)
        self.hBoxLayout.setSpacing(0)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(
            self.iconLabel, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addSpacing(38)
        self.vBoxLayout.addWidget(self.emailLabel)
        self.vBoxLayout.addSpacing(11)
        self.vBoxLayout.addWidget(self.emailLineEdit)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.activateCodeLabel)
        self.vBoxLayout.addSpacing(11)
        self.vBoxLayout.addWidget(self.activateCodeLineEdit)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.rememberCheckBox)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.loginButton)
        self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addStretch(1)

    def __connectSignalToSlot(self):
        self.loginButton.clicked.connect(self._login)
        self.rememberCheckBox.stateChanged.connect(
            lambda: cfg.set(cfg.rememberMe, self.rememberCheckBox.isChecked()))

    def _login(self):
        code = self.activateCodeLineEdit.text().strip()

        def login():
            if cfg.get(cfg.rememberMe):
                cfg.set(cfg.email, self.emailLineEdit.text().strip())
                cfg.set(cfg.activationCode, code)

            self.loginButton.setDisabled(True)
            QTimer.singleShot(1500, self._showMainWindow)

        if (reCode := self.register.validate(code, self.emailLineEdit.text(), self.signupFlag)) == 1:
            InfoBar.error(
                self.tr("Activate failed"),
                self.tr('Please input a legal email address'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        elif reCode == 3:
            InfoBar.error(
                self.tr("Activate failed"),
                self.tr("Please input right activation code to login this account"),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        elif reCode == 2 and self.signupFlag is False:
            InfoBar.warning(
                self.tr("Wait for activation"),
                self.tr('This email address has not been registered.\n'
                        'Try again to register now, or change another address.'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            self.signupFlag = True
        elif reCode == 2 and self.signupFlag is True:
            InfoBar.warning(
                self.tr("Success"),
                self.tr('This email address has been activated.'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            login()
        else:
            InfoBar.success(
                self.tr("Success"),
                self.tr('Activated successful'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            login()

    def _emailChanged(self):
        self.signupFlag = False
        return None

    def _showMainWindow(self):
        self.close()
        setThemeColor('#009faa')

        w = MainWindow()
        w.show()
