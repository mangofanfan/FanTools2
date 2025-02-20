from .translateapi import *
from .config import translator_config


class TranslateCore:
    def __init__(self):
        pass

    def initYouDao(self):
        self.YouDao = YouDao()

    def initLocal(self, originalTexts: list[str]):
        self.Local = Local(originalTexts)

    def translate(self, originalText: str, originalLan: Language, targetLan: Language, connect: callable):
        for api in API:
            if hasattr(self, api.value):
                getattr(self, api.value).translate(originalText, originalLan, targetLan, connect)

    def test(self):
        self.YouDao.translate("test test test", Language.en, Language.zh_CHS, print)
