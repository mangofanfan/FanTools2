from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import  BodyLabel, LineEdit, PasswordLineEdit, FluentIcon, ConfigItem, SimpleExpandGroupSettingCard

from .config import translator_config


class APISettingCard(SimpleExpandGroupSettingCard):
    def __init__(self,
                 icon: str | QIcon | FluentIcon,
                 title: str,
                 content: str,
                 parent,
                 arg1name: str,
                 arg2name: str,
                 configItem1: ConfigItem,
                 configItem2: ConfigItem):
        super().__init__(icon=icon, title=title, content=content, parent=parent)
        BodyLabel_1 = BodyLabel()
        BodyLabel_1.setText(arg1name)
        self.LineEdit_1 = LineEdit()
        self.LineEdit_1.setFixedWidth(300)
        self.LineEdit_1.editingFinished.connect(lambda: translator_config.set(configItem1, self.LineEdit_1.text()))
        self.LineEdit_1.setText(translator_config.get(configItem1))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_1, self.LineEdit_1))

        BodyLabel_2 = BodyLabel()
        BodyLabel_2.setText(arg2name)
        self.LineEdit_2 = PasswordLineEdit()
        self.LineEdit_2.setFixedWidth(300)
        self.LineEdit_2.editingFinished.connect(lambda: translator_config.set(configItem2, self.LineEdit_2.text()))
        self.LineEdit_2.setText(translator_config.get(configItem2))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_2, self.LineEdit_2))


def expandCardAddWidget(label, widget):
    w = QWidget()
    layout = QHBoxLayout(w)
    layout.setContentsMargins(30, 0, 0, 0)
    w.setLayout(layout)
    w.setFixedHeight(50)

    widget.setMaximumWidth(160)
    layout.addWidget(label)
    layout.addWidget(widget)
    return w