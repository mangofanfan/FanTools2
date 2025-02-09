# 固定数字加密，秘钥为一指定数字

from .Functions import word_dict

class crypt_1:
    # 专门用于窗口操作的部分
    def encrypt_window(self: int, before_encrypt_str: str, key: int):
        length = len(before_encrypt_str)

        word_list_1 = []

        word_list_2 = []

        for i in range(length):
            unit_1 = before_encrypt_str[i: i + 1]
            word_list_1.append(unit_1)

        for i in word_list_1:
            unit_2 = word_dict.word_dict[i]
            word_list_2.append(unit_2)

        word_list_3 = []

        word_list_4 = []

        for i in word_list_2:
            unit_3 = i + key
            unit_3 = word_dict.letter_changing(0, unit_3)
            word_list_3.append(unit_3)

        for i in word_list_3:
            unit_4 = word_dict.word_dict[i]
            word_list_4.append(unit_4)

        after_encrypt_str = "".join(word_list_4)

        return after_encrypt_str

    def decrypt_window(self: int, before_decrypt_str: str, key: int):
        length = len(before_decrypt_str)

        word_list_1 = []

        word_list_2 = []

        for i in range(length):
            unit_1 = before_decrypt_str[i: i + 1]
            word_list_1.append(unit_1)

        for i in word_list_1:
            unit_2 = word_dict.word_dict[i]
            word_list_2.append(unit_2)

        word_list_3 = []

        word_list_4 = []

        for i in word_list_2:
            unit_3 = i - key
            unit_3 = word_dict.letter_changing(0, unit_3)
            word_list_3.append(unit_3)

        for i in word_list_3:
            unit_4 = word_dict.word_dict[i]
            word_list_4.append(unit_4)

        after_decrypt_str = "".join(word_list_4)

        return after_decrypt_str
