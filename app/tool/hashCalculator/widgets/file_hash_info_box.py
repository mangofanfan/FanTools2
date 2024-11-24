from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, SubtitleLabel, LineEdit, ToolButton, FluentIcon, StrongBodyLabel

from .function import HashData


class FileHashInfoBox(MessageBoxBase):
    def __init__(self, fileName: str, hashData: HashData, parent=None):
        self._parent = parent
        self.hashData = hashData
        super().__init__(parent=parent)

        titleLabel = SubtitleLabel()
        titleLabel.setText(self.tr("Full Hash Info of file:"))
        fileNameLabel = TitleLabel()
        fileNameLabel.setText(fileName)
        self.viewLayout.addWidget(titleLabel)
        self.viewLayout.addWidget(fileNameLabel)

        for mode in ["sha1", "sha256", "sha384", "sha512", "md5"]:
            self._displayHashInfo(mode)

    def _displayHashInfo(self, mode) -> None:
        label = StrongBodyLabel()
        label.setText(mode.upper())
        lineEdit = LineEdit()
        lineEdit.setReadOnly(True)
        lineEdit.setText(self.hashData.get(mode))
        toolButton = ToolButton()
        toolButton.setIcon(FluentIcon.COPY)
        # toolButton.clicked.connect(lineEdit.text)

        hLayout = QHBoxLayout()
        hLayout.addWidget(label)
        hLayout.addWidget(lineEdit)
        hLayout.addWidget(toolButton)
        self.viewLayout.addLayout(hLayout)
        return None

