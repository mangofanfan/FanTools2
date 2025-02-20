import hashlib
import json
import random
import time
from typing import NoReturn
from urllib.parse import quote

from PySide6.QtWidgets import QApplication

from app.common.logger import logger
from app.common.network import QRequestReady
from .baseapi import TranslateAPI, TranslateError, API
from .language import Language
from ..config import translator_config


class YouDao(TranslateAPI):

    def __init__(self):
        super().__init__()
        self._ApiName = "YouDao"
        self._ApiWeb = "https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html"
        self._api = "https://openapi.youdao.com/api"

    def translate(self, originalText: str, originalLan: Language, targetLan: Language, connect: callable) -> None:
        appKey = translator_config.get(translator_config.YouDaoAPPKey)
        key = translator_config.get(translator_config.YouDaoKey)
        utcTime = str(int(time.time()))
        salt = str(random.randint(100000, 999999))

        # 根据 originalText 的长度来决定签名格式
        if len(originalText) > 20:
            input_ = originalText[0:10] + str(len(originalText)) + originalText[-10:len(originalText)]
        else:
            input_ = originalText
        sign = hashlib.sha256((appKey + input_ + salt + utcTime + key).encode("utf-8")).hexdigest()

        fanyi_url = f"{self._api}?q={quote(originalText)}&from={originalLan}&to={targetLan}&appKey={appKey}&salt={salt}&sign={sign}&signType=v3&curtime={utcTime}"

        logger.trace(f"正在调用有道文本翻译API执行翻译，目标URL为 {fanyi_url}")

        def thenDo(_res: dict) -> str | NoReturn:
            try:
                return _res["translation"][0]
            except KeyError:
                code = _res["errorCode"]
                logger.error(
                    f"有道翻译API调用错误，错误代码：{code} | 请参阅有道提供的文档 [ https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html#section-10 ] 查看详情。")
                raise TranslateError(f"有道文本翻译 API 调用错误，返回值为 {code}")

        (
            QRequestReady(QApplication.instance())
            .get(fanyi_url)
            .then(lambda _res: thenDo(json.loads(_res)))
            .then(lambda targetText: (connect(originalText, targetText, API.YouDao), logger.debug(f"有道翻译结果：{originalText} => {targetText}")))
            .done()
        )

        return

    def test(self) -> bool:
        pass
