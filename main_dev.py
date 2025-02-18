# coding:utf-8
import traceback
import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.common.logger import logger
from app.common import resource
from app.view.main_window import MainWindow


# 注册全局异常处理
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
    logger.critical("您正在测试模式下运行工具箱，因此客套话就免啦，开始调试吧hiahiahia（划掉）")
    logger.critical("下面将打印异常 Traceback，您可以将此情报反馈给芒果来处理，或者亲自研究一下工具箱的源码。")
    logger.critical(f"exc_type: {exc_type.__name__}")
    logger.critical(f"exc_value: {exc_value}")
    logger.critical(f"exc_traceback: ")
    for i in traceback.format_tb(exc_traceback):
        logger.critical("\n" + i)
    logger.critical("以上内容会被同时输出到工具箱的日志文件中。")
    logger.critical("同时如果您看上面的输出格式不爽，以下会把 Traceback 再 print 一遍：（只在命令行可见）")
    for i in traceback.format_tb(exc_traceback):
        print(i)
    logger.trace("已经……麻木了……")

sys.excepthook = handle_exception

# 准备启动
logger.trace("测试模式下不加载 Pro 组件。")
logger.warning("注意！在测试模式下，您无法启动工具箱内的任何使用了 QFluentWidgets Pro 组件的工具，也无法在工具箱本体中触发任何通过 Pro 组件实现的效果！")

logger.debug("模块导入完成。")

# enable dpi scale
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))


# create application
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "app", ".", ":/app/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

app.setStyleSheet("""QScrollArea { background: transparent; border: none; }
QWidget#scrollAreaWidgetContents { background: transparent; }
QFrame { background: transparent; border: none; }""")

logger.debug("程序初始化完成。")

# create main window
w = MainWindow()
w.show()

logger.success("工具箱本体进入事件循环。")

app.exec_()
