﻿import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

if __name__ == '__main__':
    from Main_with_Window import launch
    try:
        launch()
    except Exception as e:
        print("ERROR!!!!!")
        print(e)