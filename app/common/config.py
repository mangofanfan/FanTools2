# coding:utf-8
import sys
from enum import Enum

from PySide6.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, Theme, FolderValidator, ConfigSerializer, RangeConfigItem, RangeValidator)

from .setting import CONFIG_FILE

class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Language.Chinese, QLocale.Country.HongKong)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # TODO: ADD YOUR CONFIG GROUP HERE

    # register
    rememberMe = ConfigItem("Register", "RememberMe", True)
    email = ConfigItem("Register", "Email", "")
    activationCode = ConfigItem("Register", "ActivationCode", "")

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())

    # 一言
    yiYanEnabled = ConfigItem("Function", "YiYanEnabled", True, BoolValidator())
    yiYanAPI = OptionsConfigItem("Function", "YiYanAPI", "fan_mirror", OptionsValidator(["official", "fan_mirror"]))
    yiYanTypeA = ConfigItem("Function", "YiYanTypeA", True, BoolValidator())
    yiYanTypeB = ConfigItem("Function", "YiYanTypeB", True, BoolValidator())
    yiYanTypeC = ConfigItem("Function", "YiYanTypeC", True, BoolValidator())
    yiYanTypeD = ConfigItem("Function", "YiYanTypeD", True, BoolValidator())
    yiYanTypeE = ConfigItem("Function", "YiYanTypeE", True, BoolValidator())
    yiYanTypeF = ConfigItem("Function", "YiYanTypeF", True, BoolValidator())
    yiYanTypeG = ConfigItem("Function", "YiYanTypeG", True, BoolValidator())
    yiYanTypeH = ConfigItem("Function", "YiYanTypeH", True, BoolValidator())
    yiYanTypeI = ConfigItem("Function", "YiYanTypeI", True, BoolValidator())
    yiYanTypeJ = ConfigItem("Function", "YiYanTypeJ", True, BoolValidator())
    yiYanTypeK = ConfigItem("Function", "YiYanTypeK", True, BoolValidator())
    yiYanTypeL = ConfigItem("Function", "YiYanTypeL", True, BoolValidator())
    timeSleep = RangeConfigItem("Function", "TimeSleep", 20, RangeValidator(5, 60))


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(str(CONFIG_FILE.absolute()), cfg)