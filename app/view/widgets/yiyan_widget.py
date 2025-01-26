from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import ElevatedCardWidget, BodyLabel, StrongBodyLabel

from ...common.hitokoto import HitokotoManager
from ...common.signal_bus import signalBus


class YiYanCard(ElevatedCardWidget):
    def __init__(self):
        super().__init__()
        self.viewLayout = QVBoxLayout()
        self.viewLayout.setContentsMargins(32, 12, 32, 12)
        self.setLayout(self.viewLayout)

        self.bodyLabel = BodyLabel()
        self.strongBodyLabel = StrongBodyLabel()
        self.strongBodyLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.viewLayout.addWidget(self.bodyLabel)
        self.viewLayout.addWidget(self.strongBodyLabel)

        self.hm = HitokotoManager()
        signalBus.hitokotoUpdate.connect(self._update)
        self.clicked.connect(signalBus.hitokotoStartUpdate)

        self._update()

    def _update(self) -> None:
        self.bodyLabel.setText(self.hm.hitokoto.text)
        self.strongBodyLabel.setText(self.hm.hitokoto.by)
        return None
