# 字符串加密，秘钥为一不长于密文的字符串

from Functions import word_dict

class crypt_2:
    # 专门用于窗口操作的部分
    def encrypt_window(self: int, before_encrypt_str: str, key_str: str):
        length = len(before_encrypt_str)

        word_list_1 = []

        word_list_2 = []

        for i in range(length):
            unit_1 = before_encrypt_str[i: i + 1]
            word_list_1.append(unit_1)

        for i in word_list_1:
            unit_2 = word_dict.word_dict[i]
            word_list_2.append(unit_2)

        key_length = len(key_str)

        key_list_1 = []

        for p in range(key_length):
            key = key_str[p: p + 1]
            key_list_1.append(key)

        num = length // key_length + 1

        key_list_2 = num * key_list_1

        key_list_3 = []

        word_list_3 = []

        word_list_4 = []

        for i in key_list_2:
            key_int = word_dict.word_dict[i]
            key_list_3.append(key_int)

        for i in range(length):
            unit_3 = int(word_list_2[i]) + int(key_list_3[i])
            unit_3 = word_dict.letter_changing(0, unit_3)
            word_list_3.append(unit_3)

        for i in word_list_3:
            unit_4 = word_dict.word_dict[i]
            word_list_4.append(unit_4)

        after_decrypt_str = "".join(word_list_4)

        return after_decrypt_str

    def decrypt_window(self: int, before_encrypt_str: str, key_str: str):
        length = len(before_encrypt_str)

        word_list_1 = []

        word_list_2 = []

        for i in range(length):
            unit_1 = before_encrypt_str[i: i + 1]
            word_list_1.append(unit_1)

        for i in word_list_1:
            unit_2 = word_dict.word_dict[i]
            word_list_2.append(unit_2)

        key_length = len(key_str)

        key_list_1 = []

        for p in range(key_length):
            key = key_str[p: p + 1]
            key_list_1.append(key)

        num = length // key_length + 1

        key_list_2 = num * key_list_1

        key_list_3 = []

        word_list_3 = []

        word_list_4 = []

        for i in key_list_2:
            key_int = word_dict.word_dict[i]
            key_list_3.append(key_int)

        for i in range(length):
            unit_3 = int(word_list_2[i]) - int(key_list_3[i])
            unit_3 = word_dict.letter_changing(0, unit_3)
            word_list_3.append(unit_3)

        for i in word_list_3:
            unit_4 = word_dict.word_dict[i]
            word_list_4.append(unit_4)

        after_decrypt_str = "".join(word_list_4)

        return after_decrypt_str