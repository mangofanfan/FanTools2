from .translateapi import *
from .config import translator_config


class TranslateCore:
    def __init__(self):
        self.YouDao = YouDao()

    def translate(self, originalText: str, originalLan: Language, targetLan: Language, api: API, connect: callable):
        if hasattr(self, api.value):
            getattr(self, api.value).translate(originalText, originalLan, targetLan, connect)

    def test(self):
        self.YouDao.translate("test test test", Language.en, Language.zh_CHS, print)
