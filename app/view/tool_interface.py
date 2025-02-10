import importlib
import subprocess
from dataclasses import dataclass
from functools import partial
from typing import Union

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SmoothScrollArea, TitleLabel, FlowLayout, LargeTitleLabel

from app.view.widgets.tool_info_box import ToolInfoBox
from app.view.widgets.tool_load import load_all_tools
from app.view.widgets.tool_widget import ToolWidget, Tool
from app.common import resource
from common.function import basicFunc
from view.widgets.tool_load import ToolMultiLaunchError


class ToolInterface(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName("scrollAreaWidgetContents")
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.setObjectName('ToolInterface')
        self.scrollWidget.setLayout(self.scrollLayout)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.titleLabel = LargeTitleLabel(self.scrollWidget)
        self.titleLabel.setText(self.tr("Tools"))
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollLayout.addWidget(self.titleLabel)

        self.toolInfoList = []
        self.launchedToolInfoDict = {}
        self.pythonRuntimePath = basicFunc.getHerePath()+"/runtime/python.exe"
        self.__initToolInfo()

        self.__initToolList()

        self.scrollLayout.addStretch()

    def __initToolInfo(self) -> None:
        n = 0
        try:
            tools = load_all_tools()
            while True:
                self.toolInfoList.append(next(tools))
                n += 1
        except StopIteration:
            pass
        return None

    def __initToolList(self) -> None:
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
            widget = ToolWidget(tool=tool)
            widget.launchButton.clicked.connect(partial(self.launchTool, tool.name))
            widget.clicked.connect(partial(self.showInfoBox, tool))
            self.flowLayout.addWidget(widget)
        return None

    def launchTool(self, toolName: str) -> None:
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

        # 分启动模式来启动工具
        if tool.launchMode == 0:  # 直接 import 来启动
            if tool.module not in self.launchedToolInfoDict.keys():
                self.launchedToolInfoDict[tool.module] = importlib.import_module(f"tool.{tool.module}.run")
            else:
                self.launchedToolInfoDict[tool.module] = importlib.reload(self.launchedToolInfoDict[tool.module])
        elif tool.launchMode == 1:
            if tool.module not in self.launchedToolInfoDict.keys():
                process = QProcess()
                process.finished.connect(lambda: self.launchedToolInfoDict.pop(tool.module, None))
                process.start(self.pythonRuntimePath, [f"{basicFunc.getHerePath()}/tool/{tool.module}/run.py"])
                self.launchedToolInfoDict[tool.module] = process
            else:
                raise ToolMultiLaunchError(f"toolName={toolName} already launched")
        return None

    def showInfoBox(self, tool: Tool) -> None:
        infoBox = ToolInfoBox(tool=tool, parent=self._parent)
        infoBox.launchToolSignal.connect(lambda: self.launchTool(tool.name))
        infoBox.show()
        return None
