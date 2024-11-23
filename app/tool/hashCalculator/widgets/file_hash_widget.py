from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import SimpleCardWidget, SubtitleLabel, StrongBodyLabel, ComboBox, PushButton, ToolButton, FluentIcon

from app.tool.hashCalculator.widgets.function import HashData


class FileHashWidget(SimpleCardWidget):
    def __init__(self, filePath: str, hashData: HashData, parent=None):
        super().__init__(parent=parent)
        self.hashData = hashData

        self.baseLayout = QHBoxLayout()
        self.setLayout(self.baseLayout)

        titleLabel = SubtitleLabel()
        titleLabel.setText(filePath)
        self.hashLabel = StrongBodyLabel()
        self.hashLabel.setText(self.hashData.sha1)
        self.toolButton = ToolButton()
        self.toolButton.setIcon(FluentIcon.COPY)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.hashLabel)
        bottomLayout.addWidget(self.toolButton)

        centerLayout = QVBoxLayout()
        centerLayout.addWidget(titleLabel)
        centerLayout.addLayout(bottomLayout)

        self.baseLayout.addLayout(centerLayout)

        buttonLayout = QVBoxLayout()
        self.moreButton = PushButton()
        self.moreButton.setText(self.tr("More"))
        self.combobox = ComboBox()
        self.combobox.addItems(["SHA1", "SHA256", "SHA384", "SHA512", "MD5"])
        self.combobox.setCurrentIndex(0)

        buttonLayout.addWidget(self.moreButton)
        buttonLayout.addWidget(self.combobox)
        self.baseLayout.addLayout(buttonLayout)

        self.__connect()
        self.__setStyle()

    def displayHash(self):
        index = self.combobox.currentIndex()
        if index == 0:
            self.hashLabel.setText(self.hashData.sha1)
        elif index == 1:
            self.hashLabel.setText(self.hashData.sha256)
        elif index == 2:
            self.hashLabel.setText(self.hashData.sha384)
        elif index == 3:
            self.hashLabel.setText(self.hashData.sha512)
        elif index == 4:
            self.hashLabel.setText(self.hashData.md5)
        else:
            raise IndexError(f"index {index} out of range.")
        return None

    def __connect(self):
        self.combobox.currentIndexChanged.connect(self.displayHash)

    def __setStyle(self):
        self.combobox.setFixedWidth(120)
        self.moreButton.setFixedWidth(120)

