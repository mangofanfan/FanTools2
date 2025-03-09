# 翻译工具入口文件
from app.common.logger import logger

from .translator_panel import TranslatorPanel


if __name__ == "tool.translator.run":
    logger.info("启动翻译工具！翻译工具的日志也会输出在工具箱的主日志系统中哦！")

    w = TranslatorPanel()
    w.centerWindow()
    w.show()
