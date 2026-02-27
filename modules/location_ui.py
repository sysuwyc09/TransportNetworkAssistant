# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'location.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_LocationForm(object):
    def setupUi(self, LocationForm):
        if not LocationForm.objectName():
            LocationForm.setObjectName(u"LocationForm")
        LocationForm.resize(513, 273)
        icon = QIcon()
        icon.addFile(u"icon/search.ico", QSize(), QIcon.Normal, QIcon.Off)
        LocationForm.setWindowIcon(icon)
        LocationForm.setStyleSheet(u"QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));}\n"
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
"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"}\n"
"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #"
                        "44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(LocationForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(250, -1, -1, -1)
        self.label = QLabel(LocationForm)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.distanceLE = QLineEdit(LocationForm)
        self.distanceLE.setObjectName(u"distanceLE")

        self.horizontalLayout.addWidget(self.distanceLE)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 300, -1)
        self.srcButton = QPushButton(LocationForm)
        self.srcButton.setObjectName(u"srcButton")

        self.horizontalLayout_2.addWidget(self.srcButton)

        self.srcModButton = QPushButton(LocationForm)
        self.srcModButton.setObjectName(u"srcModButton")

        self.horizontalLayout_2.addWidget(self.srcModButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.srcFilePathLE = QLineEdit(LocationForm)
        self.srcFilePathLE.setObjectName(u"srcFilePathLE")

        self.verticalLayout.addWidget(self.srcFilePathLE)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 300, -1)
        self.objButton = QPushButton(LocationForm)
        self.objButton.setObjectName(u"objButton")

        self.horizontalLayout_3.addWidget(self.objButton)

        self.objModButton = QPushButton(LocationForm)
        self.objModButton.setObjectName(u"objModButton")

        self.horizontalLayout_3.addWidget(self.objModButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.objFilePathLE = QLineEdit(LocationForm)
        self.objFilePathLE.setObjectName(u"objFilePathLE")

        self.verticalLayout.addWidget(self.objFilePathLE)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.searchButton = QPushButton(LocationForm)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QSize(150, 40))
        self.searchButton.setMaximumSize(QSize(150, 40))

        self.horizontalLayout_4.addWidget(self.searchButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.statusLabel = QLabel(LocationForm)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setStyleSheet(u"QLabel {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));\n"
"                color: #e0e5ec;          /* \u6d45\u7070\u767d\u8272\u6587\u5b57\uff0c\u9002\u914d\u6df1\u8272\u80cc\u666f */\n"
"                font-size: 12px;         /* \u57fa\u7840\u5b57\u53f7 */\n"
"                font-family: \"Microsoft YaHei\", Arial, sans-serif; /* \u6e05\u6670\u5b57\u4f53 */\n"
"                padding: 6px 8px;        /* \u5185\u8fb9\u8ddd\uff0c\u63d0\u5347\u53ef\u8bfb\u6027 */\n"
"            }")

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(LocationForm)

        QMetaObject.connectSlotsByName(LocationForm)
    # setupUi

    def retranslateUi(self, LocationForm):
        LocationForm.setWindowTitle(QCoreApplication.translate("LocationForm", u"\u8d44\u6e90\u63a2\u9488", None))
        self.label.setText(QCoreApplication.translate("LocationForm", u"\u641c\u7d22\u8303\u56f4(\u5355\u4f4d\uff1a\u516c\u91cc)\uff1a", None))
        self.srcButton.setText(QCoreApplication.translate("LocationForm", u"\u9009\u62e9\u9700\u6c42\u70b9", None))
        self.srcModButton.setText(QCoreApplication.translate("LocationForm", u"\u9700\u6c42\u5e93\u6a21\u677f\u4e0b\u8f7d", None))
        self.objButton.setText(QCoreApplication.translate("LocationForm", u"\u9009\u62e9\u641c\u7d22\u5e93", None))
        self.objModButton.setText(QCoreApplication.translate("LocationForm", u"\u641c\u7d22\u5e93\u6a21\u677f\u4e0b\u8f7d", None))
        self.searchButton.setText(QCoreApplication.translate("LocationForm", u"\u8d44\u6e90\u641c\u7d22", None))
        self.statusLabel.setText("")
    # retranslateUi

