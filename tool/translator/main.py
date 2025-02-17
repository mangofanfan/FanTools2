import os

from PySide6.QtCore import QFile, QIODevice

from app.common import resource

from .widgets.text_line_widget import TextLineWidget
from .widgets.window import TranslatorMainWindow
from .widgets.text_object import TextObject
from .widgets.language_file import PoFileObject
from ..public.function import getToolDir


class Main:
    def __init__(self):
        self.MainWindow = TranslatorMainWindow()

    def showMainWindow(self):
        self.MainWindow.centerWindow()
        self.MainWindow.show()

    def generateTestData(self):
        """ 生成测试项目 """
        testFile = QFile(":/app/texts/langText_en_ES.po")
        testFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        os.makedirs(f"{getToolDir('translator')}projects/langText", exist_ok=True)
        with open(file=f"{getToolDir('translator')}projects/langText/langText_en_ES.po", mode="w+", encoding="utf-8") as f:
            f.write(testFile.readAll().toStdString())
        testFile.close()

        poFile = PoFileObject(f"{getToolDir('translator')}projects/langText/langText_en_ES.po")
        textObjectList = poFile.getTextList()
        for textObject in textObjectList:
            tlw = TextLineWidget()
            tlw.setTextObject(textObject)
            self.MainWindow.addTextLineWidget(tlw)

        self.MainWindow.addTextLineWidgetFinished()

