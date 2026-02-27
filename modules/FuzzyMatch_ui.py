# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FuzzyMatch.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_FuzzyMatchForm(object):
    def setupUi(self, FuzzyMatchForm):
        if not FuzzyMatchForm.objectName():
            FuzzyMatchForm.setObjectName(u"FuzzyMatchForm")
        FuzzyMatchForm.resize(514, 337)
        icon = QIcon()
        icon.addFile(u"icon/fuzzy.ico", QSize(), QIcon.Normal, QIcon.Off)
        FuzzyMatchForm.setWindowIcon(icon)
        FuzzyMatchForm.setStyleSheet(u"QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));}\n"
"QPushButton {\n"
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
"}\n"
"QComboBox {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #55dd99;\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    selection-background-color: rgba(68, 204, 136, 0.3);\n"
"}\n"
"\n"
"QLabel {\n"
"    background-color"
                        ": #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"}\n"
"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(FuzzyMatchForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(250, -1, -1, -1)
        self.label = QLabel(FuzzyMatchForm)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.fuzzyTypeCBox = QComboBox(FuzzyMatchForm)
        self.fuzzyTypeCBox.setObjectName(u"fuzzyTypeCBox")

        self.horizontalLayout.addWidget(self.fuzzyTypeCBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.srcFileButton = QPushButton(FuzzyMatchForm)
        self.srcFileButton.setObjectName(u"srcFileButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srcFileButton.sizePolicy().hasHeightForWidth())
        self.srcFileButton.setSizePolicy(sizePolicy)
        self.srcFileButton.setMinimumSize(QSize(100, 25))
        self.srcFileButton.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_2.addWidget(self.srcFileButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.srcFilePathLE = QLineEdit(FuzzyMatchForm)
        self.srcFilePathLE.setObjectName(u"srcFilePathLE")

        self.verticalLayout.addWidget(self.srcFilePathLE)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.objFileButton = QPushButton(FuzzyMatchForm)
        self.objFileButton.setObjectName(u"objFileButton")
        sizePolicy.setHeightForWidth(self.objFileButton.sizePolicy().hasHeightForWidth())
        self.objFileButton.setSizePolicy(sizePolicy)
        self.objFileButton.setMinimumSize(QSize(100, 25))
        self.objFileButton.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_3.addWidget(self.objFileButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.objFilePathLE = QLineEdit(FuzzyMatchForm)
        self.objFilePathLE.setObjectName(u"objFilePathLE")

        self.verticalLayout.addWidget(self.objFilePathLE)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(FuzzyMatchForm)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.notMatchStrLE = QLineEdit(FuzzyMatchForm)
        self.notMatchStrLE.setObjectName(u"notMatchStrLE")

        self.verticalLayout.addWidget(self.notMatchStrLE)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.fuzzyButton = QPushButton(FuzzyMatchForm)
        self.fuzzyButton.setObjectName(u"fuzzyButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fuzzyButton.sizePolicy().hasHeightForWidth())
        self.fuzzyButton.setSizePolicy(sizePolicy1)
        self.fuzzyButton.setMinimumSize(QSize(150, 40))
        self.fuzzyButton.setMaximumSize(QSize(150, 40))

        self.horizontalLayout_4.addWidget(self.fuzzyButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.statusLabel = QLabel(FuzzyMatchForm)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setStyleSheet(u"QLabel {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));\n"
"                color: #e0e5ec;          /* \u6d45\u7070\u767d\u8272\u6587\u5b57\uff0c\u9002\u914d\u6df1\u8272\u80cc\u666f */\n"
"                font-size: 12px;         /* \u57fa\u7840\u5b57\u53f7 */\n"
"                font-family: \"Microsoft YaHei\", Arial, sans-serif; /* \u6e05\u6670\u5b57\u4f53 */\n"
"                padding: 6px 8px;        /* \u5185\u8fb9\u8ddd\uff0c\u63d0\u5347\u53ef\u8bfb\u6027 */\n"
"            }")

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(FuzzyMatchForm)

        QMetaObject.connectSlotsByName(FuzzyMatchForm)
    # setupUi

    def retranslateUi(self, FuzzyMatchForm):
        FuzzyMatchForm.setWindowTitle(QCoreApplication.translate("FuzzyMatchForm", u"\u6a21\u7cca\u5339\u914d", None))
        self.label.setText(QCoreApplication.translate("FuzzyMatchForm", u"\u9009\u62e9\u6a21\u7cca\u5339\u914d\u7c7b\u578b\uff1a", None))
        self.srcFileButton.setText(QCoreApplication.translate("FuzzyMatchForm", u"\u9009\u62e9\u9700\u6c42\u6587\u4ef6", None))
        self.objFileButton.setText(QCoreApplication.translate("FuzzyMatchForm", u"\u9009\u62e9\u5339\u914d\u5e93", None))
        self.label_2.setText(QCoreApplication.translate("FuzzyMatchForm", u"\u5254\u9664\u5339\u914d\u7684\u5b57\u7b26\u4e32\uff0c\u987f\u53f7\u201c\u3001\u201d\u9694\u5f00\uff1a", None))
        self.fuzzyButton.setText(QCoreApplication.translate("FuzzyMatchForm", u"\u6a21\u7cca\u5339\u914d", None))
        self.statusLabel.setText("")
    # retranslateUi

