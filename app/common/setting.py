# coding: utf-8
from pathlib import Path

# change DEBUG to False if you want to compile the code to exe
DEBUG = "__compiled__" not in globals()


YEAR = 2024
AUTHOR = "MangoFanFanw"
VERSION = "0.2.3"
APP_NAME = "FanTools"
HELP_URL = "https://ifanspace.top/"
REPO_URL = "https://github.com/mangofanfan/FanTools2"
FEEDBACK_URL = "https://github.com/mangofanfan/FanTools2/issues"
DOC_URL = "https://docs-fantools.mangofanfan.cn/"

CONFIG_FOLDER = Path('AppData').absolute()
CONFIG_FILE = CONFIG_FOLDER / "config.json"
