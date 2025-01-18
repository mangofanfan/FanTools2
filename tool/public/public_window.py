import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from qfluentwidgets import isDarkTheme, qconfig, FluentTitleBar
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

from app.common.function import basicFunc


class FanTitleBar(FluentTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(20, 0, 0, 0)


class FanWindow(BackgroundAnimationWidget, FramelessWindow):

    windowResizeSignal = Signal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isMicaEnabled = False
        self._isAcrylicEnabled = False
        self._lightBackgroundColor_int = (243, 243, 243)
        self._darkBackgroundColor_int = (32, 32, 32)
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)

        self.setMicaEffectEnabled(True)

        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)
        self.setTitleBar(FanTitleBar(self))

    def centerWindow(self):
        # TODO
        pass

    def setMicaEffectEnabled(self, isEnabled: bool):
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def getBackgroundColor(self, _hex: bool = False):
        if _hex:
            if isDarkTheme():
                return basicFunc.rgb_to_hex(self._darkBackgroundColor_int)
            else:
                return basicFunc.rgb_to_hex(self._lightBackgroundColor_int)
        else:
            return self.bgColorObject.backgroundColor

    def setAcrylicEffectEnabled(self, isEnabled: bool):
        self._isAcrylicEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setAcrylicEffect(self.winId(), self.getBackgroundColor(True))
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self.getBackgroundColor())

    def isAcrylicEffectEnabled(self):
        return self._isAcrylicEnabled

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        if self.isAcrylicEffectEnabled():
            self.windowEffect.setAcrylicEffect(self.winId(), self.getBackgroundColor(True))

    def resizeEvent(self, event):
        self.windowResizeSignal.emit()
        super().resizeEvent(event)
        return None
