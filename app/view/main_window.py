# coding: utf-8
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from .main_interface import MainInterface
from .setting_interface import SettingInterface
from .tool_interface import ToolInterface
from .about_interface import AboutInterface
from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.mainInterface = MainInterface(self)
        self.toolInterface = ToolInterface(self)
        self.settingInterface = SettingInterface(self)
        self.aboutInterface = AboutInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        # self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(
            self.mainInterface, FIF.HOME, self.tr("Main"), FIF.HOME_FILL, NavigationItemPosition.TOP)
        self.addSubInterface(
            self.toolInterface, FIF.APPLICATION, self.tr("Tools"), FIF.APPLICATION, NavigationItemPosition.TOP)

        # add custom widgets to bottom
        self.addSubInterface(
            self.aboutInterface, FIF.QUESTION, self.tr("About"), FIF.QUESTION, NavigationItemPosition.BOTTOM)
        self.addSubInterface(
            self.settingInterface, Icon.SETTINGS, self.tr('Settings'), Icon.SETTINGS_FILLED, NavigationItemPosition.BOTTOM)

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/app/images/logo.png'))
        self.setWindowTitle(self.tr('FanTools-Main'))

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        # add style
        self.setStatusTip('QScrollArea {background: transparent; }'
                          'QFrame {background: transparent; }'
                          'QWidget {background: transparent; }')

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())