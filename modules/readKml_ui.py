# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'readKml.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ReadKmlForm(object):
    def setupUi(self, ReadKmlForm):
        if not ReadKmlForm.objectName():
            ReadKmlForm.setObjectName(u"ReadKmlForm")
        ReadKmlForm.resize(559, 325)
        ReadKmlForm.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));")
        self.verticalLayout_3 = QVBoxLayout(ReadKmlForm)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(ReadKmlForm)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.selectKmlButton = QPushButton(self.frame)
        self.selectKmlButton.setObjectName(u"selectKmlButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.selectKmlButton.sizePolicy().hasHeightForWidth())
        self.selectKmlButton.setSizePolicy(sizePolicy1)
        self.selectKmlButton.setMinimumSize(QSize(0, 30))
        self.selectKmlButton.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamilies([u"\u6977\u4f53"])
        font.setPointSize(10)
        font.setBold(False)
        self.selectKmlButton.setFont(font)
        self.selectKmlButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(40, 45, 56, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 25, 36, 255);\n"
"}")

        self.verticalLayout.addWidget(self.selectKmlButton)

        self.kmlPathLabel = QLabel(self.frame)
        self.kmlPathLabel.setObjectName(u"kmlPathLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.kmlPathLabel.sizePolicy().hasHeightForWidth())
        self.kmlPathLabel.setSizePolicy(sizePolicy2)
        self.kmlPathLabel.setMinimumSize(QSize(0, 30))
        self.kmlPathLabel.setMaximumSize(QSize(16777215, 30))
        self.kmlPathLabel.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.kmlPathLabel)


        self.verticalLayout_3.addWidget(self.frame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(ReadKmlForm)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setMaximumSize(QSize(16777215, 150))
        self.frame_2.setStyleSheet(u"border: 1px solid #44cc88;")
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pointCheckBox = QCheckBox(self.frame_2)
        self.pointCheckBox.setObjectName(u"pointCheckBox")
        self.pointCheckBox.setMinimumSize(QSize(0, 30))
        self.pointCheckBox.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setFamilies([u"\u6977\u4f53"])
        font1.setPointSize(11)
        self.pointCheckBox.setFont(font1)
        self.pointCheckBox.setStyleSheet(u"QCheckBox{color:#44cc88}\n"
"")
        self.pointCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.pointCheckBox)

        self.lineCheckBox = QCheckBox(self.frame_2)
        self.lineCheckBox.setObjectName(u"lineCheckBox")
        self.lineCheckBox.setMinimumSize(QSize(0, 30))
        self.lineCheckBox.setMaximumSize(QSize(16777215, 30))
        self.lineCheckBox.setFont(font1)
        self.lineCheckBox.setStyleSheet(u"QCheckBox{color:#44cc88}\n"
"")
        self.lineCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.lineCheckBox)

        self.polyCheckBox = QCheckBox(self.frame_2)
        self.polyCheckBox.setObjectName(u"polyCheckBox")
        self.polyCheckBox.setMinimumSize(QSize(0, 30))
        self.polyCheckBox.setMaximumSize(QSize(16777215, 30))
        self.polyCheckBox.setFont(font1)
        self.polyCheckBox.setStyleSheet(u"QCheckBox{color:#44cc88}\n"
"")
        self.polyCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.polyCheckBox)


        self.horizontalLayout.addWidget(self.frame_2)

        self.readKmlButton = QPushButton(ReadKmlForm)
        self.readKmlButton.setObjectName(u"readKmlButton")
        self.readKmlButton.setMinimumSize(QSize(0, 40))
        self.readKmlButton.setMaximumSize(QSize(16777215, 40))
        self.readKmlButton.setFont(font1)
        self.readKmlButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 10px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(40, 45, 56, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 25, 36, 255);\n"
"}")

        self.horizontalLayout.addWidget(self.readKmlButton)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.progressBar = QProgressBar(ReadKmlForm)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.verticalLayout_3.addWidget(self.progressBar)

        self.stateLabel = QLabel(ReadKmlForm)
        self.stateLabel.setObjectName(u"stateLabel")
        sizePolicy.setHeightForWidth(self.stateLabel.sizePolicy().hasHeightForWidth())
        self.stateLabel.setSizePolicy(sizePolicy)
        self.stateLabel.setMinimumSize(QSize(0, 30))
        self.stateLabel.setMaximumSize(QSize(16777215, 30))
        self.stateLabel.setAutoFillBackground(False)
        self.stateLabel.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_3.addWidget(self.stateLabel)

        self.verticalLayout_3.setStretch(1, 5)

        self.retranslateUi(ReadKmlForm)

        QMetaObject.connectSlotsByName(ReadKmlForm)
    # setupUi

    def retranslateUi(self, ReadKmlForm):
        ReadKmlForm.setWindowTitle(QCoreApplication.translate("ReadKmlForm", u"\u89e3\u6790\u8c37\u6b4c\u56fe\u5c42", None))
        self.selectKmlButton.setText(QCoreApplication.translate("ReadKmlForm", u"\u9009\u62e9KML\u56fe\u5c42\u6587\u4ef6", None))
        self.kmlPathLabel.setText("")
        self.pointCheckBox.setText(QCoreApplication.translate("ReadKmlForm", u"\u6807\u8bb0\u8d44\u6e90", None))
        self.lineCheckBox.setText(QCoreApplication.translate("ReadKmlForm", u"\u8def\u5f84\u8d44\u6e90", None))
        self.polyCheckBox.setText(QCoreApplication.translate("ReadKmlForm", u"\u591a\u8fb9\u5f62\u8d44\u6e90", None))
        self.readKmlButton.setText(QCoreApplication.translate("ReadKmlForm", u"\u5f00\u59cb\u89e3\u6790", None))
        self.stateLabel.setText("")
    # retranslateUi

