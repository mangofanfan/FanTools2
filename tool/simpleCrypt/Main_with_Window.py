# 这里的代码是有关于使用tkinter库启动图形化的解释器的……
# 嗯……希望我写得出来……
import ctypes
import time as t
import tkinter as tk
import webbrowser

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)

from Logging_for_Window import launch_logger
from Config_for_Window import config
from Functions_for_Window import window_func


def launch():
    class main:
        window = tk.Tk()
        window.tk.call('tk', 'scaling', ScaleFactor/125)
        window.title(config.window_name)
        window.geometry("1000x600")
        window.iconbitmap(config.icon_path)
        window.resizable(False, False)

        background_phtot = tk.PhotoImage(file=config.background_path)

        # 下面开始正式操作

        background = tk.Label(window, image=background_phtot, width=1000, height=600, relief="flat")
        background.place(x=0, y=0, anchor="nw")

        output_1 = tk.StringVar()
        output_1.set(config.lang_still_not_1)
        output_2 = tk.StringVar()
        output_2.set(config.lang_still_not_2)
        output_3 = tk.StringVar()
        output_3.set(config.lang_still_not_1)
        output_4 = tk.StringVar()
        output_4.set(config.lang_still_not_2)
        lang_wait_for_input_1 = tk.StringVar()
        lang_wait_for_input_2 = tk.StringVar()
        lang_wait_for_input_3 = tk.StringVar()
        lang_wait_for_input_4 = tk.StringVar()
        lang_wait_for_key_1 = tk.StringVar()
        lang_wait_for_key_2 = tk.StringVar()
        lang_wait_for_key_3 = tk.StringVar()
        lang_wait_for_key_4 = tk.StringVar()

        # 窗口内标题文字

        main_title = tk.Label(window, text=config.lang_main_title, bg="lightcyan", width=20, height=5,
                              font=("微软雅黑", 14), relief="groove")
        main_title.place(x=1, y=1, anchor="nw")

        # 署名

        main_author = tk.Label(window, text=config.lang_main_author, bg="lightskyblue", fg="blue", width=29, height=1,
                               font=("微软雅黑", 10), relief="groove")
        main_author.place(x=5, y=104, anchor="nw")

        # 版本号

        version_tag = tk.Label(window, text=config.version_tag, bg="lightskyblue", fg="green", width=29, height=1,
                               font=("微软雅黑", 10), relief="groove")
        version_tag.place(x=5, y=4, anchor="nw")

        # 相关声明

        notice = tk.Label(window, text=config.lang_notice, fg="snow", bg="MediumPurple3", font=("微软雅黑", 8))
        notice.place(x=0, y=580, anchor="nw")

    # 功能分区 ——————————————————————————————————————————————————


    working_region = tk.LabelFrame(main.window, width=570, height=490,
                                   text=config.working_region_title, bg="beige",
                                   font=("微软雅黑", 12))
    working_region.place(x=426, y=44)


    # 打开帮助网页


    def open_web():
        webbrowser.open_new(config.url_help_web)
        return 0


    tip_label = tk.Button(main.window, text=config.lang_tip_label, width=26, height=1, font=("微软雅黑", 12), bg="snow2",
                          command=lambda: open_web())
    tip_label.place(x=980, y=70, anchor="ne")


    # 清空按钮


    def clean_all_input():
        nothing = ""
        main.lang_wait_for_input_1.set(nothing)
        main.lang_wait_for_input_2.set(nothing)
        main.lang_wait_for_input_3.set(nothing)
        main.lang_wait_for_input_4.set(nothing)
        main.lang_wait_for_key_1.set(nothing)
        main.lang_wait_for_key_2.set(nothing)
        main.lang_wait_for_key_3.set(nothing)
        main.lang_wait_for_key_4.set(nothing)
        return 0


    clean_all_button = tk.Button(main.window, text=config.lang_clean_all, width=14, height=1, font=("微软雅黑", 12), bg="snow1",
                                 command=lambda: clean_all_input())
    clean_all_button.place(x=440, y=70)


    class encrypt_1:
        # 输入框

        input_place_1 = tk.Entry(main.window, textvariable=main.lang_wait_for_input_1, width=50, bg="snow",
                                 font=("微软雅黑", 12))
        input_place_1.place(x=440, y=120, anchor="nw")

        input_key_1 = tk.Entry(main.window, textvariable=main.lang_wait_for_key_1, width=50, bg="snow", font=("微软雅黑", 12))
        input_key_1.place(x=440, y=150, anchor="nw")

        output_place_1 = tk.Entry(main.window, textvariable=main.output_1, width=50, bg="snow", font=("微软雅黑", 12),
                                  relief="groove")
        output_place_1.place(x=440, y=180, anchor="nw")

        # 按钮

        tk.Button(main.window, text=config.lang_confirm_1, width=7, height=3, bg="snow1", font=("微软雅黑", 16),
                  command=lambda: local_func.print_to_label_1(0,
                                                              window_func.click_encrypt_1(0, encrypt_1.input_place_1.get(),
                                                                                          encrypt_1.input_key_1.get()))
                  ).place(x=888, y=114, anchor="nw")


    class decrypt_1:
        # 输入框

        input_place_2 = tk.Entry(main.window, textvariable=main.lang_wait_for_input_2, width=50, bg="snow",
                                 font=("微软雅黑", 12))
        input_place_2.place(x=440, y=220, anchor="nw")

        input_key_2 = tk.Entry(main.window, textvariable=main.lang_wait_for_key_2, width=50, bg="snow", font=("微软雅黑", 12))
        input_key_2.place(x=440, y=250, anchor="nw")

        output_place_2 = tk.Entry(main.window, textvariable=main.output_2, width=50, bg="snow", font=("微软雅黑", 12),
                                  relief="groove")
        output_place_2.place(x=440, y=280, anchor="nw")

        # 按钮

        tk.Button(main.window, text=config.lang_confirm_2, width=7, height=3, bg="snow1", font=("微软雅黑", 16),
                  command=lambda: local_func.print_to_label_2(0,
                                                              window_func.click_decrypt_1(0, decrypt_1.input_place_2.get(),
                                                                                          decrypt_1.input_key_2.get()))
                  ).place(x=888, y=214, anchor="nw")


    class encrypt_2:
        # 输入框

        input_place_3 = tk.Entry(main.window, textvariable=main.lang_wait_for_input_3, width=50, bg="snow",
                                 font=("微软雅黑", 12))
        input_place_3.place(x=440, y=320, anchor="nw")

        input_key_3 = tk.Entry(main.window, textvariable=main.lang_wait_for_key_3, width=50, bg="snow", font=("微软雅黑", 12))
        input_key_3.place(x=440, y=350, anchor="nw")

        output_place_3 = tk.Entry(main.window, textvariable=main.output_3, width=50, bg="snow", font=("微软雅黑", 12),
                                  relief="groove")
        output_place_3.place(x=440, y=380, anchor="nw")

        # 按钮

        tk.Button(main.window, text=config.lang_confirm_1, width=7, height=3, bg="snow1", font=("微软雅黑", 16),
                  command=lambda: local_func.print_to_label_3(0,
                                                              window_func.click_encrypt_2(0, encrypt_2.input_place_3.get(),
                                                                                          encrypt_2.input_key_3.get()))
                  ).place(x=888, y=314, anchor="nw")


    class decrypt_2:
        # 输入框

        input_place_4 = tk.Entry(main.window, textvariable=main.lang_wait_for_input_4, width=50, bg="snow",
                                 font=("微软雅黑", 12))
        input_place_4.place(x=440, y=420, anchor="nw")

        input_key_4 = tk.Entry(main.window, textvariable=main.lang_wait_for_key_4, width=50, bg="snow", font=("微软雅黑", 12))
        input_key_4.place(x=440, y=450, anchor="nw")

        output_place_4 = tk.Entry(main.window, textvariable=main.output_4, width=50, bg="snow", font=("微软雅黑", 12),
                                  relief="groove")
        output_place_4.place(x=440, y=480, anchor="nw")

        # 按钮

        tk.Button(main.window, text=config.lang_confirm_2, width=7, height=3, font=("微软雅黑", 16), bg="snow1",
                  command=lambda: local_func.print_to_label_4(0,
                                                              window_func.click_decrypt_2(0, decrypt_2.input_place_4.get(),
                                                                                          decrypt_2.input_key_4.get()))
                  ).place(x=888, y=414, anchor="nw")


    # 功能分区 ——————————————————————————————————————————————————
    # 日志控件

    log_text = tk.Text(exportselection=True,  # 允许内容复制到剪贴板
                       bg="LightCyan", wrap="word", font=("微软雅黑", 12), width=45, height=12, relief="groove")
    log_text.place(x=10, y=270, anchor="nw")
    log_text.insert(index="end", chars=config.lang_log_1)

    scrollbar = tk.Scrollbar(master=log_text)
    scrollbar.place(x=407, y=0, relheight=1, anchor="ne")
    log_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=log_text.yview)

    # 欢迎使用

    hello_label = tk.Label(main.window, text=config.lang_hello_label, width=40, height=1,
                           font=("微软雅黑", 12), bg="DodgerBlue", relief="groove")
    hello_label.place(x=12, y=245)

    # 将日志保存到文件

    save_log_to_txt_button = tk.Button(main.window, text=config.lang_save_log_to_txt, width=39, height=1,
                                       font=("微软雅黑", 12), bg="DodgerBlue", relief="groove",
                                       command=lambda: launch_logger(log_text.get(index1="0.0", index2="end")))
    save_log_to_txt_button.place(x=12, y=527)


    # 本地调用的函数

    class local_func:
        def print_to_label_1(self: int, output_text: str):
            main.output_1.set(output_text)
            local_func.log_printer_encrypt(0, encrypt_1.input_place_1.get(), encrypt_1.input_key_1.get(), output_text)
            return 0

        def print_to_label_2(self: int, output_text: str):
            main.output_2.set(output_text)
            local_func.log_printer_decrypt(0, decrypt_1.input_place_2.get(), decrypt_1.input_key_2.get(), output_text)
            return 0

        def print_to_label_3(self: int, output_text: str):
            main.output_3.set(output_text)
            local_func.log_printer_encrypt(0, encrypt_2.input_place_3.get(), encrypt_2.input_key_3.get(), output_text)
            return 0

        def print_to_label_4(self: int, output_text: str):
            main.output_4.set(output_text)
            local_func.log_printer_decrypt(0, decrypt_2.input_place_4.get(), decrypt_2.input_key_4.get(), output_text)
            return 0

        def log_printer_encrypt(self: int, before_encrypt_text: str, key: str, after_encrypt_text: str):
            now_time = t.strftime("%Y-%m-%d %H:%M:%S")
            prefix = config.lang_info
            sign = config.lang_log_0
            message = (
                    sign + before_encrypt_text + "\n" + sign + "↓↓↓加密↓↓↓" + "\n" + sign + after_encrypt_text + "\n" + sign + "[秘钥=" + key + "]")
            print_text = (now_time + " " + prefix + "\n" + message + "\n\n")
            log_text.insert(index="end", chars=print_text)
            return 0

        def log_printer_decrypt(self: int, before_decrypt_text: str, key: str, after_decrypt_text: str):
            now_time = t.strftime("%Y-%m-%d %H:%M:%S")
            prefix = config.lang_info
            sign = config.lang_log_0
            message = (
                    sign + before_decrypt_text + "\n" + sign + "↓↓↓解密↓↓↓" + "\n" + sign + after_decrypt_text + "\n" + sign + "[秘钥=" + key + "]")
            print_text = (now_time + " " + prefix + "\n" + message + "\n\n")
            log_text.insert(index="end", chars=print_text)
            return 0


    main.lang_wait_for_input_1.set(config.lang_wait_for_input)
    main.lang_wait_for_input_2.set(config.lang_wait_for_input)
    main.lang_wait_for_input_3.set(config.lang_wait_for_input)
    main.lang_wait_for_input_4.set(config.lang_wait_for_input)
    main.lang_wait_for_key_1.set(config.lang_wait_for_key_1)
    main.lang_wait_for_key_2.set(config.lang_wait_for_key_1)
    main.lang_wait_for_key_3.set(config.lang_wait_for_key_2)
    main.lang_wait_for_key_4.set(config.lang_wait_for_key_2)

    # 事件判断

    main.window.focus()
    main.window.mainloop()
