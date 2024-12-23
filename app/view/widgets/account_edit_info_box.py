from PySide6.QtCore import QSize, Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, AvatarWidget, StrongBodyLabel, LineEdit, BodyLabel, PrimaryPushButton

from app.common.error import UserCodeWrongError
from app.common.license_service import LicenseService


class AccountEditInfoBox(MessageBoxBase):
    successSignal = Signal()
    def __init__(self, name: str, uuid: str, mail: str, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.name = name
        self.uuid = str(uuid)
        self.mail = mail
        self.ls = LicenseService()

        self.hBox = QHBoxLayout()
        self.viewLayout.addLayout(self.hBox)

        self.aBox = QVBoxLayout()
        self.hBox.addLayout(self.aBox)

        self.AvatarWidget = AvatarWidget()
        self.AvatarWidget.setFixedSize(QSize(200, 200))
        self.AvatarWidget.setRadius(100)
        self.aBox.addWidget(self.AvatarWidget)

        self.Push_Avatar = PrimaryPushButton()
        self.Push_Avatar.setText(self.tr("Change Avatar"))
        self.Push_Avatar.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://cravatar.cn/")))
        self.aBox.addWidget(self.Push_Avatar)

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

        self.pBox = QVBoxLayout()
        self.hBox.addLayout(self.pBox)
        self.label_OldCode = StrongBodyLabel(self.tr("Old Code"))
        self.lineE_OldCode = LineEdit()
        self.label_NewCode = StrongBodyLabel(self.tr("New Code"))
        self.lineE_NewCode = LineEdit()

        self.lineE_OldCode.setFixedWidth(300)
        self.lineE_NewCode.setFixedWidth(300)

        self.pBox.addWidget(self.label_OldCode)
        self.pBox.addWidget(self.lineE_OldCode)
        self.pBox.addWidget(self.label_NewCode)
        self.pBox.addWidget(self.lineE_NewCode)

        self.CodeTip = BodyLabel(self.tr("You can set your Account Activation Code here.\n"
                                        "Next time you need to login with code you set here.\n"
                                        "Once you set your code, you can never cancel it but only change it.\n"
                                        "Whatever you do here on your account, your Old Code is needed to confirm them."))
        self.CodeTip.setWordWrap(True)
        self.pBox.addWidget(self.CodeTip)

        self.ErrorLabel = StrongBodyLabel()
        self.ErrorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ErrorLabel.setHidden(True)
        self.viewLayout.addWidget(self.ErrorLabel)

        self._loadAvatar()


    def _loadAvatar(self) -> None:
        ls = LicenseService()
        ls.getAvatar(self.AvatarWidget.setImage, 200)
        return None


    def validate(self) -> bool:
        ls = LicenseService()

        if (code := ls.changeUserInfo(oldCode=self.lineE_OldCode.text(),
                                      name=self.lineE_Name.text(),
                                      newCode=self.lineE_NewCode.text(),)) == 0:
            return True
        elif code == 1:
            self.ErrorLabel.setText(self.tr("Old Code Wrong. Please try again."))
            self.ErrorLabel.setVisible(True)
            return False
        elif code == -1:
            self.ErrorLabel.setText(self.tr("Unknown Error. Please try again."))
            self.ErrorLabel.setVisible(True)
            return False
