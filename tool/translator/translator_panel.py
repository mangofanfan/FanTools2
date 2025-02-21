import os

from PySide6.QtCore import QFile, QIODevice

from .widgets.language_file import PoFileObject
from .translator_window import TranslatorMainWindow
from .designer.TranslatorPanel import Ui_Form as Ui_TranslatorPanel
from .widgets.project_widget import ProjectCardWidget
from ..public.function import getToolDir
from ..public.public_window import FanWindow


class TranslatorPanel(Ui_TranslatorPanel, FanWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.resize(900, 600)

        # 窗口进阶设计
        self.RoundListWidget.setCurrentRow(0)

        # 窗口魔改逻辑
        self.MainWindow = TranslatorMainWindow()
        self.PushButton_CreateExampleProject.clicked.connect(self._createExampleProject)

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
