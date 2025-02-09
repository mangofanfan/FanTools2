# 日志文件写入模块，用于将日志打印到log.txt或其他文件中

import tkinter as tk
from .Config_for_Window import config
from .Functions_for_Window import window_func


def launch_logger(log_txt: str):
    logger = tk.Tk()
    logger.title(config.logger_title)
    logger.iconbitmap(config.icon_path)
    logger.resizable(False, False)

    # 第一行：文字提示
    tip_input_written_txt_name = tk.Label(logger, text=config.logger_input_written_txt_name_1, font=("微软雅黑", 12))
    tip_input_written_txt_name.grid(row=1, column=1, columnspan=3)

    # 第二行：输入框和后缀名“txt”
    normal_name = tk.StringVar()
    input_written_txt_name = tk.Entry(logger, textvariable=normal_name, font=("微软雅黑", 12))
    input_written_txt_name.grid(row=2, column=1, sticky="e")
    tip_txt = tk.Label(logger, text=".txt（拓展名无法更改）", font=("微软雅黑", 12))
    tip_txt.grid(row=2, column=2, sticky="w")

    # 第三行：文字提示 和 确认写入按钮
    tip_wait_for_logging_text = tk.Label(logger, text=config.lang_wait_for_logging_text, font=("微软雅黑", 12))
    tip_wait_for_logging_text.grid(row=3, column=1)
    confirm_logging_buttom = tk.Button(logger, text=config.lang_confirm_logging_bottom, font=("微软雅黑", 12))
    confirm_logging_buttom.grid(row=3, column=2, sticky="w"+"e")

    # 第四行：内容显示 和 数值滑块
    y_scroll = tk.Scrollbar(logger)
    y_scroll.grid(row=4, column=3, sticky="n"+"s")
    wait_for_logging_text = tk.Text(logger, exportselection=True,  # 允许内容复制到剪贴板
                                    bg="LightCyan", wrap="none", font=("微软雅黑", 12), relief="groove")
    wait_for_logging_text.grid(row=4, column=1, columnspan=2)
    wait_for_logging_text.config(yscrollcommand=y_scroll.set)
    y_scroll.config(command=wait_for_logging_text.yview)

    wait_for_logging_text.insert(index="end", chars=log_txt)

    confirm_logging_buttom.config(command=lambda: window_func.logger_playing(0, input_written_txt_name.get(), wait_for_logging_text.get(index1="0.0", index2="end")))

    # 最后
    normal_name.set(config.logger_input_written_txt_name_2)
    logger.focus()
    logger.mainloop()

