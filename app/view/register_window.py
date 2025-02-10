# coding:utf-8
import json
import sys
from PySide6.QtCore import Qt, QTimer, QUrl, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (MSFluentTitleBar, isDarkTheme, ImageLabel, BodyLabel, LineEdit,
                            PasswordLineEdit, PrimaryPushButton, HyperlinkButton, CheckBox, InfoBar,
                            InfoBarPosition, setThemeColor, PushButton, CaptionLabel, ToolTip, ToolTipFilter)
from qfluentwidgets.window.stacked_widget import StackedWidget

from requests_oauthlib import OAuth2Session

from common.function import basicFunc
from common.setting import VERSION
from ..common import resource
from ..common.license_service import LicenseService
from ..common.config import cfg
from ..common.logger import logger
from ..common.fan_license_service import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, fanlive_url, fanlive_token, fanlive_me
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
        self.setResizeEnabled(False)
        self.setTitleBar(MSFluentTitleBar(self))
        self.register = LicenseService()
        self.hBoxLayout = QHBoxLayout(self)

        self.stackedWidget = StackedWidget(self)

        self.imageLabel = ImageLabel(':/app/images/BestWishes.jpg', self)
        self.iconLabel_LoginWithFan = ImageLabel(':/app/IconFanSpace', self)
        self.iconLabel_LoginWithEmail = ImageLabel(':/app/images/logo.png', self)

        self.returnButton1 = HyperlinkButton(self)
        self.returnButton1.setText(self.tr('Return'))
        self.returnButton1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.returnButton2 = HyperlinkButton(self)
        self.returnButton2.setText(self.tr('Return'))
        self.returnButton2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # 选择页面的组件
        self.widget_ChooseLoginMode = QWidget(self)
        self.vBoxLayout_ChooseLoginMode = QVBoxLayout()
        self.pushButton_LoginWithFan = PrimaryPushButton(self)
        self.pushButton_LoginWithFan.setText(self.tr('Login with FanSpace account'))
        self.pushButton_LoginWithFan.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.pushButton_LoginWithEmail = PushButton(self)
        self.pushButton_LoginWithEmail.setText(self.tr('Login with an email address'))
        self.pushButton_LoginWithEmail.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        # 帆域登录模式的组件
        self.widget_LoginWithFan = QWidget(self)
        self.vBoxLayout_LoginWithFan = QVBoxLayout()
        self.pushButton_OpenOauthWeb = PushButton(self)
        self.pushButton_OpenOauthWeb.setText(self.tr('Login with ifanspace.top'))
        self.pushButton_OpenOauthWeb.clicked.connect(self._loginWithFan)
        self.pushButton_UseSavedToken = PushButton(self)
        self.pushButton_UseSavedToken.setText(self.tr('Use saved token to login'))
        self.pushButton_UseSavedToken.setEnabled(self._loadFanToken())
        self.linkButton_Fan = HyperlinkButton(self)
        self.linkButton_Fan.setText(self.tr('Open ifanspace.top'))
        self.linkButton_Fan.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://ifanspace.top')))
        self.linkButton_Fan.setToolTip(self.tr("You may want to create a FanSpace account first?"))
        self.linkButton_Fan.installEventFilter(ToolTipFilter(self.linkButton_Fan))

        self.webEngineView = QWebEngineView()
        self.webEngineView.setWindowTitle(self.tr("Please login in this window as soon as possible ~"))
        self.webEngineView.setWindowIcon(QIcon(':/app/images/logo.png'))
        self.webEngineView.setFixedSize(QSize(640, 800))

        # Email 模式的组件
        self.widget_LoginWithEmail = QWidget(self)
        self.vBoxLayout_LoginWithEmail = QVBoxLayout()
        self.signupFlag = False
        self.emailLabel = BodyLabel(self.tr('Email'), self)
        self.emailLineEdit = LineEdit(self)
        self.emailLineEdit.textEdited.connect(self._emailChanged)

        self.activateCodeLabel = BodyLabel(self.tr('Activation Code'))
        self.activateCodeLineEdit = PasswordLineEdit(self)

        self.rememberCheckBox = CheckBox(self.tr('Remember me'), self)

        self.loginButton_Email = PrimaryPushButton(self.tr('Login'), self)


        self.__initWidgets()

        logger.success("登录窗口初始化完成。")

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
        self.resize(1100, 450)

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
        self.imageLabel.scaledToHeight(450)
        self.iconLabel_LoginWithFan.scaledToHeight(100)
        self.iconLabel_LoginWithEmail.scaledToHeight(100)

        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addWidget(self.stackedWidget)

        # 选择页面
        self.stackedWidget.addWidget(self.widget_ChooseLoginMode)
        self.widget_ChooseLoginMode.setLayout(self.vBoxLayout_ChooseLoginMode)

        self.vBoxLayout_ChooseLoginMode.addStretch(3)
        self.vBoxLayout_ChooseLoginMode.addWidget(self.pushButton_LoginWithFan)
        self.vBoxLayout_ChooseLoginMode.addSpacing(2)
        self.vBoxLayout_ChooseLoginMode.addWidget(self.pushButton_LoginWithEmail)
        self.vBoxLayout_ChooseLoginMode.addSpacing(5)
        self.vBoxLayout_ChooseLoginMode.addWidget(CaptionLabel(self.tr("Version:") + VERSION))
        self.vBoxLayout_ChooseLoginMode.addWidget(CaptionLabel(self.tr("Picture left from pixiv.")))
        self.vBoxLayout_ChooseLoginMode.addStretch(1)

        # 帆域登录模式
        self.stackedWidget.addWidget(self.widget_LoginWithFan)
        self.widget_LoginWithFan.setLayout(self.vBoxLayout_LoginWithFan)
        self.vBoxLayout_LoginWithFan.addStretch(1)

        self.vBoxLayout_LoginWithFan.addWidget(self.iconLabel_LoginWithFan, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout_LoginWithFan.addSpacing(9)
        bodyLabel = BodyLabel(self.tr('Using your FanSpace account on ifanspace.top to login.<br>'
                                      'ifanspace.top is a website powered by WordPress, designed by MangoFanFan.<br>'
                                      'You need to take actions on another window.'), self)
        bodyLabel.setWordWrap(True)
        self.vBoxLayout_LoginWithFan.addWidget(bodyLabel)
        self.vBoxLayout_LoginWithFan.addWidget(self.pushButton_OpenOauthWeb)
        self.vBoxLayout_LoginWithFan.addSpacing(2)
        self.vBoxLayout_LoginWithFan.addWidget(self.pushButton_UseSavedToken)
        self.vBoxLayout_LoginWithFan.addSpacing(2)
        self.vBoxLayout_LoginWithFan.addWidget(self.linkButton_Fan)
        self.vBoxLayout_LoginWithFan.addSpacing(9)
        self.vBoxLayout_LoginWithFan.addWidget(self.returnButton1)
        self.vBoxLayout_LoginWithFan.addStretch(1)

        # Email 登录模式
        self.stackedWidget.addWidget(self.widget_LoginWithEmail)
        self.widget_LoginWithEmail.setLayout(self.vBoxLayout_LoginWithEmail)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout_LoginWithEmail.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout_LoginWithEmail.setSpacing(0)
        self.hBoxLayout.setSpacing(0)

        self.vBoxLayout_LoginWithEmail.addStretch(1)
        self.vBoxLayout_LoginWithEmail.addWidget(self.iconLabel_LoginWithEmail, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout_LoginWithEmail.addSpacing(20)
        self.vBoxLayout_LoginWithEmail.addWidget(BodyLabel(self.tr('Login with an unchecked email address...'), self))
        self.vBoxLayout_LoginWithEmail.addSpacing(10)
        self.vBoxLayout_LoginWithEmail.addWidget(self.emailLabel)
        self.vBoxLayout_LoginWithEmail.addSpacing(11)
        self.vBoxLayout_LoginWithEmail.addWidget(self.emailLineEdit)
        self.vBoxLayout_LoginWithEmail.addSpacing(12)
        self.vBoxLayout_LoginWithEmail.addWidget(self.activateCodeLabel)
        self.vBoxLayout_LoginWithEmail.addSpacing(11)
        self.vBoxLayout_LoginWithEmail.addWidget(self.activateCodeLineEdit)
        self.vBoxLayout_LoginWithEmail.addSpacing(12)
        self.vBoxLayout_LoginWithEmail.addWidget(self.rememberCheckBox)
        self.vBoxLayout_LoginWithEmail.addSpacing(15)
        self.vBoxLayout_LoginWithEmail.addWidget(self.loginButton_Email)
        self.vBoxLayout_LoginWithEmail.addSpacing(10)
        self.vBoxLayout_LoginWithEmail.addWidget(self.returnButton2)
        self.vBoxLayout_LoginWithEmail.addSpacing(8)
        self.vBoxLayout_LoginWithEmail.addStretch(1)

    def __connectSignalToSlot(self):
        self.loginButton_Email.clicked.connect(self._loginWithEmail)
        self.rememberCheckBox.stateChanged.connect(
            lambda: cfg.set(cfg.rememberMe, self.rememberCheckBox.isChecked()))
        logger.trace("根据相关设置调整「记住我」选择框状态。")

    def _loginWithEmail(self):
        logger.trace("尝试执行登录。")
        email = self.emailLineEdit.text().strip()
        code = self.activateCodeLineEdit.text().strip()

        def login():
            if cfg.get(cfg.rememberMe):
                cfg.set(cfg.email, self.emailLineEdit.text().strip())
                cfg.set(cfg.activationCode, code)

            self.loginButton_Email.setDisabled(True)
            QTimer.singleShot(1500, self._showMainWindow)

        if (reCode := self.register.validate_email(code, email, self.signupFlag)) == 1:
            logger.error("登录失败，输入的电子邮件地址不合法。")
            InfoBar.error(
                self.tr("Activate failed"),
                self.tr('Please input a legal email address'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        elif reCode == 3:
            logger.error("登录失败，激活码与电子邮件地址不匹配或错误。")
            InfoBar.error(
                self.tr("Activate failed"),
                self.tr("Please input right activation code to login this account"),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        elif reCode == 2 and self.signupFlag is False:
            logger.info("使用的邮件地址尚未注册，再次使用该地址登录以创建新用户并完成登录。")
            InfoBar.warning(
                self.tr("Wait for activation"),
                self.tr('This email address has not been registered.\n'
                        'Try again to register now, or change another address.'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            self.signupFlag = True
            logger.debug("已对该电子邮件地址标注待激活状态。")
        elif reCode == 2 and self.signupFlag is True:
            logger.success("成功创建新用户并登录。")
            InfoBar.success(
                self.tr("Success"),
                self.tr('This email address has been activated.'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            login()
        else:
            logger.success("成功登录。")
            InfoBar.success(
                self.tr("Success"),
                self.tr('Activated successful'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
            login()

        logger.debug(f"本次登录使用用户：{email}")

    def _emailChanged(self):
        self.signupFlag = False
        logger.debug("电子邮件地址更改，待激活状态取消。")
        return None

    def _loginWithFan(self):

        def urlChanged():
            if self.webEngineView.url().toString().startswith("http://localhost:8080/"):
                AUTH_RES = self.webEngineView.url().toString()
                self.webEngineView.close()
                token_datas = self.oauthClient.fetch_token(token_url=fanlive_token, client_secret=CLIENT_SECRET, authorization_response=AUTH_RES)

                self.__loginWithFan(token_datas)
            return None

        # 禁用使用保存凭证登录按钮
        self.pushButton_UseSavedToken.setDisabled(True)

        self.oauthClient = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                         auto_refresh_url=fanlive_url, token_updater=token_saver)

        AUTH_URL, state = self.oauthClient.authorization_url(url=fanlive_url)
        logger.debug(f"帆域 Oauth 第一步返回：{AUTH_URL} | {state}")

        self.webEngineView.setUrl(QUrl(AUTH_URL))
        self.webEngineView.show()
        self.webEngineView.urlChanged.connect(urlChanged)
        logger.info("展示 Oauth 验证登录窗口。")

        return None

    def __loginWithFan(self, token_datas: dict[str, str]) -> None:

        datas = self.oauthClient.get(fanlive_me).json()

        InfoBar.success(title=self.tr("Login successful"),
                        content=self.tr("Successfully login with a FanSpace account."),
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self.window())

        logger.success("帆域 Oauth 登录成功。")
        self.register.validate_fan(datas)
        token_saver(token_datas)
        QTimer.singleShot(1500, self._showMainWindow)

        # 禁用按钮防止重复登录
        self.pushButton_UseSavedToken.setDisabled(True)
        self.pushButton_LoginWithFan.setDisabled(True)

        return None

    def _loadFanToken(self) -> bool:
        if (token_datas := token_loader()) == {}:
            return False

        token_datas["expires_in"] = -1
        token_datas["expires_at"] = 1600000000.123456

        try:
            self.oauthClient = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                             auto_refresh_url=fanlive_token,
                                             token_updater=token_saver,
                                             auto_refresh_kwargs={"client_id": CLIENT_ID,
                                                                  "client_secret": CLIENT_SECRET},
                                             token={"access_token": token_datas.get("refresh_token"),
                                                    "refresh_token": token_datas.get("refresh_token"),
                                                    "expires_in": token_datas.get("expires_in"),
                                                    "token_type": token_datas.get("token_type")})
            self.oauthClient.refresh_token(fanlive_token)
            logger.debug("已刷新保存的帆域 Oauth 令牌，可快速登录。")
        except:
            self.pushButton_UseSavedToken.setToolTip(self.tr("You need to login first to get a saved token."))
            self.pushButton_UseSavedToken.installEventFilter(ToolTipFilter(self.pushButton_UseSavedToken))
            return False

        self.pushButton_UseSavedToken.clicked.connect(lambda: self.__loginWithFan(token_datas))
        return True

    def _showMainWindow(self):
        self.close()
        setThemeColor('#009faa')

        logger.debug("关闭登录窗口，启动工具箱主窗口。")

        w = MainWindow()
        w.show()
        logger.trace("工具箱主窗口已经显示，登录流程结束。")



def token_saver(token: dict[str, str]) -> None:
    with open(file=basicFunc.getHerePath()+"/AppData/oauth-fan.json", mode="w", encoding="utf-8") as f:
        f.write(json.dumps(token, indent=4))
    logger.trace("帆域 Oauth 登录凭证已经保存至数据目录下。")
    return None

def token_loader() -> dict[str, str]:
    try:
        with open(file=basicFunc.getHerePath()+"/AppData/oauth-fan.json", mode="r", encoding="utf-8") as f:
            logger.trace("读取已保存的帆域 Oauth 登录凭证。")
            return json.loads(f.read())
    except FileNotFoundError:
        logger.trace("未发现已保存的帆域 Oauth 登录凭证。")
        return {}
