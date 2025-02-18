class TextObject:
    """
    翻译文本对象，一个翻译词条对应一个此对象
    """
    id_count = 0
    def __init__(self, originalText: str, translatedText: str, updateFunc: callable):
        self._originalText = originalText
        self._translatedText = translatedText
        self._updateFunc = updateFunc

        # 自动增加编号
        TextObject.id_count += 1
        self.id = TextObject.id_count

    def getOriginalText(self):
        return self._originalText

    def getTranslatedText(self):
        return self._translatedText

    def setTranslatedText(self, translatedText: str):
        self._translatedText = translatedText
        self._updateFunc(self)
        return None

    def __str__(self):
        return f"[TextObject {self.id}]"
