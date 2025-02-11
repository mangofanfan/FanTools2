# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mango\PycharmProjects\FanTools2\app\tool\bilingualWriting\designer\dilingual_writing.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets

import qfluentwidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1125, 781)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(-1, 45, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.SingleDirectionScrollArea = SingleDirectionScrollArea(Form)
        self.SingleDirectionScrollArea.setWidgetResizable(True)
        self.SingleDirectionScrollArea.setObjectName("SingleDirectionScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 892, 337))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SimpleCardWidget = SimpleCardWidget(self.scrollAreaWidgetContents)
        self.SimpleCardWidget.setObjectName("SimpleCardWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.SimpleCardWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SubtitleLabel = SubtitleLabel(self.SimpleCardWidget)
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.horizontalLayout.addWidget(self.SubtitleLabel)
        self.LineEdit = LineEdit(self.SimpleCardWidget)
        self.LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit.setObjectName("LineEdit")
        self.horizontalLayout.addWidget(self.LineEdit)
        self.PrimaryToolButton = PrimaryToolButton(self.SimpleCardWidget)
        self.PrimaryToolButton.setObjectName("PrimaryToolButton")
        self.horizontalLayout.addWidget(self.PrimaryToolButton)
        self.verticalLayout.addWidget(self.SimpleCardWidget)
        self.SimpleCardWidget_NewParaHere = SimpleCardWidget(self.scrollAreaWidgetContents)
        self.SimpleCardWidget_NewParaHere.setObjectName("SimpleCardWidget_NewParaHere")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.SimpleCardWidget_NewParaHere)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SubtitleLabel_NewParaHere = SubtitleLabel(self.SimpleCardWidget_NewParaHere)
        self.SubtitleLabel_NewParaHere.setAlignment(QtCore.Qt.AlignCenter)
        self.SubtitleLabel_NewParaHere.setObjectName("SubtitleLabel_NewParaHere")
        self.horizontalLayout_2.addWidget(self.SubtitleLabel_NewParaHere)
        self.verticalLayout.addWidget(self.SimpleCardWidget_NewParaHere)
        spacerItem = QtWidgets.QSpacerItem(20, 193, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.SingleDirectionScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.SingleDirectionScrollArea, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SimpleCardWidget_Settings = SimpleCardWidget(Form)
        self.SimpleCardWidget_Settings.setMinimumSize(QtCore.QSize(200, 0))
        self.SimpleCardWidget_Settings.setObjectName("SimpleCardWidget_Settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.SimpleCardWidget_Settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SubtitleLabel_Settings = SubtitleLabel(self.SimpleCardWidget_Settings)
        self.SubtitleLabel_Settings.setObjectName("SubtitleLabel_Settings")
        self.verticalLayout_3.addWidget(self.SubtitleLabel_Settings)
        self.PushButton_Settings = PushButton(self.SimpleCardWidget_Settings)
        self.PushButton_Settings.setObjectName("PushButton_Settings")
        self.verticalLayout_3.addWidget(self.PushButton_Settings)
        self.verticalLayout_2.addWidget(self.SimpleCardWidget_Settings)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 3, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TextEdit = TextEdit(Form)
        self.TextEdit.setObjectName("TextEdit")
        self.horizontalLayout_3.addWidget(self.TextEdit)
        self.TextEdit_2 = TextEdit(Form)
        self.TextEdit_2.setObjectName("TextEdit_2")
        self.horizontalLayout_3.addWidget(self.TextEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.BodyLabel_TrAPI = BodyLabel(Form)
        self.BodyLabel_TrAPI.setObjectName("BodyLabel_TrAPI")
        self.horizontalLayout_4.addWidget(self.BodyLabel_TrAPI)
        self.ComboBox_TrAPI = qfluentwidgets.ComboBox(Form)
        self.ComboBox_TrAPI.setObjectName("ComboBox_TrAPI")
        self.horizontalLayout_4.addWidget(self.ComboBox_TrAPI)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SubtitleLabel.setText(_translate("Form", "Title"))
        self.SubtitleLabel_NewParaHere.setText(_translate("Form", "Subtitle label"))
        self.SubtitleLabel_Settings.setText(_translate("Form", "Subtitle label"))
        self.PushButton_Settings.setText(_translate("Form", "Push button"))
        self.BodyLabel_TrAPI.setText(_translate("Form", "Body label"))
from qfluentwidgets import BodyLabel, LineEdit, PrimaryToolButton, PushButton, SimpleCardWidget, SingleDirectionScrollArea, SubtitleLabel, TextEdit
