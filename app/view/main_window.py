# coding: utf-8
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QColor, QCloseEvent, QResizeEvent, QDesktopServices, QShowEvent
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, SystemTrayMenu, Action
from qfluentwidgets import FluentIcon as FIF

from common.setting import DOC_URL
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
        self.isExited = False
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

        # 如果设置允许系统托盘图标功能
        if cfg.get(cfg.trayIcon):
            self.systemTrayIcon = FanSystemTrayIcon(self)

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
        self.navigationInterface.addItem("Quit", FIF.STOP_WATCH, self.tr("Quit"), self.exitFanTools, True, FIF.STOP_WATCH, NavigationItemPosition.BOTTOM)

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

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

        logger.trace("工具箱主窗口初始化完毕。")

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def closeEvent(self, e: QCloseEvent):
        if not cfg.get(cfg.trayIcon):
            super().closeEvent(e)
            return None
        if not self.isExited:
            e.ignore()
            self.systemTrayIcon.showHideTip()
            self.hide()
            logger.info("工具箱已经隐藏至系统托盘。")
        return None

    def showEvent(self, e: QShowEvent):
        if cfg.get(cfg.trayIcon):
            logger.info("工具箱已经重新显示。")
        super().showEvent(e)
        return None

    def exitFanTools(self) -> None:
        """真正退出工具箱的函数"""
        self.isExited = True
        QApplication.instance().quit()
        logger.success("工具箱已退出，感谢使用。")
        return None

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


class FanSystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent: MSFluentWindow):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self._parent = parent

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action(text=self.tr("💡 Show Main Window"), triggered=self._parent.show),
            Action(text=self.tr("📖 Open FanTools Docs"), triggered=lambda: QDesktopServices.openUrl(QUrl(DOC_URL))),
            Action(text=self.tr("🚪 Exit FanTools"), triggered=self._parent.exitFanTools),
        ])
        self.setContextMenu(self.menu)

        self.show()

        logger.trace("初始化并显示系统托盘图标。")

    def showHideTip(self) -> None:
        """工具箱方法，如果系统支持，向桌面发送窗口关闭的消息，否则不做处理。"""
        if self.supportsMessages():
            self.showMessage(self.tr("FanTools Main Window has been hidden."),
                             self.tr("You can re-open it by right-clicking FanTools icon in System Tray."),
                             QIcon(':/app/images/logo.png'),
                             5000)
            logger.trace("向桌面发送工具箱窗口关闭消息。")
        else:
            logger.trace("系统不支持桌面消息，因此未向桌面发送窗口关闭消息。")
        return None

