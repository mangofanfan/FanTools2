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


# 测试模式下不使用全局异常处理。

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
