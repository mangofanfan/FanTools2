from abc import ABC, abstractmethod
from enum import Enum

from .language import Language


class TranslateError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class API(Enum):
    BaiDu = "BaiDu"
    YouDao = "YouDao"
    Local = "Local"


class TranslateAPI(ABC):
    """ 翻译 API 的基类，基础属性必须实现 """
    def __init__(self):
        self._ApiName = "BaseAPI"
        self._ApiWeb = "BaseAPIWeb"
        self._api = "https://api.web.qaq"

    def __str__(self):
        return f"[ {self._ApiName} | {self._ApiWeb} ]"

    @abstractmethod
    def translate(self, originalText: str, originalLan: Language, targetLan: Language, connect: callable) -> None:
        """ 实现翻译功能，传入字符串，返回字符串 """
        ...

    @abstractmethod
    def test(self) -> bool:
        """ 测试 API 可用性 """
        ...
