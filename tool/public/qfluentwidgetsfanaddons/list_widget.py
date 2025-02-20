from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QMenu
from qfluentwidgets import RoundMenu
from qfluentwidgetspro import RoundListWidget


class FanRoundListWidget(RoundListWidget):
    def __init__(self, parent=None):
        super(FanRoundListWidget, self).__init__(parent)

    def setRightClickMenu(self, menu: RoundMenu | QMenu) -> None:
        self.menu = menu
        return None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super(FanRoundListWidget, self).mousePressEvent(e)
        if not hasattr(self, "menu"): return
        if e.button() == Qt.MouseButton.RightButton and self.itemAt(e.pos()):
            self.menu.exec(e.globalPos())
