from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, ImageLabel, StrongBodyLabel, SimpleCardWidget, BodyLabel, \
    PushButton

from .tool_load import Tool, ModuleInstaller


class ToolInfoBox(MessageBoxBase):
    launchToolSignal = Signal()
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
        childVBoxLayout.addWidget(BodyLabel(self.tr("Needed modules:") + (" ".join(tool.modules) if tool.modules else self.tr("None"))))

        if tool.modules:
            self.moduleInstaller = ModuleInstaller(self)
            pushButton_installModules = PushButton(self.tr("Install Modules"))
            pushButton_installModules.clicked.connect(lambda: self.moduleInstaller.install_modules(tool))
            childVBoxLayout.addWidget(pushButton_installModules)

        vBoxLayout.addWidget(simpleCard)
        hBoxLayout.addLayout(vBoxLayout)

        self.yesButton.setText(self.tr("Launch"))

        self.viewLayout.addLayout(hBoxLayout)

    def launch_text(self, mode: int) -> str:
        if mode == 0:
            return self.tr("This tool can be launched without FanTools Main Software.")
        elif mode == 1:
            return self.tr("This tool can only be launched with FanTools Main Software.")
        else:
            raise IndexError(f"Index {mode} out of range.")

    def validate(self) -> bool:
        """点击确认按钮后启动工具，此处不做验证。"""
        self.launchToolSignal.emit()
        return True



