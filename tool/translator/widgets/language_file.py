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
            _list.append(TextObject(entry.msgid, entry.msgstr, self.updateTextObject))
        return _list

    def updateTextObject(self, textObject: TextObject) -> None:
        """ 更新有变化的翻译文本 """
        for entry in self._poFile:
            if entry.msgid == textObject.getOriginalText():
                entry.msgstr = textObject.getTranslatedText()

    def save(self) -> None:
        """ 将变化保存到po文件 """
        self._poFile.save(self._filePath)
        return None

    def getTextTotal(self) -> int:
        """ 获取翻译词条总数 """
        return len(self._poFile)

    def getTranslatedTextTotal(self) -> int:
        """ 获取已翻译的词条总数 """
        count = 0
        for entry in self._poFile:
            # 将翻译文本不为空字符串的词条认为已被翻译
            if entry.msgstr != "":
                count += 1
            else:
                # 将两个都是空字符串的翻译词条认为已被翻译
                if entry.msgid == "":
                    count += 1
        return count

    def getPoFilePath(self) -> str:
        """ 获取po文件路径 """
        return pathlib.Path(self._filePath).name
