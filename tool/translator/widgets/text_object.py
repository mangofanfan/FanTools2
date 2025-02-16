class TextObject:
    """
    翻译文本对象，一个翻译词条对应一个此对象
    """
    id_count = 0
    def __init__(self, originalText: str, translatedText: str=None):
        self.originalText = originalText
        self.translatedText = translatedText

        # 自动增加编号
        TextObject.id_count += 1
        self.id = TextObject.id_count