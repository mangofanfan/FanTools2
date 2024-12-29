# coding:utf-8
import os
import sys

from PySide6.QtCore import Qt, QTranslator, QFile
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator
from qfluentwidgetspro import ProTranslator

from app.common.config import cfg
from app.view.register_window import RegisterWindow

from qfluentwidgetspro import setLicense
setLicense(open(file="ProLicense").read())


# enable dpi scale
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

# internationalization
locale = cfg.get(cfg.language).value
translator1 = FluentTranslator(locale)
translator2 = ProTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "app", ".", ":/app/i18n")

app.installTranslator(translator1)
app.installTranslator(translator2)
app.installTranslator(galleryTranslator)

app.setStyleSheet("""QScrollArea { background: transparent; border: none; }
QWidget#scrollAreaWidgetContents { background: transparent; }
QFrame { background: transparent; border: none; }""")

# create main window
w = RegisterWindow()
w.show()

app.exec()
