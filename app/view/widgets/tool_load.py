import json
import os
from PySide6.QtCore import QProcess
from dataclasses import dataclass
from typing import Generator

from ...common.function import basicFunc
from ...common.logger import logger
from .tool_load_info_bar import ModuleInstallInfoBar


@dataclass
class Tool:
    name: str
    module: str
    icon: str
    tip: str
    ver: str
    author: str
    launchMode: int
    modules: list[str]


tools_dir = basicFunc.getHerePath() + "/tool"


def pre_load_tool(tool: Tool) -> Tool:
    # 替换工具路径
    icon_path = tool.icon.replace("%ToolLocal%", f"{tools_dir}/{tool.module}")
    tool.icon = icon_path

    # 检查启动模式
    if tool.launchMode == 0:
        tool.modules = []
    return tool


def load_all_tools() -> Generator[Tool, None, None]:
    with os.scandir(tools_dir) as entries:
        for o in entries:
            if o.is_dir():
                try:
                    data: dict = json.loads(basicFunc.readFile(f"{tools_dir}/{o.name}/tool.json", realPath=True), )
                except FileNotFoundError:
                    continue
                else:
                    yield pre_load_tool(Tool(name=data["name"], module=data["module"],
                                             icon=data["icon"], tip=data["tip"],
                                             ver=data["ver"], author=data["author"],
                                             launchMode=data["launchMode"],
                                             modules=data["modules"]))


class ModuleInstaller:
    def __init__(self, parent):
        self.process = QProcess()
        self.process.started.connect(self.processStarted)
        self.process.finished.connect(self.processFinished)
        self.process.readyRead.connect(self.processPrint)

        self.infoBar = ModuleInstallInfoBar()
        self.parent = parent

    def install_modules(self, tool: Tool) -> None:
        python_path = basicFunc.getHerePath() + "/runtime/python.exe"
        self.infoBar.install_now(tool.name, self.parent)
        self.process.start(python_path, ["-m", "pip", "install"] + tool.modules)
        return None

    def processStarted(self):
        logger.debug(f"ToolInstaller 子进程开始，启动命令为 {self.process.arguments()}")
        return None

    def processPrint(self):
        logger.debug(f"ToolInstaller 子进程输出：{self.process.readAll()}")
        return None

    def processFinished(self):
        logger.debug(f"ToolInstaller 子进程结束，返回 {(code:=self.process.exitCode())} | {self.process.exitStatus()}")
        if code == 0:
            self.infoBar.install_success(self.parent)
        else:
            self.infoBar.install_failed(self.parent)
        return None


class ToolMultiLaunchError(Exception):
    pass

