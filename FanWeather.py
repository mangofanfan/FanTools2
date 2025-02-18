# 这里是程序入口。

import sys

if __name__ == "__main__":
    if "-test" in sys.argv:
        import main_dev
    else:
        import main
