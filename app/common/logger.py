import sys

from loguru import logger

logger.remove(0)
logger.add(sys.stderr, level="DEBUG", colorize=True, format="{time} | {level} | {message}")

logger.success("日志模块初始化完毕。")