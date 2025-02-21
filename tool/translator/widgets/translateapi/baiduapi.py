import hashlib
import json
import random
from enum import Enum
from typing import NoReturn
from urllib.parse import quote

from PySide6.QtWidgets import QApplication

from app.common.logger import logger
from app.common.network import QRequestReady
from .baseapi import TranslateAPI, TranslateError, API
from .language import Language
from ..config import translator_config


class BaiDu(TranslateAPI):
    def __init__(self):
        self._ApiName = "BaiDu"
        self._ApiWeb = "https://api.fanyi.baidu.com/product/11"
        self._api = "https://fanyi-api.baidu.com/api/trans/vip/translate"

    def translate(self, originalText: str, originalLan: Language, targetLan: Language, connect: callable) -> None:
        appid = translator_config.get(translator_config.BaiDuAPPID)
        key = translator_config.get(translator_config.BaiDuKey)
        salt = str(random.randint(100000, 999999))
        sign = hashlib.md5((appid + originalText + salt + key).encode("utf-8")).hexdigest()
        originalLan = getattr(BaiDuLanguage, originalLan.value.replace("-", "_"))
        targetLan = getattr(BaiDuLanguage, targetLan.value.replace("-", "_"))
    
        fanyi_url = f"{self._api}?q={quote(originalText)}&from={originalLan.value}&to={targetLan.value}&appid={appid}&salt={salt}&sign={sign}"
    
        logger.trace(f"正在调用百度通用文本翻译API执行翻译，目标URL为 {fanyi_url}")

        def thenDo(_res: dict) -> str | NoReturn:
            if "error_code" in _res or "error_msg" in _res:
                code = _res["error_code"]
                logger.error(
                    f"百度文本翻译API调用错误，错误代码：{code} | 请参阅有道提供的文档 [ https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html#section-10 ] 查看详情。")
                raise TranslateError(f"百度文本翻译 API 调用错误，返回值为 {code}")
            return _res["trans_result"][0]["dst"]
    
        (
            QRequestReady(QApplication.instance())
            .get(fanyi_url)
            .then(lambda _res: thenDo(json.loads(_res)))
            .then(lambda targetText: (connect(originalText, targetText, API.BaiDu), logger.debug(f"百度翻译结果：{originalText} => {targetText}")))
            .done()
        )

        return

    def test(self) -> bool:
        pass


class BaiDuLanguage(Enum):
    zh_CHS = "zh"
    zh_CHT = "zht"
    en = "en"
