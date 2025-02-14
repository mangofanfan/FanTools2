import sys
import traceback

from PySide6.QtWidgets import QMessageBox

from app.common.logger import logger


def handle_exception(exc_type, exc_value, exc_traceback: traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # 捕获错误并打印堆栈信息
    try:
        QMessageBox.critical(None,
                             "An Unexpected Error Occurred! 意料外的异常！",
                             "An Unexpected Error has just occurred and was caught by FanTools.\n"
                                  "Although FanTools Main Software may still run as well, something bad may happen now.\n"
                                  "Check latest-error.log for more details.\n"
                                  "一个意料之外的异常刚刚发生，并且被芒果工具箱捕获。\n"
                                  "尽管工具箱主程序可能仍在运行，但在不为人知的角落，很可能会有不妙的事情发生……\n"
                                  "请检查 latest-error.log 以获取更详细的信息！", )
    except:
        pass
    logger.critical("工具箱本体事件循环出现意料外的异常，该异常已经被捕获。")
    logger.critical("如果您是在工具箱本体中，而不是任何工具中触发了异常，则问题出在工具箱本体；否则，问题有可能由您正在工作的工具所触发，需要进一步判断。")
    logger.critical("对于第一种可能性，这往往意味着工具箱的代码中存在问题，或者用户的行为越过了工具箱开发者的思维极限，也可能只是单纯的芒果比较傻所以没考虑到这种情况。")
    logger.critical("对于第二种可能性，请联系该工具的作者以反馈有关问题，灰常感谢！")
    logger.critical("下面将打印异常 Traceback，您可以将此情报反馈给芒果来处理，或者亲自研究一下工具箱的源码。")
    logger.critical(f"exc_type: {exc_type.__name__}")
    logger.critical(f"exc_value: {exc_value}")
    logger.critical(f"exc_traceback: ")
    for i in traceback.format_tb(exc_traceback):
        logger.critical("\n" + i)
    logger.critical("如您需要，工具箱的 GitHub 仓库：https://github.com/mangofanfan/FanTools2")
    logger.critical("理论上工具箱依然可以继续运行，但这并不意味着异常可以被忽视，请提起重视！")
    logger.trace("怎么会！又出错了！QAQ！！")

sys.excepthook = handle_exception

if __name__ == "__main__":
    import main
