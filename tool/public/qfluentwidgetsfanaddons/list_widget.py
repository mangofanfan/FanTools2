from typing import overload

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QMenu, QListWidgetItem, QListWidget
from qfluentwidgets import RoundMenu, ListWidget
from qfluentwidgetspro import RoundListWidget

from .enum import RightClickMenuMode


class QListWidgetProtocol:
    def itemAt(self, pos: QPoint) -> QListWidgetItem | None: ...
    def contextMenuPolicy(self) -> Qt.ContextMenuPolicy: ...
    def setContextMenuPolicy(self, policy: Qt.ContextMenuPolicy) -> None: ...
    def hasAttribute(self, attr: str) -> bool: ...
    def mousePressEvent(self, e: QMouseEvent) -> None: ...


class MouseClickFanAddon(QListWidgetProtocol):
    """ 增强处理鼠标事件的核心 """

    RightClickItem = Signal(QListWidgetItem)

    def __init__(self):
        self._mode = RightClickMenuMode.NeverShow
        self._leftClickEnabled = True

    @overload
    def setRightClickMenu(self, menu: RoundMenu | QMenu, mode: RightClickMenuMode): ...
    @overload
    def setRightClickMenu(self, menu: RoundMenu | QMenu, menu2: RoundMenu | QMenu): ...

    def setRightClickMenu(self, menu: RoundMenu | QMenu, menu2: RoundMenu | QMenu, mode: RightClickMenuMode = None) -> None:
        """
        传入一个或两个菜单实例。在传入一个菜单时，需要设置菜单显示条件。

        每次调用此函数设置右键菜单时，先前的设置都会被覆盖。

        不应该以 keyword 形式传入参数。
        """
        if mode is not None: raise ValueError("Too Many args!")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        try: del self._menu
        except AttributeError: pass
        try: del self._menu2
        except AttributeError: pass
        if type(menu2) == RightClickMenuMode:
            mode = menu2
            self._menu = menu
            self._mode = mode
        else:
            self._menu = menu
            self._menu2 = menu2
        return None

    def setLeftClickEnabled(self, isEnabled: bool) -> None:
        """ 设置是否处理左键点击事件，一般用于取消列表组件的选中功能，或从代码层面完全接管选中功能 """
        self._leftClickEnabled = isEnabled
        return None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton and not self._leftClickEnabled: return
        super().mousePressEvent(e)
        if item := self.itemAt(e.pos()): self.RightClickItem.emit(item)
        if not hasattr(self, "_menu"): return
        if hasattr(self, "_menu2"):
            if e.button() == Qt.MouseButton.RightButton:
                if self.itemAt(e.pos()): self._menu2.exec(e.globalPos())
                else: self._menu.exec(e.globalPos())
            return
        if self._mode == RightClickMenuMode.NeverShow: return
        if e.button() == Qt.MouseButton.RightButton:
            if self._mode == RightClickMenuMode.OnItemShow and not self.itemAt(e.pos()): return
            self._menu.exec(e.globalPos())
        return


class FanQListWidget(MouseClickFanAddon, QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        MouseClickFanAddon.__init__(self)


class FanListWidget(MouseClickFanAddon, ListWidget):
    def __init__(self, parent=None):
        ListWidget.__init__(self, parent)
        MouseClickFanAddon.__init__(self)


class FanRoundListWidget(MouseClickFanAddon, RoundListWidget):
    def __init__(self, parent=None):
        RoundListWidget.__init__(self, parent)
        MouseClickFanAddon.__init__(self)

