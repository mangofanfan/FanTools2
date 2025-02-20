class TextObject:
    """
    翻译文本对象，一个翻译词条对应一个此对象
    """
    id_count = 0
    def __init__(self, originalText: str, translatedText: str, comment: str, translated: bool, fuzzy: bool, flags: list[str], updateFunc: callable):
        self._originalText = originalText
        self._translatedText = translatedText
        self._comment = comment
        self._translated = translated
        self._fuzzy = fuzzy
        self._flags = flags
        self._updateFunc = updateFunc

        # 自动增加编号
        TextObject.id_count += 1
        self.id = TextObject.id_count

    def getOriginalText(self):
        return self._originalText

    def getTranslatedText(self):
        return self._translatedText

    def getComment(self):
        return self._comment

    def getTranslated(self):
        return self._translated

    def getFuzzy(self):
        return self._fuzzy

    def getFlags(self):
        return self._flags

    def setTranslatedText(self, translatedText: str):
        self._translatedText = translatedText
        self._updateFunc(self)
        return None

    def setComment(self, comment: str):
        self._comment = comment
        self._updateFunc(self)
        return None

    def setFuzzy(self, fuzzy: bool):
        """ 设置一个词条是否具备 fuzzy 标签，重复设置不报错 """
        self._fuzzy = fuzzy
        if fuzzy and "fuzzy" not in self._flags:
            self._flags.append("fuzzy")
        elif not fuzzy and "fuzzy" in self._flags:
            self._flags.remove("fuzzy")
        self._updateFunc(self)
        return None

    def __str__(self):
        return f"[TextObject {self.id}]"
