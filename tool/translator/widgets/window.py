from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import Action, InfoLevel
from qfluentwidgets import FluentIcon as FIC

from app.common import resource

from .text_line_widget import TextLineWidget
from .text_object import TextObject
from ..designer.TranslatorMainWindow import Ui_Form as Ui_TranslatorMainWindow
from ...public.public_window import FanWindow


class TranslatorMainWindow(Ui_TranslatorMainWindow, FanWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 窗口进阶设计
        self.resize(QSize(800, 600))
        self.setWindowTitle("Translator")
        self.setWindowIcon(QIcon(":app/images/icons/IconTranslate.png"))

        self._scrollLayout = QVBoxLayout()
        self._scrollLayout.setContentsMargins(0, 5, 10, 0)
        self.scrollAreaWidgetContents.setLayout(self._scrollLayout)
        self.ScrollArea.setWidgetResizable(True)

        self.Tag_TranslatedTextAccepted.setLevel(InfoLevel.SUCCESS)
        self.Tag_TranslatedTextAccepted.setText(self.tr("Translated Text Accepted."))
        self.Tag_TranslatedTextEdited.setLevel(InfoLevel.WARNING)
        self.Tag_TranslatedTextEdited.setText(self.tr("Translated Text has been Edited!"))

        self.CommandBar.addActions([
            Action(FIC.SAVE, self.tr("Save"),
                   triggered=self._onTranslatedTextChangAccepted),
            Action(FIC.RETURN, self.tr("Return"),
                   triggered=self._onTranslatedTextChangAccepted),
        ])

        self.CommandBar.addSeparator()

        self.CommandBar.addActions([
            Action(FIC.COPY, self.tr("Copy"),
                   triggered=lambda: self.LineEdit_Text_Translated.setText(self.LineEdit_Text_Original.text()))
        ])

        # 魔改窗口逻辑
        self._textLineList: list[TextLineWidget] = []
        self._onChosenTextObject: TextObject = None
        self._isTranslatedTextEdited = False

        # 工作区组建设置
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)
        self.LineEdit_Text_Original.setReadOnly(True)
        self.LineEdit_Text_Translated.textEdited.connect(self._onTranslatedTextEdited)

    def addTextLineWidget(self, textLine: TextLineWidget) -> None:
        self._scrollLayout.addWidget(textLine)
        self._textLineList.append(textLine)
        textLine.isChosenSignal.connect(self.onTextLineChosen)
        return None

    def removeTextLineWidget(self, textLine: TextLineWidget) -> None:
        ...

    def addTextLineWidgetFinished(self) -> None:
        self._scrollLayout.addStretch()
        self._textLineList[0].setChosen(True)
        return None

    def onTextLineChosen(self, textObject: TextObject) -> None:
        # 取消其他所有卡片的选中状态
        for tl in self._textLineList:
            tl: TextLineWidget
            tl.setChosen(False)

        # 工作区更新为选中的词条数据
        self.LineEdit_Text_Original.setText(textObject.getOriginalText())
        self.LineEdit_Text_Translated.setText(textObject.getTranslatedText())
        self._onChosenTextObject = textObject
        return None

    def _returnTranslatedText(self):
        self.LineEdit_Text_Translated.setText(self._onChosenTextObject.getTranslatedText())
        # 由于已经在翻译文本变动的绑定方法中检测文本是否一致，因而这里不用手动调用 self._onTranslatedTextChangAccepted()

    def _onTranslatedTextEdited(self):
        if self._isTranslatedTextEdited:
            # 如果翻译文本已经变化，检查是否与原翻译文本一致。
            if self.LineEdit_Text_Translated.text() == self._onChosenTextObject.getTranslatedText():
                self._onTranslatedTextChangAccepted()
            return None
        self._isTranslatedTextEdited = True
        self.Tag_TranslatedTextAccepted.setHidden(True)
        self.Tag_TranslatedTextEdited.setHidden(False)

    def _onTranslatedTextChangAccepted(self):
        if not self._isTranslatedTextEdited:
            return None
        self._isTranslatedTextEdited = False
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)

