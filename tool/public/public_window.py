from PySide6.QtCore import Signal
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
    """只能在launchMode为0时导入使用"""
    windowResizeSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(FanTitleBar(self))

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def centerWindow(self):
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        return None

    def resizeEvent(self, event):
        self.windowResizeSignal.emit()
        super().resizeEvent(event)
        return None

