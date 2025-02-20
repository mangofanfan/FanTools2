from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QCloseEvent, Qt
from PySide6.QtWidgets import QVBoxLayout, QListWidgetItem
from qfluentwidgets import Action, InfoLevel, RoundMenu
from qfluentwidgets import FluentIcon as FIC

from app.common import resource
from app.common.logger import logger

from .config import translator_config
from .icon import TranslatorIcon
from .language_file import PoFileObject
from .text_line_widget import TextLineWidget
from .text_object import TextObject
from .translate_core import TranslateCore
from .translateapi import Language, API
from ..designer.TranslatorMainWindow import Ui_Form as Ui_TranslatorMainWindow
from ...public.public_window import FanWindow


class TranslatorMainWindow(Ui_TranslatorMainWindow, FanWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 窗口进阶设计
        self.resize(QSize(1000, 800))
        self.setWindowTitle(self.tr("Translator"))
        self.setWindowIcon(QIcon(":app/images/icons/IconTranslate.png"))

        self.ProgressRing.setRange(0, 100)
        self.ProgressRing.setTextVisible(True)

        self._scrollLayout = QVBoxLayout()
        self._scrollLayout.setContentsMargins(0, 5, 12, 0)
        self.scrollAreaWidgetContents.setLayout(self._scrollLayout)
        self.ScrollArea.setWidgetResizable(True)

        self.PushButton_TestAPIStatus.setText(self.tr("Test API status"))

        self.Tag_TranslatedTextAccepted.setLevel(InfoLevel.SUCCESS)
        self.Tag_TranslatedTextAccepted.setText(self.tr("Translated Text Accepted."))
        self.Tag_TranslatedTextEdited.setLevel(InfoLevel.WARNING)
        self.Tag_TranslatedTextEdited.setText(self.tr("Translated Text has been Edited!"))
        self.Tag_CommentAccepted.setLevel(InfoLevel.SUCCESS)
        self.Tag_CommentAccepted.setText(self.tr("Comment Accepted."))
        self.Tag_CommentEdited.setLevel(InfoLevel.WARNING)
        self.Tag_CommentEdited.setText(self.tr("Comment has been Edited!"))
        self.Tag_Fuzzy.setLevel(InfoLevel.INFOAMTION)
        self.Tag_Fuzzy.setText(self.tr("Fuzzy."))

        self.PushButton_StartThink.setText(self.tr("Start Thinking"))
        self.ToggleButton_LocalThinking.setText(self.tr("Local Thinking"))
        self.ToggleButton_APIThinking.setText(self.tr("API Thinking"))

        self.BodyLabel_OriginalText.setText(self.tr("Original Text"))
        self.BodyLabel_TranslatedText.setText(self.tr("Translated Text"))
        self.BodyLabel_Comment.setText(self.tr("Comment"))
        self.BodyLabel_TranslateSuggestions.setText(self.tr("Translated Suggestions"))

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
                   triggered=self._markFuzzy),
        ])

        self.SuggestionsPopMenu = RoundMenu()
        self.SuggestionsPopMenu.addActions([
            Action(FIC.DELETE, self.tr("Clear suggestions"),
                   triggered=self._clearThinking)
        ])
        self.RoundListWidget_Text_Suggested.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.RoundListWidget_Text_Suggested.setRightClickMenu(self.SuggestionsPopMenu)

        # 魔改窗口逻辑
        self._textLineList: list[TextLineWidget] = []
        self._onChosenTextObject: TextObject = None
        self._isTranslatedTextEdited = False
        self._isCommentEdited = False
        self._poFileObject: PoFileObject = None
        self._translateCore = TranslateCore()

        # 信息区组件设置
        self._tr_poFileFrom = self.tr(".po File From:")
        self._tr_textTotal = self.tr("Text Total:")
        self._tr_translatedTotal = self.tr("Translated Total:")
        self._tr_leftTotal = self.tr("Left Total:")
        self._tr_fuzzyTotal = self.tr("Fuzzy Total:")

        # 控制区组件设置
        self.PushButton_TestAPIStatus.clicked.connect(self._translateCore.test)

        # 工作区组件设置
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)
        self.Tag_CommentAccepted.setHidden(False)
        self.Tag_CommentEdited.setHidden(True)
        self.Tag_Fuzzy.setHidden(True)
        self.LineEdit_Text_Original.setReadOnly(True)
        self.LineEdit_Text_Translated.textChanged.connect(self._onTranslatedTextEdited)
        self.LineEdit_Comment.textChanged.connect(self._onCommentEdited)
        self.PushButton_StartThink.clicked.connect(self.startThinking)

        logger.trace("翻译工具主窗口初始化完毕。")

    def setPoFileObject(self, poFileObject: PoFileObject):
        self. _poFileObject = poFileObject
        self._updateProjectDisplay()
        logger.trace("为翻译工具主窗口设置了 PoFileObject")
        return None

    def addTextLineWidget(self, textLine: TextLineWidget) -> None:
        self._scrollLayout.addWidget(textLine)
        self._textLineList.append(textLine)
        textLine.isChosenSignal.connect(self.onTextLineChosen)
        logger.trace(f"在翻译工具主窗口中添加 {textLine.textObject} 对应的 TextLineWidget")
        return None

    def addTextLineWidgetFinished(self) -> None:
        """ 在所有词条卡片添加完毕后调用 """
        self._scrollLayout.addStretch()
        self._textLineList[0].setChosen(True)
        self.onTextLineChosen(self._textLineList[0].textObject)
        logger.success("在翻译工具主窗口中的 TextLineWidget 全部添加完毕。")
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
        self.LineEdit_Comment.setText(textObject.getComment())
        self._onChosenTextObject = textObject
        self._onTranslatedTextChangedAccepted()
        self._onCommentChangedAccepted()
        if textObject.getFuzzy():
            self.Tag_Fuzzy.setHidden(False)
            logger.trace(f"已对词条 {textObject} 显示 Fuzzy 标签。")
        else:
            self.Tag_Fuzzy.setHidden(True)
            logger.trace(f"词条 {textObject} 没有 Fuzzy 标签。")
        self._clearThinking()
        logger.info(f"在翻译工具主窗口中选中了词条 {textObject} 所在卡片。")
        return None

    def startThinking(self) -> None:
        """ 主动开始思考，获取所有可用的翻译思考渠道的结果并添加到翻译建议中 """
        self._translateCore.translate(self._onChosenTextObject.getOriginalText(),
                                      Language.en,
                                      Language.zh_CHS,
                                      API.YouDao,
                                      self._addSuggestion)
        return None

    def _clearThinking(self) -> None:
        """ 清空思考结果，应当在选中其他词条卡片时自动调用 """
        self.RoundListWidget_Text_Suggested.clear()
        return None

    def _addSuggestion(self, targetText: str, api: API) -> None:
        """ 在翻译建议中添加建议 """
        item = QListWidgetItem()
        item.setText(targetText)
        item.setIcon(QIcon((getattr(TranslatorIcon, api.value)).path()))
        self.RoundListWidget_Text_Suggested.addItem(item)
        return None

    def _saveTranslatedText(self):
        """ 与 save 按钮绑定，用来将 LineEdit 中编辑过的翻译文本保存 """
        if self._onChosenTextObject.getFuzzy():
            self.Tag_Fuzzy.setHidden(True)
            self._onChosenTextObject.setFuzzy(False)
            logger.trace(f"已对词条 {self._onChosenTextObject} 隐藏 Fuzzy 标签。")
        if self._isTranslatedTextEdited:
            self._onChosenTextObject.setTranslatedText(self.LineEdit_Text_Translated.text())
            self._onTranslatedTextChangedAccepted()
        if self._isCommentEdited:
            self._onChosenTextObject.setComment(self.LineEdit_Comment.text())
            self._onCommentChangedAccepted()
        self._updateProjectDisplay()
        logger.info(f"在翻译工具主窗口中保存了当前修改的词条 {self._onChosenTextObject}")

    def _returnTranslatedText(self):
        """ 与 return 按钮绑定，用来回退 LineEdit 中的翻译文本到原始状态 """
        self.LineEdit_Text_Translated.setText(self._onChosenTextObject.getTranslatedText())
        # 由于已经在翻译文本变动的绑定方法中检测文本是否一致，因而这里不用手动调用 self._onTranslatedTextChangAccepted()
        # 顺手返回注释
        self.LineEdit_Comment.setText(self._onChosenTextObject.getComment())
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
        # 顺手清掉注释
        self.LineEdit_Comment.clear()
        logger.info(f"在翻译工具主窗口中清空了当前词条 {self._onChosenTextObject} 的翻译与注释。")

    def _markFuzzy(self):
        """ 与 fuzzy 按钮绑定，用来将词条标注为 Fuzzy """
        self.Tag_Fuzzy.setHidden(False)
        self._onChosenTextObject.setFuzzy(True)
        self._updateProjectDisplay()
        logger.info(f"在翻译工具主窗口中将当前词条 {self._onChosenTextObject} 标注为 Fuzzy。")

    def _onTranslatedTextEdited(self):
        if self._isTranslatedTextEdited:
            # 如果翻译文本已经变化，检查是否与原翻译文本一致。
            if self.LineEdit_Text_Translated.text() == self._onChosenTextObject.getTranslatedText():
                self._onTranslatedTextChangedAccepted()
                logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 在编辑后回到原状态，取消翻译编辑标记。")
            return None
        self._isTranslatedTextEdited = True
        self.Tag_TranslatedTextAccepted.setHidden(True)
        self.Tag_TranslatedTextEdited.setHidden(False)
        self._updateProjectDisplay()
        logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 被编辑，已将其标记。")

    def _onTranslatedTextChangedAccepted(self):
        if not self._isTranslatedTextEdited:
            return None
        self._isTranslatedTextEdited = False
        self.Tag_TranslatedTextAccepted.setHidden(False)
        self.Tag_TranslatedTextEdited.setHidden(True)
        self._updateProjectDisplay()
        logger.trace(f"在翻译工具主窗口中，词条 {self._onChosenTextObject} 的编辑已被接受。")

    def _onCommentEdited(self):
        if self._isCommentEdited:
            # 如果注释已经变化，检查是否与原注释一致。
            if self.LineEdit_Comment.text() == self._onChosenTextObject.getComment():
                self._onCommentChangedAccepted()
                logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 的注释在编辑后回到原状态，取消翻译编辑标记。")
            return None
        self._isCommentEdited = True
        self.Tag_CommentAccepted.setHidden(True)
        self.Tag_CommentEdited.setHidden(False)
        logger.trace(f"在翻译工具主窗口中检测到词条 {self._onChosenTextObject} 的注释被编辑，已将其标记。")

    def _onCommentChangedAccepted(self):
        if not self._isCommentEdited:
            return None
        self._isCommentEdited = False
        self.Tag_CommentAccepted.setHidden(False)
        self.Tag_CommentEdited.setHidden(True)
        logger.trace(f"在翻译工具主窗口中，词条 {self._onChosenTextObject} 的注释的编辑已被接受。")

    def _updateProjectDisplay(self):
        """ 更新主窗口中的项目统计信息 """
        self.TitleLabel_PoFileName.setText(self._poFileObject.getPoFilePath())
        self.SubtitleLabel_FromFileName.setText(self._tr_poFileFrom)
        self.BodyLabel_TextTotal.setText(self._tr_textTotal + str(self._poFileObject.getTextTotal()))
        self.BodyLabel_TranslatedTextTotal.setText(self._tr_translatedTotal + str(self._poFileObject.getTranslatedTextTotal()))
        self.BodyLabel_LeftTextTotal.setText(self._tr_leftTotal + str(self._poFileObject.getUnTranslatedTextTotal()))
        self.BodyLabel_FuzzyTotal.setText(self._tr_fuzzyTotal + str(self._poFileObject.getFuzzyTextTotal()))
        self.ProgressRing.setValue(self._poFileObject.getPercentTranslatedTotal())
        logger.trace("在翻译工具主窗口中更新了统计信息面板。")
        return None

    def closeEvent(self, event: QCloseEvent) -> None:
        self._poFileObject.save()
        logger.success("翻译工具主窗口关闭前，项目已经保存。")
        super().closeEvent(event)

