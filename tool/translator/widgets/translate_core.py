from .translateapi import *


class TranslateCore:
    def __init__(self):
        pass

    def initBaiDu(self):
        self.BaiDu = BaiDu()

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
