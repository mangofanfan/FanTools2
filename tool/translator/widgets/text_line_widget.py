from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import BodyLabel

from ...public.public_card import ClickableCardWidget


class TextLineWidget(ClickableCardWidget):

    isChosenSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stayChosen = False

        self.setChosenEnabled(True)
        self.setClickToChoose(True)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._textLabel = BodyLabel()
        self._layout.addWidget(self._textLabel)

        self.clicked.connect(lambda: self.setChosen(True))

    def setText(self, text: str) -> None:
        self._textLabel.setText(text)
        return None

    def setChosen(self, isChosen: bool) -> None:
        if isChosen:
            super().setChosen(isChosen)
            self._stayChosen = True
            self.isChosenSignal.emit()
        else:
            if self._stayChosen:
                self._stayChosen = False
            else:
                super().setChosen(isChosen)
        return None
