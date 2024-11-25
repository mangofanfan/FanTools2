from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon

from .designer.dilingual_writing import Ui_Form as Form
from .widgets.settings_info_box import SettingsInfoBox
from ..public.public_window import FanWindow


class BilingualWritingWindow(FanWindow, Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle(self.tr("Bilingual Writing"))
        self.setWindowIcon(QIcon(":/app/images/icons/IconTranslate.png"))
        self.__initWindow()

    def __initWindow(self) -> None:
        self.SubtitleLabel.setText(self.tr("Title:"))
        self.PrimaryToolButton.setIcon(FluentIcon.ACCEPT_MEDIUM)

        self.SubtitleLabel_NewParaHere.setText(self.tr("Your new paragraph will be put here!"))

        self.BodyLabel_TrAPI.setText(self.tr("using API:"))

        self.SubtitleLabel_Settings.setText(self.tr("Settings"))
        self.PushButton_Settings.setText(self.tr("Open settings ..."))
        self.PushButton_Settings.clicked.connect(self._showSettingsInfoBox)

        return None

    def _showSettingsInfoBox(self) -> None:
        infoBox = SettingsInfoBox(self)
        infoBox.show()
        return None


if __name__ == "app.tool.bilingualWriting.run":
    window = BilingualWritingWindow()
    window.show()