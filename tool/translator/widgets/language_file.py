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
            _list.append(TextObject(entry.msgid, entry.msgstr, self.updateTextObject))
        return _list

    def updateTextObject(self, textObject: TextObject):
        """ 更新有变化的翻译文本 """
        for entry in self._poFile:
            if entry.msgid == textObject.getOriginalText():
                entry.msgstr = textObject.getTranslatedText()

    def save(self):
        """ 将变化保存到po文件 """
        self._poFile.save(self._filePath)
