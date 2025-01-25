# 工具箱版本记录

## 下一个版本：0.2.2

**（计划）将要包含的新特性**

* [X] **日志系统** - 工具箱将在运行时输出日志，以更好地实现运行情况记录与问题诊断。
    - 尽管工具箱本体的未来目标是多语言，但日志系统的输出始终会是中文。
* [X] **关于页面增加更多功能** - 增加连接至工具箱发布页、GitHub仓库、工具箱文档等地的链接，增加打开数据目录的按钮（用于查看日志等）。
* [ ] **接入一言功能** - 重构旧版工具箱中实现的一言API功能。

**问题修复**

* [X] 来自上游的窗口问题，参见`0.2.1`的已知问题。

## 当前主要版本：0.2.1

**包含的新特性**

* **启动时版本检查** - 实现了简陋的启动时版本检查功能，可在设置中开启，检查结果会在工具箱主窗口中提醒并记录在日志中。
    - 未来计划实现自动下载新版本的安装程序。
* **新闻** - 实现了简陋的工具箱新闻功能，相当简陋。 

**已知问题**

* **来自上游的窗口问题** - 参见[我提的issue](https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/178)，在开发环境Python3.11下存在窗口最大化与缩小时缺失动画以及相关的一系列问题，由于并非严重问题，等待上游修复。
    - 已经确定降级PySide6版本（6.8.1.1->6.7.2）能够规避该问题，将在工具箱`0.2.2`中规避问题。
    - 已经确定是PySide6 6.8.1的问题，上游等待PySide6修复。

**下载**

安装程序下载链接：[https://file.mangofanfan.cn/s/1nehnw](https://file.mangofanfan.cn/s/1nehnw)

## 0.2.0

工具箱在此版本完全重构，但此版本并未分发。重构后的首个分发版本是0.2.1。

**包含的新特性**

**完全重构这个特性还不够多嘛？**

由于重构需要，暂时移除了下载工具与翻译工具，将在日后基于重构版工具箱重新实现。

## 0.1.0、0.0.0与0.0.1

中道崩殂的版本。从`0.0.1`向`0.1.0`的迈进是极其痛苦的，以至于最终`0.1.0`被直接放弃。

0.0.0与0.0.1版本的更新记录请参见下列地址：

* https://ifanspace.top/2024/08/28/510.html （完整）
* https://github.com/mangofanfan/FanTools/releases/ （只有这两个版本）

**下载** （仅供考古娱乐使用，不再维护，也不再接受任何issue）

* 命令行安装工具-0.0.1：[https://file.mangofanfan.cn/s/5awxmv](https://file.mangofanfan.cn/s/5awxmv)
* 芒果工具箱本体-0.0.1：[https://file.mangofanfan.cn/s/gx0vjp](https://file.mangofanfan.cn/s/gx0vjp)
* 命令行安装工具-0.0.0：[https://file.mangofanfan.cn/s/4aiaby](https://file.mangofanfan.cn/s/4aiaby)
* 芒果工具箱本体-0.0.0：[https://file.mangofanfan.cn/s/kmpnbp](https://file.mangofanfan.cn/s/kmpnbp)