import os

from PySide6.QtCore import QFile, QIODevice

from app.common import resource

from .widgets.text_line_widget import TextLineWidget
from .widgets.window import TranslatorMainWindow
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
        t1 = TextLineWidget()
        t2 = TextLineWidget()
        t1.setText("abaaba")
        t2.setText("cdccdc")
        self.MainWindow.addTextLineWidget(t1)
        self.MainWindow.addTextLineWidget(t2)
        self.MainWindow.addTextLineWidgetFinished()


