from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase
from qfluentwidgetspro import RoundListWidget

from .tr_api import TrAPI, apis


class SettingsInfoBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.hViewLayout = QHBoxLayout()
        self.viewLayout.addLayout(self.hViewLayout)

        self.listWidget = RoundListWidget()
        for api in apis.getApis():
            api: TrAPI
            self.listWidget.addItem(api.name)
        self.hViewLayout.addWidget(self.listWidget)


    def validate(self) -> bool:
        return True

