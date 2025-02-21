from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import SimpleCardWidget, SubtitleLabel, PushButton

from .language_file import PoFileObject


class ProjectCardWidget(SimpleCardWidget):

    openProjectSignal = Signal(PoFileObject)

    def __init__(self, parent, project: PoFileObject):
        super(ProjectCardWidget, self).__init__(parent)
        self._parent = parent
        self._poFileObject = project

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self.SubTitle_ProjectName = SubtitleLabel(project.getPoFileName())
        self._layout.addWidget(self.SubTitle_ProjectName)

        self.PushButton_OpenProject = PushButton(self.tr("Open Project"))
        self.PushButton_OpenProject.clicked.connect(self.openProject)
        self._layout.addWidget(self.PushButton_OpenProject)

    def openProject(self):
        self.openProjectSignal.emit(self._poFileObject)
