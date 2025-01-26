import json
from dataclasses import dataclass

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication

from .config import cfg
from .error import UnexpectedError
from .function import Singleton
from .logger import logger
from .network import QRequestReady
from .signal_bus import signalBus


@dataclass
class Hitokoto:
    text: str
    by: str
    data: dict


@Singleton
class HitokotoManager(QObject):
    update = Signal()
    def __init__(self):
        super().__init__()
        if cfg.get(cfg.yiYanAPI) == "official":
            self.api = "https://v1.hitokoto.cn/"
        elif cfg.get(cfg.yiYanAPI) == "fan_mirror":
            self.api = "https://api-hitokoto.mangofanfan.cn/"
        else: raise UnexpectedError()

        self.hitokoto = Hitokoto(self.tr("Here’s to the imperfect tomorrow."), self.tr("Star Rail"), {})
        signalBus.hitokotoStartUpdate.connect(self._update)

        logger.info("一言管理器初始化完毕。")

    def updateNow(self):
        """立即获取一言的外部封装"""
        self._update()
        return None

    def _update(self):
        """内部：获取新的一言"""
        def thenDo(res):
            logger.debug(f"一言API调用返回：{res}")
            text = res["hitokoto"]
            by = (res["from_who"] + " - " + res["from"]) if res["from_who"] else res["from"]
            self.hitokoto = Hitokoto(text, by, res)
            return None

        argsList = []
        argsDict = {"a": cfg.yiYanTypeA, "b": cfg.yiYanTypeB,
                    "c": cfg.yiYanTypeC, "d": cfg.yiYanTypeD,
                    "e": cfg.yiYanTypeE, "f": cfg.yiYanTypeF,
                    "g": cfg.yiYanTypeG, "h": cfg.yiYanTypeH,
                    "i": cfg.yiYanTypeI, "j": cfg.yiYanTypeJ,
                    "k": cfg.yiYanTypeK, "l": cfg.yiYanTypeL,}
        for k, v in argsDict.items():
            if cfg.get(v):
                argsList.append(f"type={k}")

        if not argsList: api = self.api
        else: api = self.api + "?" + "&".join(argsList)
        logger.trace("本次调用一言地址：", api)

        (
            QRequestReady(QApplication.instance())
            .get(api)
            .then(lambda res: thenDo(json.loads(res)))
            .then(lambda _: signalBus.hitokotoUpdate.emit())
            .done()
        )

        return None
