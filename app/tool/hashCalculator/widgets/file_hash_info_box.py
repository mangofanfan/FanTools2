from PySide6.QtWidgets import QHBoxLayout, QApplication
from qfluentwidgets import MessageBoxBase, TitleLabel, SubtitleLabel, LineEdit, ToolButton, FluentIcon, StrongBodyLabel, \
    InfoBar, InfoBarPosition

from .function import HashData


class FileHashInfoBox(MessageBoxBase):
    def __init__(self, fileName: str, hashData: HashData, parent=None):
        self._parent = parent
        self.hashData = hashData
        super().__init__(parent=parent)
        self.cb = QApplication.clipboard()

        titleLabel = SubtitleLabel()
        titleLabel.setText(self.tr("Full Hash Info of file:"))
        fileNameLabel = TitleLabel()
        fileNameLabel.setText(fileName)
        self.viewLayout.addWidget(titleLabel)
        self.viewLayout.addWidget(fileNameLabel)

        for mode in ["sha1", "sha256", "sha384", "sha512", "md5"]:
            self._displayHashInfo(mode)

    def _displayHashInfo(self, mode: str) -> None:
        label = StrongBodyLabel()
        label.setText(mode.upper())
        lineEdit = LineEdit()
        lineEdit.setReadOnly(True)
        lineEdit.setText((hashText := self.hashData.get(mode)))
        toolButton = ToolButton()
        toolButton.setIcon(FluentIcon.COPY)
        toolButton.clicked.connect(lambda: self.writeToClipboard(mode, hashText))

        hLayout = QHBoxLayout()
        hLayout.addWidget(label)
        hLayout.addWidget(lineEdit)
        hLayout.addWidget(toolButton)
        self.viewLayout.addLayout(hLayout)
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

