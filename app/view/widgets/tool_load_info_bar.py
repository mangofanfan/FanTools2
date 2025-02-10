from PySide6.QtCore import QObject
from qfluentwidgets import InfoBar

from ...common.logger import logger


class ModuleInstallInfoBar(QObject):
    def install_now(self, tool_name: str, parent):
        self.infoBar = InfoBar.info(title=self.tr("Installing module(s) needed by {}").format(tool_name),
                                    content=self.tr("This may cause a few seconds ..."),
                                    isClosable=False,
                                    duration=-1,
                                    parent=parent)
        logger.info(f"开始安装工具 {tool_name} 所需的模块...")
        self.infoBar.show()
        return None

    def install_success(self, parent):
        self.infoBar.close()
        InfoBar.success(title=self.tr("Installing module(s) Successfully!"),
                        content=self.tr("Wuhu Wuhu!"),
                        isClosable=True,
                        duration=4000,
                        parent=parent)
        logger.success("模块安装成功。")
        return None

    def install_failed(self, parent):
        self.infoBar.close()
        InfoBar.error(title=self.tr("Installing module(s) Failed!"),
                      content=self.tr("You may need to check latest-error.log to get more info."),
                      isClosable=True,
                      duration=4000,
                      parent=parent)
        logger.error("模块安装失败！")
        return None

class ToolLaunchInfoBar(QObject):
    def multi_launch_error(self, parent):
        InfoBar.error(title=self.tr("Failed to launch this tool multiply!"),
                      content=self.tr("This tool could not be launched multiply at one time."),
                      isClosable=True,
                      duration=4000,
                      parent=parent)
        logger.error("此工具不支持重复启动。")
