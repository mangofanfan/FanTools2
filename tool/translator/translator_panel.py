import os

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout

from .widgets.config import translator_config
from .widgets.icon import TranslatorIcon
from .widgets.language_file import PoFileObject
from .translator_window import TranslatorMainWindow
from .designer.TranslatorPanel import Ui_Form as Ui_TranslatorPanel
from .widgets.project_widget import ProjectCardWidget
from .widgets.setting_card_widget import APISettingCard
from ..public.function import getToolDir
from ..public.public_window import FanWindow


class TranslatorPanel(Ui_TranslatorPanel, FanWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.resize(900, 600)
        self.StackedWidget.setCurrentIndex(0)
        self.RoundListWidget.setCurrentRow(0)
        self.setWindowIcon(QIcon(":/app/images/icons/IconTranslate.png"))

        # 窗口进阶设计
        self._settingsLayout = QVBoxLayout()
        self._settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.ScrollArea_2.setLayout(self._settingsLayout)
        self.addAPISettingCards()

        # 窗口魔改逻辑
        self.MainWindow = TranslatorMainWindow()
        self.PushButton_CreateExampleProject.clicked.connect(self._createExampleProject)

    def addAPISettingCards(self):
        self._settingsLayout.addWidget(APISettingCard(icon=TranslatorIcon.BaiDu.path(),
                                                      title=self.tr("百度通用文本翻译API"),
                                                      content=self.tr("Provide free usage per month. See: https://fanyi-api.baidu.com/"),
                                                      parent=self,
                                                      arg1name="APPID",
                                                      arg2name="Key",
                                                      configItem1=translator_config.BaiDuAPPID,
                                                      configItem2=translator_config.BaiDuKey))
        self._settingsLayout.addWidget(APISettingCard(icon=TranslatorIcon.YouDao.path(),
                                                      title=self.tr("有道文本翻译API"),
                                                      content=self.tr("Provide free usage once you register. See: https://ai.youdao.com/product-fanyi-text.s"),
                                                      parent=self,
                                                      arg1name="APPKey",
                                                      arg2name="Key",
                                                      configItem1=translator_config.YouDaoAPPKey,
                                                      configItem2=translator_config.YouDaoKey))
        self._settingsLayout.addStretch()

    def addProjectCard(self, poFileObject: PoFileObject):
        card = ProjectCardWidget(self, poFileObject)
        card.openProjectSignal.connect(self.openProject)
        self.ScrollLayout.insertWidget(0, card)
        return None

    def openProject(self, poFileObject: PoFileObject):
        window = TranslatorMainWindow()
        window.setPoFileObject(poFileObject)
        window.centerWindow()
        window.show()
        self.close()
        return None

    def _createExampleProject(self, allowReplace: bool=False):
        """
        生成测试项目
        :param allowReplace: 如果测试项目已经存在，是否允许覆盖
        """
        try:
            os.makedirs(f"{getToolDir('translator')}projects/langText", exist_ok=allowReplace)

        except FileExistsError:
            # 如果目录存在则说明项目存在。
            # 如果 allowReplace 为 True，则目录存在不会引发报错，测试项目将被覆盖。
            # 如果 allowReplace 为 False，当目录存在时触发报错，else 中的代码不会执行，即不会覆盖，转而直接读取已存在的测试项目。
            ...

        else:
            testFile = QFile(":/app/texts/langText_en_ES.po")
            testFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
            with open(file=f"{getToolDir('translator')}projects/langText/langText_en_ES.po", mode="w+", encoding="utf-8") as f:
                f.write(testFile.readAll().toStdString())
            testFile.close()

        finally:
            poFile = PoFileObject(f"{getToolDir('translator')}projects/langText/langText_en_ES.po")
            self.addProjectCard(poFile)
            return
