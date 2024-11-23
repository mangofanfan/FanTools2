import importlib
from dataclasses import dataclass
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SmoothScrollArea, TitleLabel, FlowLayout, LargeTitleLabel

from app.view.widgets.tool_widget import ToolWidget
from app.common import resource


@dataclass
class Tool:
    name: str
    module: str
    icon: Union[QIcon, str]
    toolTip: str


class ToolInterface(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName("scrollAreaWidgetContents")
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.setObjectName('ToolInterface')
        self.scrollWidget.setLayout(self.scrollLayout)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.titleLabel = LargeTitleLabel(self.scrollWidget)
        self.titleLabel.setText(self.tr("Tools"))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.scrollLayout.addWidget(self.titleLabel)

        self.toolInfoList = []
        self.launchedToolInfoDict = {}
        self.__initToolInfo()

        self.__initToolList()

        self.scrollLayout.addStretch()

    def __initToolInfo(self):
        self.toolInfoList.append(Tool(name=self.tr("Hash Calculator"),
                                      module="hashCalculator",
                                      icon=QIcon(":/app/images/icons/IconHash.png"),
                                      toolTip=self.tr("Calculate Hash of anything.")))
        return None

    def __initToolList(self):
        """
        全部工具列表，显示在页面底部。
        :return: None
        """
        titleLabel = TitleLabel()
        titleLabel.setText(self.tr("All Tools"))
        self.scrollLayout.addWidget(titleLabel)

        self.flowLayout = FlowLayout()
        self.scrollLayout.addLayout(self.flowLayout)

        # 加载工具
        for tool in self.toolInfoList:
            widget = ToolWidget(toolName=tool.name, toolIcon=tool.icon, toolTip=tool.toolTip)
            widget.launchButton.clicked.connect(lambda: self.launchTool(tool.name))
            self.flowLayout.addWidget(widget)
        return None

    def launchTool(self, toolName: str):
        """
        通过 importlib 模块动态导入并使用工具。
        :param toolName: str，工具名称。
        :return: None
        """
        tool: Tool = None
        for t in self.toolInfoList:
            if t.name == toolName:
                tool = t
                break
        if tool is None:
            raise Exception(f"toolName={toolName} not found")

        if tool.module not in self.launchedToolInfoDict.keys():
            self.launchedToolInfoDict[tool.module] = importlib.import_module(f"app.tool.{tool.module}.run")
        else:
            self.launchedToolInfoDict[tool.module] = importlib.reload(self.launchedToolInfoDict[tool.module])
        return None
