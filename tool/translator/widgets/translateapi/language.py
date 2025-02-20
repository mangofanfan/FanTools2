from enum import Enum


class Language(Enum):
    """ 并非任何标准的语言代码，只是给翻译 API 模块配合使用 """
    zh_CHS = "zh-CHS"
    zh_CHT = "zh-CHT"
    en = "en"
