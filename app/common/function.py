from os import getcwd, getenv
from pathlib import Path


class Singleton(object):
    """
    A singleton class that provides a singleton.
    """

    def __init__(self, cls):
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self):
        if self.uniqueInstance is None:
            self.uniqueInstance = self._cls()
        return self.uniqueInstance


class basicFunc:
    def __init__(self):
        pass


    @staticmethod
    def getHerePath() -> str:
        return getcwd()

    @staticmethod
    def readFile(file: str, realPath: bool = False) -> str:
        if realPath:
            with open(file=file, mode="r", encoding="utf-8") as f:
                r = f.read()
            return r
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="r", encoding="utf-8") as f:
            r = f.read()
        return r

    @staticmethod
    def saveFile(file: str, text: str, realPath: bool = False):
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        if realPath:
            with open(file=file, mode="w+", encoding="utf-8") as f:
                f.write(text)
            return None
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="w+", encoding="utf-8") as f:
            f.write(text)
        return None

    @staticmethod
    def rgb_to_hex(rgb):
        r, g, b = rgb
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        hex_string = '{:02X}{:02X}{:02X}'.format(r, g, b)
        return hex_string



def _iconPath(fileName: str):
    return basicFunc.getHerePath() + f"/data/icon/Icon{fileName}"

def _fontPath(fileName: str):
    return basicFunc.getHerePath() + f"/data/font/{fileName}"


