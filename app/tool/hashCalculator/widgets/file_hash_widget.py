from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication
from qfluentwidgets import SimpleCardWidget, SubtitleLabel, StrongBodyLabel, ComboBox, PushButton, ToolButton, \
    FluentIcon, SplitPushButton, Action, RoundMenu, InfoBar, InfoBarPosition

from app.tool.hashCalculator.widgets.function import HashData
from app.tool.public.public_window import FanWindow


class FileHashWidget(SimpleCardWidget):
    def __init__(self, filePath: str, hashData: HashData, parent: FanWindow=None):
        super().__init__(parent=parent)
        self.hashData = hashData
        self._parent = parent
        self.cb = QApplication.clipboard()

        self.baseLayout = QHBoxLayout()
        self.setLayout(self.baseLayout)

        self.titleLabel = SubtitleLabel()
        self.titleLabel.setText(filePath)
        self.hashLabel = StrongBodyLabel()
        self.hashLabel.setText(self.hashData.sha1)
        self.toolButton = ToolButton()
        self.toolButton.setIcon(FluentIcon.COPY)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.hashLabel)
        bottomLayout.addWidget(self.toolButton)

        centerLayout = QVBoxLayout()
        centerLayout.addWidget(self.titleLabel)
        centerLayout.addLayout(bottomLayout)

        self.baseLayout.addLayout(centerLayout)

        buttonLayout = QVBoxLayout()
        self.moreButton = SplitPushButton()
        self.moreButton.setText(self.tr("More"))
        self.moreButton.setIcon(FluentIcon.MORE)
        menu = RoundMenu()
        menu.addAction(Action(icon=FluentIcon.DELETE, text=self.tr("Delete"),
                              triggered=self.deleteLater))
        self.moreButton.setFlyout(menu)
        self.combobox = ComboBox()
        self.combobox.addItems(["SHA1", "SHA256", "SHA384", "SHA512", "MD5"])
        self.combobox.setCurrentIndex(0)

        buttonLayout.addWidget(self.moreButton)
        buttonLayout.addWidget(self.combobox)
        self.baseLayout.addLayout(buttonLayout)

        self.__connect()
        self.__setStyle()

    def displayHash(self) -> None:
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

    def __connect(self) -> None:
        self.combobox.currentIndexChanged.connect(self.displayHash)
        self._parent.windowResizeSignal.connect(self.labelResize)
        self.toolButton.clicked.connect(lambda: self.writeToClipboard(self.combobox.currentText(), self.hashLabel.text()))
        return None

    def __setStyle(self) -> None:
        self.combobox.setFixedWidth(120)
        self.moreButton.setFixedWidth(120)
        self.moreButton.button.setFixedWidth(90)
        self.labelResize()
        return None

    def writeToClipboard(self, mode: str, hashText: str) -> None:
        self.cb.setText(hashText)
        InfoBar.success(parent=self._parent,
                        title=self.tr("Success"),
                        content=self.tr("Selected file's {} has been written to clipboard.").format(mode.upper()),
                        position=InfoBarPosition.BOTTOM,
                        duration=4000,
                        isClosable=True)
        return None

    def labelResize(self) -> None:
        """在窗口大小变化时动态控制文本标签最大长度来防止卡片超出窗口"""
        self.titleLabel.setMaximumWidth(self._parent.width()-200)
        self.hashLabel.setMaximumWidth(self._parent.width()-240)
        return None
