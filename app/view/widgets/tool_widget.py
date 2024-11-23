from dataclasses import dataclass
from typing import Union

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import CardWidget, SubtitleLabel, PrimaryPushButton, ToolTipFilter, BodyLabel, IconWidget


@dataclass
class Tool:
    name: str
    module: str
    icon: str
    tip: str


class ToolWidget(CardWidget):
    def __init__(self, parent=None, tool: Tool = None):
        super().__init__(parent=parent)
        self.setFixedWidth(400)
        self.setFixedHeight(70)

        self.baseLayout = QHBoxLayout()
        self.setLayout(self.baseLayout)

        self.iconWidget = IconWidget(self)
        self.iconWidget.setIcon(tool.icon)
        self.iconWidget.setFixedSize(QSize(48, 48))
        self.baseLayout.addWidget(self.iconWidget)

        textLayout = QVBoxLayout()

        self.subtitleLabel = SubtitleLabel(self)
        self.subtitleLabel.setText(tool.name)
        textLayout.addWidget(self.subtitleLabel)

        self.descriptionLabel = BodyLabel(self)
        self.descriptionLabel.setText(tool.tip)
        textLayout.addWidget(self.descriptionLabel)

        self.baseLayout.addLayout(textLayout)

        self.launchButton = PrimaryPushButton()
        self.launchButton.setFixedWidth(80)
        self.launchButton.setText(self.tr("Launch"))
        self.launchButton.setToolTip(self.tr("Launch this tool"))
        self.launchButton.installEventFilter(ToolTipFilter(self.launchButton))
        self.baseLayout.addWidget(self.launchButton)
