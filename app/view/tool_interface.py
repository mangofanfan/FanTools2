import importlib
import os
import subprocess
from dataclasses import dataclass
from functools import partial
from typing import Union

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SmoothScrollArea, TitleLabel, FlowLayout, LargeTitleLabel

from .widgets.tool_info_box import ToolInfoBox
from .widgets.tool_load import load_all_tools
from .widgets.tool_widget import ToolWidget, Tool
from .widgets.tool_load import ToolMultiLaunchError
from .widgets.tool_load_info_bar import ToolLaunchInfoBar
from ..common import resource
from ..common.function import basicFunc
from ..common.logger import logger


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

        self.infoBar = ToolLaunchInfoBar(self)

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
                process.setEnvironment([f"{basicFunc.getHerePath()}/tool/{tool.module}"] + list(os.environ))
                process.started.connect(lambda: self.processStarted(process, toolName))
                process.readyRead.connect(lambda: self.processPrint(process, toolName))
                process.finished.connect(lambda: self.processFinished(process, toolName))
                process.finished.connect(lambda: self.launchedToolInfoDict.pop(tool.module, None))
                process.start(self.pythonRuntimePath, [f"{basicFunc.getHerePath()}/tool/{tool.module}/run.py"])
                self.launchedToolInfoDict[tool.module] = process
            else:
                self.infoBar.multi_launch_error(self.window())
                logger.error(f"工具 {toolName} 无法多开。")
        return None

    def showInfoBox(self, tool: Tool) -> None:
        infoBox = ToolInfoBox(tool=tool, parent=self._parent)
        infoBox.launchToolSignal.connect(lambda: self.launchTool(tool.name))
        infoBox.show()
        return None

    @staticmethod
    def processStarted(process: QProcess, toolName: str) -> None:
        logger.debug(f"工具 {toolName} 子进程开始，启动参数为 {process.arguments()}")
        return None

    @staticmethod
    def processPrint(process: QProcess, toolName: str) -> None:
        logger.debug(f"工具 {toolName} 子进程输出：{process.readAll()}")
        return None

    @staticmethod
    def processFinished(process: QProcess, toolName: str) -> None:
        logger.debug(f"工具 {toolName} 子进程结束，返回 {(process.exitCode())} | {process.exitStatus()}")
        return None
