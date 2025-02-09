# 与窗口化工作有关的函数

from tkinter import messagebox
from .Config_for_Window import config
from .crypt_1 import crypt_1
from .crypt_2 import crypt_2
import traceback


class window_func:
    def click_encrypt_1(self: int, input_text, key_text):
        global output_text
        input_text = window_func.check_no_input(0, input_text)
        input_text = window_func.check_input_str(0, input_text)
        key_text = window_func.check_no_key(0, key_text)
        key_text = window_func.check_key_int(0, key_text)
        output_text = crypt_1.encrypt_window(0, input_text, key_text)
        messagebox.showinfo(title=config.messagebox_title,
                            message=config.lang_output_1_1 + output_text + "\n" +
                                    config.lang_output_1_2 + input_text + "\n" +
                                    config.lang_output_3 + str(key_text) + "\n" +
                                    config.lang_output_4
                            )
        return output_text

    def click_decrypt_1(self: int, input_text: str, key_text: int):
        global output_text
        input_text = window_func.check_no_input(0, input_text)
        input_text = window_func.check_input_str(0, input_text)
        key_text = window_func.check_no_key(0, key_text)
        key_text = window_func.check_key_int(0, key_text)
        output_text = crypt_1.decrypt_window(0, input_text, key_text)
        messagebox.showinfo(title=config.messagebox_title,
                            message=config.lang_output_2_1 + output_text + "\n" +
                                    config.lang_output_2_2 + input_text + "\n" +
                                    config.lang_output_3 + str(key_text) + "\n" +
                                    config.lang_output_4
                            )
        return output_text

    def click_encrypt_2(self: int, input_text: str, key_text: str):
        global output_text
        input_text = window_func.check_no_input(0, input_text)
        input_text = window_func.check_input_str(0, input_text)
        key_text = window_func.check_no_key(0, key_text)
        key_text = window_func.check_key_str(0, key_text)
        output_text = crypt_2.encrypt_window(0, input_text, key_text)
        messagebox.showinfo(title=config.messagebox_title,
                            message=config.lang_output_1_1 + output_text + "\n" +
                                    config.lang_output_1_2 + input_text + "\n" +
                                    config.lang_output_3 + str(key_text) + "\n" +
                                    config.lang_output_4
                            )
        return output_text

    def click_decrypt_2(self: int, input_text: str, key_text: str):
        global output_text
        input_text = window_func.check_no_input(0, input_text)
        input_text = window_func.check_input_str(0, input_text)
        key_text = window_func.check_no_key(0, key_text)
        key_text = window_func.check_key_str(0, key_text)
        output_text = crypt_2.decrypt_window(0, input_text, key_text)
        messagebox.showinfo(title=config.messagebox_title,
                            message=config.lang_output_2_1 + output_text + "\n" +
                                    config.lang_output_2_2 + input_text + "\n" +
                                    config.lang_output_3 + str(key_text) + "\n" +
                                    config.lang_output_4
                            )
        return output_text

    # 检测输入给加密/解密算法的内容是否是支持的str或int
    # 预备

    def warning_not_str_input(self: int):
        messagebox.showwarning(title=config.warning_title, message=config.warning_not_str_input)
        return 0

    def warning_no_key(self: int):
        messagebox.showwarning(title=config.warning_title, message=config.warning_no_key)
        return 0

    def warning_not_int_key(self: int):
        messagebox.showwarning(title=config.warning_title, message=config.warning_not_int_key)
        return 0

    def warning_not_str_key(self: int):
        messagebox.showwarning(title=config.warning_title, message=config.warning_not_str_key)
        return 0

    def warning_no_input(self: int):
        messagebox.showwarning(title=config.warning_title, message=config.warning_no_input)
        return 0

    # 正式调用

    def check_key_int(self: int, key_text):
        try:
            key_text = int(key_text)
            return key_text
        except:
            window_func.warning_not_int_key(0)
            return 0

    def check_key_str(self: int, key_text):
        try:
            key_text = str(key_text)
            return key_text
        except:
            window_func.warning_not_str_key(0)
            return "a"

    def check_input_str(self: int, input_text):
        try:
            input_text = str(input_text)
            return input_text
        except:
            window_func.warning_not_str_input(0)
            return 0

    def check_no_key(self: int, key_text):
        if len(key_text) == 0:
            window_func.warning_no_key(0)
            return 0
        else:
            return key_text

    def check_no_input(self: int, input_text):
        if len(input_text) == 0:
            window_func.warning_no_input(0)
            return 0
        else:
            return input_text

    # 写入日志到txt文件

    def logger_playing(self: int, log_name: str, log_txt: str):
        log_path = "SimpleCrypt/" + log_name + ".txt"
        try:
            open(mode="w+", file=log_path).write(log_txt)
            return_message = config.log_success
        except:
            error_text = traceback.format_exc()
            return_message = error_text
        messagebox.showinfo(title="提示", message=return_message)
        return 0
