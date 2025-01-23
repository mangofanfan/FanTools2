from PySide6.QtCore import QObject
from qfluentwidgets import InfoBar, InfoBarPosition


class UpdateInfoBar(QObject):
    def update_true(self, _parent, version: str):
        """发现更新版本，需要更新。"""
        InfoBar.warning(
            title=self.tr("New Version Found"),
            content=self.tr("FanTools v{} can be updated now.").format(version),
            duration=4000,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=_parent,
        )
        return None

    def update_false(self, _parent, version: str):
        """当前版本已是最新，无需更新。"""
        InfoBar.success(
            title=self.tr("New Version Now"),
            content=self.tr("FanTools v{} is the latest version.").format(version),
            duration=4000,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=_parent,
        )
        return None