from functools import partial

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import FluentIcon

from .designer.hash_calculator import Ui_Form as Window
from .widgets.file_hash_info_box import FileHashInfoBox
from .widgets.file_hash_widget import FileHashWidget
from .widgets.function import cal_file_hash, HashData
from ..public.public_window import FanWindow
from ...common import resource


class HashCalculatorWindow(FanWindow, Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(self.tr("Hash Calculator"))
        self.setWindowIcon(QIcon(":/app/images/icons/IconHash.png"))

        self.scrollLayout = QVBoxLayout()
        self.__initWindow()
        self.__initDropEvent()


    def __initWindow(self):
        self.IconWidget.setIcon(FluentIcon.INFO)
        self.BodyLabel.setText(self.tr("Drop any file here, and then you can check their hash, or compare them with someone else."))

        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)
        self.scrollLayout.addStretch()

        return None

    def __initDropEvent(self):
        self.DropMultiFilesWidget.fileDropped.connect(self.fileAccept)
        self.DropMultiFilesWidget.filesDropped.connect(self.filesAccept)
        return None

    def fileAccept(self, filePath: str):
        self.__addFileCard(filePath, cal_file_hash(filePath))
        return None

    def filesAccept(self, filePaths: list):
        for filePath in filePaths:
            self.fileAccept(filePath)
        return None

    def showFileHashInfoBox(self, filePath: str, hashData: HashData):
        infoBox = FileHashInfoBox(filePath, hashData, parent=self)
        infoBox.show()

    def __addFileCard(self, filePath: str, hashData: HashData):
        self.scrollLayout.addWidget((widget := FileHashWidget(filePath=filePath, hashData=hashData)))
        widget.moreButton.clicked.connect(partial(self.showFileHashInfoBox, filePath, hashData, ))
        return None


if __name__ == "app.tool.hashCalculator.run":
    window = HashCalculatorWindow()
    window.show()

