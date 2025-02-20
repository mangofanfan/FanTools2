from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import BodyLabel

from .text_object import TextObject
from ...public.qfluentwidgetsfanaddons import ClickableCardWidget


class TextLineWidget(ClickableCardWidget):

    isChosenSignal = Signal(TextObject)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stayChosen = False

        self.setChosenEnabled(True)
        self.setClickToChoose(True)

        self._textObject: TextObject = None

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._textLabel = BodyLabel()
        self._textLabel.setText("")
        self._layout.addWidget(self._textLabel)

        self.clicked.connect(lambda: self.setChosen(True))

    def setText(self, text: str) -> None:
        self._textLabel.setText(text)
        return None

    def setTextObject(self, textObject: TextObject) -> None:
        self._textObject = textObject
        self._textLabel.setText(f"[{self._textObject.id}] {self._textLabel.text()}")

    def setChosen(self, isChosen: bool) -> None:
        if isChosen:
            super().setChosen(isChosen)
            self._stayChosen = True
            self.isChosenSignal.emit(self._textObject)
        else:
            if self._stayChosen:
                self._stayChosen = False
            else:
                super().setChosen(isChosen)
        return None

    @property
    def textObject(self):
        return self._textObject
