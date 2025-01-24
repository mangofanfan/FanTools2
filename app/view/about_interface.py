from PySide6.QtCore import QSize, QUrl, QFile
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget
from qfluentwidgets import BodyLabel

from .designer.about_interface import Ui_Form as AboutForm
from ..common import resource
from ..common.license_service import LicenseService


class AboutInterface(QWidget, AboutForm):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setObjectName('AboutInterface')
        self.ls = LicenseService()
        self.initWindow()

    def initWindow(self) -> None:
        # 头像卡片
        self.AvatarWidget.setImage(QImage(":/app/images/avatar.png"))
        self.AvatarWidget.setFixedSize(QSize(72, 72))
        self.AvatarWidget.setRadius(36)
        self.TitleLabel.setText(self.tr("MangoFanFan,"))
        self.SubtitleLabel.setText(self.tr("Maybe a player, maybe a student?"))

        # 二维码卡片
        self.ImageLabel.setImage(QImage(":/app/images/payQRcode.png"))
        self.ImageLabel.setFixedSize(QSize(200, 200))
        self.ImageLabel.setBorderRadius(5, 5, 5, 5)
        self.BodyLabel.setText(self.tr("or"))
        self.HyperlinkButton.setText(self.tr("Support Me"))
        self.HyperlinkButton.setUrl(QUrl("https://pay.dns163.cn/paypage/?merchant=3dc6X8Y8GegAtOXu6rZZULGW%2F33IUKWcKjsT4JZHhcOE"))

        # 关于卡片
        self.HeaderCardWidget.setTitle(self.tr("About FanTools"))
        tipFile = QFile(":/app/texts/about_tip.md")
        tipFile.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        BodyLabel_tip = BodyLabel()
        BodyLabel_tip.setText(str(tipFile.readAll(), "utf-8"))
        self.HeaderCardWidget.viewLayout.addWidget(BodyLabel_tip)
        tipFile.close()

        # 技术卡片
        self.ImageLabel_Python.setImage(QImage(":/app/IconPython"))
        self.ImageLabel_Python.setFixedSize(QSize(60, 60))
        self.ImageLabel_Python.setBorderRadius(5, 5, 5, 5)
        self.ImageLabel_PySide.setImage(QImage(":/app/IconPySide"))
        self.ImageLabel_PySide.setFixedSize(QSize(60, 60))
        self.ImageLabel_PySide.setBorderRadius(5, 5, 5, 5)
        self.ImageLabel_QFluentWidget.setImage(QImage(":/app/IconFluent"))
        self.ImageLabel_QFluentWidget.setFixedSize(QSize(60, 60))
        self.ImageLabel_QFluentWidget.setBorderRadius(5, 5, 5, 5)
        self.SubtitleLabel_Python.setText("Python")
        self.SubtitleLabel_PySide.setText("PySide")
        self.SubtitleLabel_QFluentWidget.setText("QFluentWidgets")
        self.BodyLabel_Python.setText(self.tr("Simple Language!"))
        self.BodyLabel_PySide.setText(self.tr("Simple GUI!"))
        self.BodyLabel_QFluentWidget.setText(self.tr("Simple Beauty!"))

        # 新闻卡片
        self.SubtitleLabel_News.setText(self.tr("Wait for news ^.."))
        self.BodyLabel_NewsTime.setText(self.tr("Which time?"))
        self.BodyLabel_News.setText(self.tr("What news?"))
        self.ls.getNews(self._initNews)

        # 链接卡片
        self.ImageLabel_Docs.setImage(QImage(":/app/IconDocs"))
        self.ImageLabel_Docs.setFixedSize(QSize(60, 60))
        self.ImageLabel_Docs.setBorderRadius(5, 5, 5, 5)
        self.ImageLabel_GitHub.setImage(QImage(":/app/IconGitHub"))
        self.ImageLabel_GitHub.setFixedSize(QSize(60, 60))
        self.ImageLabel_GitHub.setBorderRadius(5, 5, 5, 5)
        self.ImageLabel_Release.setImage(QImage(":/app/IconRelease"))
        self.ImageLabel_Release.setFixedSize(QSize(60, 60))
        self.ImageLabel_Release.setBorderRadius(5, 5, 5, 5)
        self.SubtitleLabel_Docs.setText(self.tr("FanTools Docs"))
        self.SubtitleLabel_GitHub.setText(self.tr("GitHub Repository"))
        self.SubtitleLabel_Release.setText(self.tr("Release Info"))
        self.BodyLabel_Docs.setText(self.tr("Online Docs about FanTools"))
        self.BodyLabel_GitHub.setText(self.tr("Open source repo on GitHub"))
        self.BodyLabel_Release.setText(self.tr("Release info on ifanspace.top"))

        return None

    def _initNews(self, newsTime: str, newsTitle: str, news: str) -> None:
        self.SubtitleLabel_News.setText(newsTitle)
        self.BodyLabel_NewsTime.setText(newsTime)
        self.BodyLabel_News.setText(news)
        return None

