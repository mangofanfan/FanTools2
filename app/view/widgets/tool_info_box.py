from PySide6.QtCore import QSize
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, ImageLabel, StrongBodyLabel

from .tool_widget import Tool


class ToolInfoBox(MessageBoxBase):
    def __init__(self, parent=None, tool: Tool = None):
        super().__init__(parent=parent)
        self.parent = parent

        hBoxLayout = QHBoxLayout()

        imageLabel = ImageLabel()
        imageLabel.setImage(QImage(tool.icon))
        imageLabel.setFixedSize(QSize(128, 128))
        hBoxLayout.addWidget(imageLabel)

        vBoxLayout = QVBoxLayout()

        titleLabel = TitleLabel()
        titleLabel.setText(self.tr("Tool Info:") + tool.name)
        vBoxLayout.addWidget(titleLabel)

        strongLabel = StrongBodyLabel()
        strongLabel.setText(self.tr("Tool Tip:") + tool.tip)
        vBoxLayout.addWidget(strongLabel)

        hBoxLayout.addLayout(vBoxLayout)

        self.viewLayout.addLayout(hBoxLayout)

    def validate(self) -> bool:
        return True



