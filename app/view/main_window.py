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
from .widgets.check_update import UpdateChecker
from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource
from ..common.logger import logger


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

        # 如果设置启用启动时检查版本
        if cfg.get(cfg.checkUpdateAtStartUp):
            logger.debug("由于相关设置，开始启动时检查版本更新。")
            self.checkUpdate()

        logger.success("工具箱主窗口初始化完毕。")

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.checkUpdateSig.connect(self.checkUpdate)

        logger.trace("工具箱主窗口信号连接完毕。")

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

        logger.trace("工具箱侧边导航初始化完毕。")

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

        logger.trace("工具箱主窗口初始化完毕。")

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def checkUpdate(self):
        """检查版本更新"""
        logger.trace("开始检查版本更新。")
        from .widgets.need_update_info_bar import UpdateInfoBar
        uib = UpdateInfoBar(self)
        self.updateChecker = UpdateChecker()
        if self.updateChecker.isNeedUpdate():
            logger.info("发现更新版本，需要更新工具箱。")
            uib.update_true(self, self.updateChecker.getLatestVersion())
        else:
            logger.info("工具箱当前版本已是最新。")
            uib.update_false(self, self.updateChecker.getLatestVersion())
