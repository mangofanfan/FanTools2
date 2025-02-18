from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import Action, InfoLevel
from qfluentwidgets import FluentIcon as FIC

from app.common import resource
from app.common.logger import logger

from .language_file import PoFileObject
from .text_line_widget import TextLineWidget
from .text_object import TextObject
from ..designer.TranslatorMainWindow import Ui_Form as Ui_TranslatorMainWindow
from ...public.public_window import FanWindow


class TranslatorMainWindow(Ui_TranslatorMainWindow, FanWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 窗口进阶设计
        self.resize(QSize(1000, 800))
        self.setWindowTitle("Translator")
        self.setWindowIcon(QIcon(":app/images/icons/IconTranslate.png"))

        self.ProgressRing.setRange(0, 100)
        self.ProgressRing.setTextVisible(True)

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
                   triggered=self._saveTranslatedText),
            Action(FIC.RETURN, self.tr("Return"),
                   triggered=self._returnTranslatedText),
        ])
        self.CommandBar.addSeparator()
        self.CommandBar.addActions([
            Action(FIC.COPY, self.tr("Copy"),
                   triggered=self._copyTranslatedText),
            Action(FIC.DELETE, self.tr("Clear"),
                   triggered=self._clearTranslatedText),
        ])
        self.CommandBar.addSeparator()
        self.CommandBar.addHiddenActions([
            Action(FIC.QUESTION, self.tr("Mark Fuzzy"),
                   triggered=print("Fuzzy"))
        ])

        # 魔改窗口逻辑
        self._textLineList: list[TextLineWidget] = []
        self._onChosenTextObject: TextObject = None
        self._isTranslatedTextEdited = False
        self._poFileObject: PoFileObject = None

        # 信息区组件设置
        self._tr_poFileFrom = self.tr(".po File From:")
        self._tr_textTotal = self.tr("Text Total:")
        self._tr_translatedTotal = self.tr("Translated Total:")
        self._tr_leftTotal = self.tr("Left Total:")

        # 工作区组件设置
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)
        self.LineEdit_Text_Original.setReadOnly(True)
        self.LineEdit_Text_Translated.textChanged.connect(self._onTranslatedTextEdited)

        logger.trace("翻译工具主窗口初始化完毕。")

    def setPoFileObject(self, poFileObject: PoFileObject):
        self. _poFileObject = poFileObject
        # 信息区显示文件信息
        self.TitleLabel_PoFileName.setText(poFileObject.getPoFilePath())
        self.SubtitleLabel_FromFileName.setText(self._tr_poFileFrom)
        self.BodyLabel_TextTotal.setText(self._tr_textTotal + str(num_total := poFileObject.getTextTotal()))
        self.BodyLabel_TranslatedTextTotal.setText(self._tr_translatedTotal + str(num_translated := poFileObject.getTranslatedTextTotal()))
        self.BodyLabel_LeftTextTotal.setText(self._tr_leftTotal + str(num_total-num_translated))
        self.ProgressRing.setValue(num_translated/num_total*100)
        logger.trace("为翻译工具主窗口设置了 PoFileObject")
        return None

    def addTextLineWidget(self, textLine: TextLineWidget) -> None:
        self._scrollLayout.addWidget(textLine)
        self._textLineList.append(textLine)
        textLine.isChosenSignal.connect(self.onTextLineChosen)
        logger.trace("在翻译工具主窗口中添加一个 TextLineWidget")
        return None

    def removeTextLineWidget(self, textLine: TextLineWidget) -> None:
        ...

    def addTextLineWidgetFinished(self) -> None:
        self._scrollLayout.addStretch()
        self._textLineList[0].setChosen(True)
        logger.trace("在翻译工具主窗口中的 TextLineWidget 全部添加完毕。")
        return None

    def onTextLineChosen(self, textObject: TextObject) -> None:
        # 取消其他所有卡片的选中状态
        for tl in self._textLineList:
            tl: TextLineWidget
            tl.setChosen(False)

        # 防止重复执行（以上代码需要执行两次，以下代码不需要重复执行）
        if textObject == self._onChosenTextObject:
            return

        # 工作区更新为选中的词条数据
        self.LineEdit_Text_Original.setText(textObject.getOriginalText())
        self.LineEdit_Text_Translated.setText(textObject.getTranslatedText())
        self._onChosenTextObject = textObject
        self._onTranslatedTextChangAccepted()
        logger.info(f"在翻译工具主窗口中选中了词条 {textObject} 所在卡片。")
        return None

    def _saveTranslatedText(self):
        """ 与 save 按钮绑定，用来将 LineEdit 中编辑过的翻译文本保存"""
        self._onChosenTextObject.setTranslatedText(self.LineEdit_Text_Translated.text())
        self._onTranslatedTextChangAccepted()
        logger.info(f"在翻译工具主窗口中保存了当前修改的词条 {self._onChosenTextObject}")

    def _returnTranslatedText(self):
        """ 与 return 按钮绑定，用来回退 LineEdit 中的翻译文本到原始状态 """
        self.LineEdit_Text_Translated.setText(self._onChosenTextObject.getTranslatedText())
        # 由于已经在翻译文本变动的绑定方法中检测文本是否一致，因而这里不用手动调用 self._onTranslatedTextChangAccepted()
        logger.info(f"在翻译工具主窗口中回退了当前修改的词条 {self._onChosenTextObject}")

    def _copyTranslatedText(self):
        """ 与 copy 按钮绑定，用来回退 LineEdit 中的翻译文本到原始状态 """
        self.LineEdit_Text_Translated.setText(self.LineEdit_Text_Original.text())
        # 由于已经在翻译文本变动的绑定方法中检测文本是否一致，因而这里不用手动调用 self._onTranslatedTextChangAccepted()
        logger.info(f"在翻译工具主窗口中复制了当前词条 {self._onChosenTextObject} 的待翻译原文。")

    def _clearTranslatedText(self):
        """ 与 clear 按钮绑定，用来回退 LineEdit 中的翻译文本到原始状态 """
        self.LineEdit_Text_Translated.clear()
        # 由于已经在翻译文本变动的绑定方法中检测文本是否一致，因而这里不用手动调用 self._onTranslatedTextChangAccepted()
        logger.info(f"在翻译工具主窗口中清空了当前词条 {self._onChosenTextObject} 的翻译。")

    def _onTranslatedTextEdited(self):
        if self._isTranslatedTextEdited:
            # 如果翻译文本已经变化，检查是否与原翻译文本一致。
            if self.LineEdit_Text_Translated.text() == self._onChosenTextObject.getTranslatedText():
                self._onTranslatedTextChangAccepted()
                logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 在编辑后回到原状态，取消翻译编辑标记。")
            return None
        self._isTranslatedTextEdited = True
        self.Tag_TranslatedTextAccepted.setHidden(True)
        self.Tag_TranslatedTextEdited.setHidden(False)
        logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 被编辑，已将其标记。")

    def _onTranslatedTextChangAccepted(self):
        if not self._isTranslatedTextEdited:
            return None
        self._isTranslatedTextEdited = False
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)
        logger.trace(f"在翻译工具主窗口中，词条 {self._onChosenTextObject} 的编辑已被接受。")

    def closeEvent(self, event: QCloseEvent) -> None:
        self._poFileObject.save()
        logger.success("翻译工具主窗口关闭前，项目已经保存。")
        super().closeEvent(event)

