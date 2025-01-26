# coding:utf-8
from qfluentwidgets import (SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme, setFont, SmoothScrollArea, BodyLabel, CheckBox,
                            RangeSettingCard, ExpandGroupSettingCard, SimpleExpandGroupSettingCard)
from qfluentwidgets import FluentIcon as FIC
from qfluentwidgets import SettingCardGroup as CardGroup
from qfluentwidgets import InfoBar
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout

from .widgets.yiyan_widget import YiYanCard
from ..common.config import cfg, isWin11
from ..common.setting import HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet


class SettingCardGroup(CardGroup):

   def __init__(self, title: str, parent=None):
       super().__init__(title, parent)
       setFont(self.titleLabel, 14, QFont.Weight.DemiBold)



class SettingInterface(SmoothScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = QVBoxLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIC.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.micaEnabled,
            self.personalGroup
        )
        self.themeCard = ComboBoxSettingCard(
            cfg.themeMode,
            FIC.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.zoomCard = ComboBoxSettingCard(
            cfg.dpiScale,
            FIC.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIC.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )

        # function
        self.functionGroup = SettingCardGroup(self.tr("Functions"), self.scrollWidget)
        self.Card_YiYanEnable = SwitchSettingCard(configItem=cfg.yiYanEnabled,
                                                  icon=FIC.PASTE,
                                                  title=self.tr("Enable YiYan function (known as Hitokoto)"),
                                                  content=self.tr("When enabled, you can get a sentence by once per some seconds."))
        self.Card_YiYanAPI = OptionsSettingCard(configItem=cfg.yiYanAPI,
                                                icon=FIC.APPLICATION,
                                                title=self.tr("YiYan API"),
                                                content=self.tr("Where should we get YiYan from?"),
                                                texts=[self.tr("Official - hitokoto.cn"), self.tr("FanMirror - mangofanfan.cn")])
        self.ExpandCard_YiYanType = SimpleExpandGroupSettingCard(icon=FIC.TAG,
                                                                 title=self.tr("YiYan categories (only Simplified Chinese)"),
                                                                 content=self.tr("What categories of YiYan would you like to see? (full chosen = none chosen)"),
                                                                 parent=self.scrollWidget)
        self.Card_UpdateYiYanNow = PushSettingCard(title=self.tr("Update YiYan Now"),
                                                   icon=FIC.UPDATE,
                                                   content=self.tr("Update YiYan immediately and globally."),
                                                   text=self.tr("Update"),
                                                   parent=self.scrollWidget)
        self.Card_TimeSleep = RangeSettingCard(configItem=cfg.timeSleep,
                                               title=self.tr("Duration to refresh"),
                                               content=self.tr("How long should we sleep before refreshing online resources again?"),
                                               icon=FIC.SEND)

        BodyLabel_YiYanTypeA = BodyLabel()
        BodyLabel_YiYanTypeA.setText("我们一直在一起，所以最后也想在你身旁。——火影忍者")
        CheckBox_YiYanTypeA = CheckBox()
        CheckBox_YiYanTypeA.setText("动画（a）")
        CheckBox_YiYanTypeA.setChecked(cfg.get(cfg.yiYanTypeA))
        CheckBox_YiYanTypeA.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeA, CheckBox_YiYanTypeA.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeA, CheckBox_YiYanTypeA))

        BodyLabel_YiYanTypeB = BodyLabel()
        BodyLabel_YiYanTypeB.setText("不管你说再多的慌，只有自己的内心，是无法欺骗的啊。——七大罪")
        CheckBox_YiYanTypeB = CheckBox()
        CheckBox_YiYanTypeB.setText("漫画（b）")
        CheckBox_YiYanTypeB.setChecked(cfg.get(cfg.yiYanTypeB))
        CheckBox_YiYanTypeB.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeB, CheckBox_YiYanTypeB.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeB, CheckBox_YiYanTypeB))

        BodyLabel_YiYanTypeC = BodyLabel()
        BodyLabel_YiYanTypeC.setText("断剑重铸之日，骑士归来之时。——锐雯 - 英雄联盟")
        CheckBox_YiYanTypeC = CheckBox()
        CheckBox_YiYanTypeC.setText("游戏（c）")
        CheckBox_YiYanTypeC.setChecked(cfg.get(cfg.yiYanTypeC))
        CheckBox_YiYanTypeC.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeC, CheckBox_YiYanTypeC.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeC, CheckBox_YiYanTypeC))

        BodyLabel_YiYanTypeD = BodyLabel()
        BodyLabel_YiYanTypeD.setText("所谓家嘛，就是一个能让你懒惰、晕眩、疯狂放松的地方。——龙应台 - 亲爱的安德烈")
        CheckBox_YiYanTypeD = CheckBox()
        CheckBox_YiYanTypeD.setText("文学（d）")
        CheckBox_YiYanTypeD.setChecked(cfg.get(cfg.yiYanTypeD))
        CheckBox_YiYanTypeD.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeD, CheckBox_YiYanTypeD.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeD, CheckBox_YiYanTypeD))

        BodyLabel_YiYanTypeE = BodyLabel()
        BodyLabel_YiYanTypeE.setText("不要太在意，太在意会开始害怕失去。——Cherri")
        CheckBox_YiYanTypeE = CheckBox()
        CheckBox_YiYanTypeE.setText("原创（e）")
        CheckBox_YiYanTypeE.setChecked(cfg.get(cfg.yiYanTypeE))
        CheckBox_YiYanTypeE.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeE, CheckBox_YiYanTypeE.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeE, CheckBox_YiYanTypeE))

        BodyLabel_YiYanTypeF = BodyLabel()
        BodyLabel_YiYanTypeF.setText("和谐的生活离不开摸头和被摸头。——豆瓣网友")
        CheckBox_YiYanTypeF = CheckBox()
        CheckBox_YiYanTypeF.setText("来自网络（f）")
        CheckBox_YiYanTypeF.setChecked(cfg.get(cfg.yiYanTypeF))
        CheckBox_YiYanTypeF.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeF, CheckBox_YiYanTypeF.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeF, CheckBox_YiYanTypeF))

        BodyLabel_YiYanTypeG = BodyLabel()
        BodyLabel_YiYanTypeG.setText("日出而作，日入而息。——击壤歌")
        CheckBox_YiYanTypeG = CheckBox()
        CheckBox_YiYanTypeG.setText("其他（g）")
        CheckBox_YiYanTypeG.setChecked(cfg.get(cfg.yiYanTypeG))
        CheckBox_YiYanTypeG.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeG, CheckBox_YiYanTypeG.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeG, CheckBox_YiYanTypeG))

        BodyLabel_YiYanTypeH = BodyLabel()
        BodyLabel_YiYanTypeH.setText("看看人间的苦难，听听人民的呐喊！——《悲惨世界》")
        CheckBox_YiYanTypeH = CheckBox()
        CheckBox_YiYanTypeH.setText("影视（h）")
        CheckBox_YiYanTypeH.setChecked(cfg.get(cfg.yiYanTypeH))
        CheckBox_YiYanTypeH.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeH, CheckBox_YiYanTypeH.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeH, CheckBox_YiYanTypeH))

        BodyLabel_YiYanTypeI = BodyLabel()
        BodyLabel_YiYanTypeI.setText("晚日寒鸦一片愁。柳塘新绿却温柔。——辛弃疾 - 鹧鸪天·晚日寒鸦一片愁")
        CheckBox_YiYanTypeI = CheckBox()
        CheckBox_YiYanTypeI.setText("诗词（i）")
        CheckBox_YiYanTypeI.setChecked(cfg.get(cfg.yiYanTypeI))
        CheckBox_YiYanTypeI.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeI, CheckBox_YiYanTypeI.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeI, CheckBox_YiYanTypeI))

        BodyLabel_YiYanTypeJ = BodyLabel()
        BodyLabel_YiYanTypeJ.setText("飒爽英姿闯江湖，诗酒茶话莫孤独。——岚")
        CheckBox_YiYanTypeJ = CheckBox()
        CheckBox_YiYanTypeJ.setText("网易云（j）")
        CheckBox_YiYanTypeJ.setChecked(cfg.get(cfg.yiYanTypeJ))
        CheckBox_YiYanTypeJ.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeJ, CheckBox_YiYanTypeJ.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeJ, CheckBox_YiYanTypeJ))

        BodyLabel_YiYanTypeK = BodyLabel()
        BodyLabel_YiYanTypeK.setText("眼睛是心灵的窗户。——达芬奇")
        CheckBox_YiYanTypeK = CheckBox()
        CheckBox_YiYanTypeK.setText("哲学（k）")
        CheckBox_YiYanTypeK.setChecked(cfg.get(cfg.yiYanTypeK))
        CheckBox_YiYanTypeK.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeK, CheckBox_YiYanTypeK.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeK, CheckBox_YiYanTypeK))

        BodyLabel_YiYanTypeL = BodyLabel()
        BodyLabel_YiYanTypeL.setText("大本钟下送快递——上面摆，下面寄。——饭堂周末夜")
        CheckBox_YiYanTypeL = CheckBox()
        CheckBox_YiYanTypeL.setText("抖机灵（l）")
        CheckBox_YiYanTypeL.setChecked(cfg.get(cfg.yiYanTypeL))
        CheckBox_YiYanTypeL.stateChanged.connect(lambda: cfg.set(cfg.yiYanTypeL, CheckBox_YiYanTypeL.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeL, CheckBox_YiYanTypeL))

        # update software
        self.updateSoftwareGroup = SettingCardGroup(
            self.tr("Software update"), self.scrollWidget)
        self.Card_CheckUpdateOnStartUp = SwitchSettingCard(
            FIC.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )
        self.Card_CheckUpdateNow = PushSettingCard(
            icon=FIC.UPDATE,
            title=self.tr('Check for updates right now'),
            content=self.tr('The new version will be more stable and have more features'),
            text=self.tr("Check")
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 100, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        setFont(self.settingLabel, 23, QFont.Weight.DemiBold)
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self._connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 50)

        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.personalGroup.addSettingCard(self.languageCard)

        self.functionGroup.addSettingCard(self.Card_YiYanEnable)
        self.functionGroup.addSettingCard(self.Card_YiYanAPI)
        self.functionGroup.addSettingCard(self.ExpandCard_YiYanType)
        self.functionGroup.addSettingCard(self.Card_UpdateYiYanNow)
        self.functionGroup.addSettingCard(self.Card_TimeSleep)

        self.updateSoftwareGroup.addSettingCard(self.Card_CheckUpdateOnStartUp)
        self.updateSoftwareGroup.addSettingCard(self.Card_CheckUpdateNow)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.functionGroup)
        self.expandLayout.addWidget(YiYanCard())
        self.expandLayout.addStretch()

    def _showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    def _connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self._showRestartTooltip)

        # personalization
        cfg.themeChanged.connect(setTheme)
        self.micaCard.checkedChanged.connect(signalBus.micaEnableChanged)

        self.Card_UpdateYiYanNow.clicked.connect(signalBus.hitokotoStartUpdate)
        self.Card_CheckUpdateNow.clicked.connect(signalBus.checkUpdateSig)

        return None
    
    @staticmethod
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
