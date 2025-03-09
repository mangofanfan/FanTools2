import polib
import pathlib

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
            _list.append(TextObject(entry.msgid, entry.msgstr, entry.comment, entry.translated(), entry.fuzzy, entry.flags, self.updateTextObject))
        return _list

    def updateTextObject(self, textObject: TextObject) -> None:
        """ 更新有变化的翻译文本 """
        for entry in self._poFile:
            if entry.msgid == textObject.getOriginalText():
                entry.msgstr = textObject.getTranslatedText()
                entry.comment = textObject.getComment()
                entry.flags = textObject.getFlags()

    def save(self) -> None:
        """ 将变化保存到po文件 """
        self._poFile.save(self._filePath)
        return None

    def getTextTotal(self) -> int:
        """ 获取翻译词条总数 """
        return len(self._poFile)

    def getTranslatedTextTotal(self) -> int:
        """ 获取已翻译的词条总数 """
        return len(self._poFile.translated_entries())

    def getUnTranslatedTextTotal(self) -> int:
        """ 获取已翻译的词条总数 """
        return len(self._poFile.untranslated_entries())

    def getFuzzyTextTotal(self) -> int:
        return len(self._poFile.fuzzy_entries())

    def getPercentTranslatedTotal(self) -> int:
        """ 获取已翻译的词条总数 """
        return self._poFile.percent_translated()

    def getPoFileName(self) -> str:
        """ 获取po文件名 """
        return pathlib.Path(self._filePath).name

    def getOriginalTextList(self) -> list[str]:
        _list = []
        for entry in self._poFile:
            _list.append(entry.msgid)
        return _list
