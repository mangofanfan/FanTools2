from PySide6.QtCore import Qt, Signal, Property
from PySide6.QtGui import QPainter, QColor, QPainterPath
from PySide6.QtWidgets import QFrame
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.common.style_sheet import isDarkTheme


class ClickableCardWidget(BackgroundAnimationWidget, QFrame):
    """ 可点击选中的卡片组件 """

    clicked = Signal()

    def __init__(self, parent=None):
        self._isClickEnabled = False
        self._isChosenEnabled = False
        self._isChosen = False
        self._borderRadius = 5
        self._unChosenColor = (255, 255, 255)
        self._chosenColor = (0, 255, 255)

        super().__init__(parent=parent)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

    def setClickEnabled(self, isEnabled: bool):
        self._isClickEnabled = isEnabled
        self.update()

    def isClickEnabled(self):
        return self._isClickEnabled

    def setChosenEnabled(self, isEnabled: bool):
        self._isChosenEnabled = isEnabled
        self.update()

    def isChosenEnabled(self):
        return self._isChosenEnabled

    def setChosen(self, isChosen: bool):
        self._isChosen = isChosen
        self._updateBackgroundColor()
        self.update()

    def setClickToChoose(self, isClickToChoose: bool):
        if isClickToChoose:
            self.clicked.connect(lambda: self.setChosen(True))
        else:
            self.clicked.disconnect(lambda: self.setChosen(True))

    def _normalBackgroundColor(self):
        if self._isChosen:
            return QColor(*self._chosenColor, 13 if isDarkTheme() else 170)
        return QColor(*self._unChosenColor, 13 if isDarkTheme() else 170)

    def _hoverBackgroundColor(self):
        if self._isChosen:
            return QColor(*self._chosenColor, 21 if isDarkTheme() else 64)
        return QColor(*self._unChosenColor, 21 if isDarkTheme() else 64)

    def _pressedBackgroundColor(self):
        if self._isChosen:
            return QColor(*self._chosenColor, 8 if isDarkTheme() else 64)
        return QColor(*self._unChosenColor, 8 if isDarkTheme() else 64)

    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, radius: int):
        self._borderRadius = radius
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        r = self.borderRadius
        d = 2 * r

        isDark = isDarkTheme()

        # draw top border
        path = QPainterPath()
        # path.moveTo(1, h - r)
        path.arcMoveTo(1, h - d - 1, d, d, 240)
        path.arcTo(1, h - d - 1, d, d, 225, -60)
        path.lineTo(1, r)
        path.arcTo(1, 1, d, d, -180, -90)
        path.lineTo(w - r, 1)
        path.arcTo(w - d - 1, 1, d, d, 90, -90)
        path.lineTo(w - 1, h - r)
        path.arcTo(w - d - 1, h - d - 1, d, d, 0, -60)

        topBorderColor = QColor(0, 0, 0, 20)
        if isDark:
            if self.isPressed:
                topBorderColor = QColor(*self._chosenColor, 18)
            elif self.isHover:
                topBorderColor = QColor(*self._chosenColor, 13)
        else:
            topBorderColor = QColor(0, 0, 0, 15)

        painter.strokePath(path, topBorderColor)

        # draw bottom border
        path = QPainterPath()
        path.arcMoveTo(1, h - d - 1, d, d, 240)
        path.arcTo(1, h - d - 1, d, d, 240, 30)
        path.lineTo(w - r - 1, h - 1)
        path.arcTo(w - d - 1, h - d - 1, d, d, 270, 30)

        bottomBorderColor = topBorderColor
        if not isDark and self.isHover and not self.isPressed:
            bottomBorderColor = QColor(0, 0, 0, 27)

        painter.strokePath(path, bottomBorderColor)

        # draw background
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setBrush(self.backgroundColor)
        painter.drawRoundedRect(rect, r, r)

    borderRadius = Property(int, getBorderRadius, setBorderRadius)