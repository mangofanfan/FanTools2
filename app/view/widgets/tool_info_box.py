from PySide6.QtCore import QSize
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, ImageLabel, StrongBodyLabel, SimpleCardWidget, BodyLabel

from .tool_load import Tool


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

        childVBoxLayout = QVBoxLayout()
        simpleCard = SimpleCardWidget()
        simpleCard.setLayout(childVBoxLayout)

        childVBoxLayout.addWidget(BodyLabel(self.tr("Author:") + tool.author))
        childVBoxLayout.addWidget(BodyLabel(self.tr("Version:") + tool.ver))
        childVBoxLayout.addWidget(BodyLabel(self.tr("Launch:") + self.launch_text(tool.launchMode)))

        vBoxLayout.addWidget(simpleCard)
        hBoxLayout.addLayout(vBoxLayout)

        self.viewLayout.addLayout(hBoxLayout)

    def launch_text(self, mode: int) -> str:
        if mode == 0:
            return self.tr("This tool can be launched without FanTools Main Software.")
        else:
            raise IndexError(f"Index {mode} out of range.")

    def validate(self) -> bool:
        return True



