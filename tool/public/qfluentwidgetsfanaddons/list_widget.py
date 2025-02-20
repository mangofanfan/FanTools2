from typing import overload

from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QMenu, QListWidgetItem
from qfluentwidgets import RoundMenu
from qfluentwidgetspro import RoundListWidget

from .enum import RightClickMenuMode


class FanRoundListWidget(RoundListWidget):

    RightClickItem = Signal(QListWidgetItem)

    def __init__(self, parent=None):
        super(FanRoundListWidget, self).__init__(parent)
        self._mode = RightClickMenuMode.NeverShow

    @overload
    def setRightClickMenu(self, menu: RoundMenu | QMenu, mode: RightClickMenuMode): ...
    @overload
    def setRightClickMenu(self, menu: RoundMenu | QMenu, menu2: RoundMenu | QMenu): ...

    def setRightClickMenu(self, menu: RoundMenu | QMenu, menu2: RoundMenu | QMenu, mode: RightClickMenuMode = None) -> None:
        """
        传入一个或两个菜单实例。在传入一个菜单时，需要设置菜单显示条件。

        不应该以 keyword 形式传入参数。
        """
        if mode is not None: raise ValueError("Too Many args!")
        if type(menu2) == RightClickMenuMode:
            mode = menu2
            self._menu = menu
            self._mode = mode
        else:
            self._menu = menu
            self._menu2 = menu2
        return None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super(FanRoundListWidget, self).mousePressEvent(e)
        if item := self.itemAt(e.pos()): self.RightClickItem.emit(item)
        if not hasattr(self, "_menu"): return
        if hasattr(self, "_menu2"):
            if e.button() == Qt.MouseButton.RightButton:
                if self.itemAt(e.pos()):
                    self._menu2.exec(e.globalPos())
                else:
                    self._menu.exec(e.globalPos())
            return
        if self._mode == RightClickMenuMode.NeverShow: return
        if e.button() == Qt.MouseButton.RightButton:
            if self._mode == RightClickMenuMode.OnItemShow and not self.itemAt(e.pos()): return
            self._menu.exec(e.globalPos())
        return
