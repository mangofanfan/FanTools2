from qfluentwidgets import QConfig, ConfigItem, qconfig

from ...public.function import getToolDir


class TranslatorConfig(QConfig):
    # 百度翻译
    BaiDuAPPID = ConfigItem("BaiDu", "BaiduAPPID", "")
    BaiDuKey = ConfigItem("BaiDu", "BaiduKey", "")

    # 有道翻译
    YouDaoAPPKey = ConfigItem("YouDao", "YouDaoAPPKey", "")
    YouDaoKey = ConfigItem("YouDao", "YouDaoKey", "")


translator_config = TranslatorConfig()
qconfig.load(f"{getToolDir()}/private/translator_config.json", translator_config)
