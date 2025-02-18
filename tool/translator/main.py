import os

from PySide6.QtCore import QFile, QIODevice

from app.common import resource
from app.common.logger import logger

logger.info("启动翻译工具！翻译工具的日志也会输出在工具箱的主日志系统中哦！")

from .widgets.text_line_widget import TextLineWidget
from .widgets.window import TranslatorMainWindow
from .widgets.language_file import PoFileObject
from ..public.function import getToolDir


class Main:
    def __init__(self):
        self.MainWindow = TranslatorMainWindow()

    def showMainWindow(self):
        self.MainWindow.centerWindow()
        self.MainWindow.show()

    def generateTestData(self, allowReplace: bool=False):
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
            textObjectList = poFile.getTextList()
            for textObject in textObjectList:
                tlw = TextLineWidget()
                tlw.setTextObject(textObject)
                self.MainWindow.addTextLineWidget(tlw)

            self.MainWindow.setPoFileObject(poFile)
            self.MainWindow.addTextLineWidgetFinished()
            return


