from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout

from app.common import resource

from .text_line_widget import TextLineWidget
from ..designer.TranslatorMainWindow import Ui_Form as Ui_TranslatorMainWindow
from ...public.public_window import FanWindow


class TranslatorMainWindow(Ui_TranslatorMainWindow, FanWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.resize(QSize(800, 600))
        self.setWindowTitle("Translator")
        self.setWindowIcon(QIcon(":app/images/icons/IconTranslate.png"))

        self._scrollLayout = QVBoxLayout()
        self.scrollAreaWidgetContents.setLayout(self._scrollLayout)
        self.ScrollArea.setWidgetResizable(True)
        self._textLineList = set()

    def addTextLineWidget(self, textLine: TextLineWidget) -> None:
        self._scrollLayout.addWidget(textLine)
        self._textLineList.add(textLine)
        textLine.isChosenSignal.connect(self.onTextLineChosen)
        return None

    def removeTextLineWidget(self, textLine: TextLineWidget) -> None:
        ...

    def addTextLineWidgetFinished(self) -> None:
        self._scrollLayout.addStretch()
        return None

    def onTextLineChosen(self) -> None:
        for tl in self._textLineList:
            tl: TextLineWidget
            tl.setChosen(False)
        return None
