from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, AvatarWidget, StrongBodyLabel, LineEdit

from app.common.license_service import LicenseService


class AccountEditInfoBox(MessageBoxBase):
    def __init__(self, name: str, uuid: str, mail: str, parent=None):
        super().__init__(parent=parent)
        self.name = name
        self.uuid = uuid
        self.mail = mail

        self.hBox = QHBoxLayout()
        self.viewLayout.addLayout(self.hBox)

        self.AvatarWidget = AvatarWidget()
        self.AvatarWidget.setFixedSize(QSize(200, 200))
        self.AvatarWidget.setRadius(100)
        self.hBox.addWidget(self.AvatarWidget)

        self.vBox = QVBoxLayout()
        self.hBox.addLayout(self.vBox)

        self.label_Name = StrongBodyLabel(self.tr("User Name"))
        self.lineE_Name = LineEdit()
        self.label_Mail = StrongBodyLabel(self.tr("EMail Address"))
        self.lineE_Mail = LineEdit()
        self.label_Uuid = StrongBodyLabel(self.tr("UUID"))
        self.lineE_Uuid = LineEdit()
        self.vBox.addWidget(self.label_Name)
        self.vBox.addWidget(self.lineE_Name)
        self.vBox.addWidget(self.label_Mail)
        self.vBox.addWidget(self.lineE_Mail)
        self.vBox.addWidget(self.label_Uuid)
        self.vBox.addWidget(self.lineE_Uuid)

        self.lineE_Mail.setDisabled(True)
        self.lineE_Uuid.setDisabled(True)
        self.lineE_Name.setFixedWidth(300)
        self.lineE_Mail.setFixedWidth(300)
        self.lineE_Uuid.setFixedWidth(300)
        self.lineE_Name.setText(self.name)
        self.lineE_Mail.setText(self.mail)
        self.lineE_Uuid.setText(self.uuid)

        self._loadAvatar()


    def _loadAvatar(self) -> None:
        ls = LicenseService()
        ls.getAvatar(self.AvatarWidget.setImage, 200)
        return None


    def validate(self) -> bool:
        return True
