import polib

from .text_object import TextObject


class PoFileObject:
    """ 一个po文件即对应一个PoFileObject """
    def __init__(self, file: str):
        self._filePath = file
        self._poFile: polib.POFile = polib.pofile(file)

    def getTextList(self) -> list[TextObject]:
        """ 按顺序获取所有文本 """
        _list = []
        for entry in self._poFile:
            _list.append(TextObject(entry.msgid, entry.msgstr))
        return _list
