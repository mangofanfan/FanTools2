# 这里是程序入口。

import dotenv
import os
import sys

if __name__ == "__main__":
    if "-test" in sys.argv:
        dotenv.load_dotenv()
        if proLicense := os.getenv("QFLUENTWIDGETS_PRO_LICENSE"):
            # 如果您有 QFluentWidgets Pro 的许可证，在此文件同目录下创建 `.env` 文件，将许可证填写为环境变量，即可将其设置。
            # 这样就可以跳过登录窗口来测试使用 Pro 组件的工具了。
            # 不创建 `.env` 文件并不影响测试模式启动，工具箱本体仍然可以被测试。
            from qfluentwidgetspro import setLicense
            setLicense(proLicense)
        import main_dev
    else:
        import main
