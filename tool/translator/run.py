# 翻译工具入口文件

if __name__ == "tool.translator.run":
    from .main import Main

    main = Main()
    main.showMainWindow()
    main.generateTestData()
