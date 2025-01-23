import sys

from loguru import logger

logger.remove(0)
logger.add(sys.stderr, level="DEBUG", colorize=True, format="{time} | {level} | {message}")
logger.add("AppData/latest.log", level="INFO", colorize=False, format="{time} | {level} | {message}", mode="w")

logger.success("日志模块初始化完毕。")