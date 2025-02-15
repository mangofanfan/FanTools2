from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from app.common import resource

from ..designer.TranslatorMainWindow import Ui_Form as Ui_TranslatorMainWindow

from ...public.public_window import FanWindow


class TranslatorMainWindow(Ui_TranslatorMainWindow, FanWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.resize(QSize(800, 600))
        self.setWindowTitle("Translator")
        self.setWindowIcon(QIcon(":app/images/icons/IconTranslate.png"))
