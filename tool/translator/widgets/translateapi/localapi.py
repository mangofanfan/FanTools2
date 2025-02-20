from thefuzz import process

from .language import Language
from .baseapi import TranslateAPI, API


class Local(TranslateAPI):

    def __init__(self, texts: list[str]):
        super().__init__()
        self._ApiName = "Local"
        self._ApiWeb = "https://mangofanfan.cn/"
        self._api = "QAQ"

        self._texts = texts
        self._limit = 3

    def setLimit(self, limit: int):
        """ 设置返回的结果数量，默认返回数量是2 """
        self._limit = limit + 1

    def translate(self, originalText: str, originalLan: Language, targetLan: Language, connect: callable) -> None:
        resList = process.extract(originalText, self._texts, limit=self._limit)[1:]
        for res in resList:
            if res[1] >= 70:
                connect(res[1], res[0], API.Local)
        return

    def test(self) -> bool:
        pass