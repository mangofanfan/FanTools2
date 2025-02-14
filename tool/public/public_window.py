from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTitleBar

from app.common.signal_bus import signalBus
from app.common.config import cfg

from ._public_window_base import FanWindowBase


class FanTitleBar(FluentTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(20, 0, 0, 0)


class FanWindow(FanWindowBase):
    """
    PS：只能在launchMode为0时导入使用

    PySide6 + QFluentWidgets 实现的基础窗口类，已经封装成与工具箱一同切换视觉效果，此窗口中没有任何组件与布局
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(FanTitleBar(self))

        # 信号
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def centerWindow(self):
        """ 窗口屏幕居中，与 show() 一起使用 """
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        return None


