# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HeatMap.ui'
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
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_HeatForm(object):
    def setupUi(self, HeatForm):
        if not HeatForm.objectName():
            HeatForm.setObjectName(u"HeatForm")
        HeatForm.resize(521, 319)
        HeatForm.setStyleSheet(u"QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));}\n"
"QPushButton {\n"
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
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"                height: 6px;\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"                                           stop:0 rgba(60, 70, 85, 255), \n"
"                                           stop:1 rgba(80, 90, 105, 255));\n"
"           "
                        "     border-radius: 3px;\n"
"                margin: 0 10px;\n"
"            }\n"
"            QSlider::groove:vertical {\n"
"                width: 6px;\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, \n"
"                                           stop:0 rgba(60, 70, 85, 255), \n"
"                                           stop:1 rgba(80, 90, 105, 255));\n"
"                border-radius: 3px;\n"
"                margin: 10px 0;\n"
"            }\n"
"\n"
"            /* \u6ed1\u5757\u624b\u67c4\u90e8\u5206 */\n"
"            QSlider::handle:horizontal {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                           stop:0 rgba(100, 115, 135, 255), \n"
"                                           stop:1 rgba(80, 95, 115, 255));\n"
"                border: 1px solid rgba(120, 135, 155, 255);\n"
"                width: 20px;\n"
"                height: 20px;\n"
"                border-radius: 10px;\n"
"     "
                        "           margin: -7px 0; /* \u8d85\u51fa\u8f68\u9053\u4e0a\u4e0b\u65b9 */\n"
"            }\n"
"            QSlider::handle:vertical {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                           stop:0 rgba(100, 115, 135, 255), \n"
"                                           stop:1 rgba(80, 95, 115, 255));\n"
"                border: 1px solid rgba(120, 135, 155, 255);\n"
"                width: 20px;\n"
"                height: 20px;\n"
"                border-radius: 10px;\n"
"                margin: 0 -7px; /* \u8d85\u51fa\u8f68\u9053\u5de6\u53f3\u65b9 */\n"
"            }\n"
"\n"
"            /* \u624b\u67c4\u60ac\u505c\u72b6\u6001 */\n"
"            QSlider::handle:horizontal:hover, QSlider::handle:vertical:hover {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                           stop:0 rgba(120, 135, 155, 255), \n"
"                                           stop:1 r"
                        "gba(100, 115, 135, 255));\n"
"                border-color: rgba(140, 155, 175, 255);\n"
"            }\n"
"\n"
"            /* \u624b\u67c4\u6309\u4e0b\u72b6\u6001 */\n"
"            QSlider::handle:horizontal:pressed, QSlider::handle:vertical:pressed {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, \n"
"                                           stop:0 rgba(80, 95, 115, 255), \n"
"                                           stop:1 rgba(60, 75, 95, 255));\n"
"                border-color: rgba(100, 115, 135, 255);\n"
"            }\n"
"\n"
"            /* \u5df2\u6ed1\u52a8\u90e8\u5206\u7684\u586b\u5145\uff08\u53ef\u9009\uff09 */\n"
"            QSlider::sub-page:horizontal {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
"                                           stop:0 rgba(90, 105, 125, 255), \n"
"                                           stop:1 rgba(110, 125, 145, 255));\n"
"                border-radius: 3px;\n"
"            }"
                        "\n"
"            QSlider::sub-page:vertical {\n"
"                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, \n"
"                                           stop:0 rgba(90, 105, 125, 255), \n"
"                                           stop:1 rgba(110, 125, 145, 255));\n"
"                border-radius: 3px;\n"
"            }\n"
"")
        self.verticalLayout = QVBoxLayout(HeatForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.kmlButton = QPushButton(HeatForm)
        self.kmlButton.setObjectName(u"kmlButton")

        self.horizontalLayout_2.addWidget(self.kmlButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.kmlFilePathLE = QLineEdit(HeatForm)
        self.kmlFilePathLE.setObjectName(u"kmlFilePathLE")

        self.verticalLayout.addWidget(self.kmlFilePathLE)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.srcButton = QPushButton(HeatForm)
        self.srcButton.setObjectName(u"srcButton")

        self.horizontalLayout_3.addWidget(self.srcButton)

        self.modFileButton = QPushButton(HeatForm)
        self.modFileButton.setObjectName(u"modFileButton")

        self.horizontalLayout_3.addWidget(self.modFileButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.srcFilePathLE = QLineEdit(HeatForm)
        self.srcFilePathLE.setObjectName(u"srcFilePathLE")

        self.verticalLayout.addWidget(self.srcFilePathLE)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(HeatForm)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"	\n"
"	font: 10pt \"Microsoft YaHei UI\";\n"
"\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")

        self.horizontalLayout.addWidget(self.label)

        self.heatNumSlider = QSlider(HeatForm)
        self.heatNumSlider.setObjectName(u"heatNumSlider")
        self.heatNumSlider.setValue(20)
        self.heatNumSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.heatNumSlider)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.outFileButton = QPushButton(HeatForm)
        self.outFileButton.setObjectName(u"outFileButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outFileButton.sizePolicy().hasHeightForWidth())
        self.outFileButton.setSizePolicy(sizePolicy)
        self.outFileButton.setMinimumSize(QSize(0, 50))
        self.outFileButton.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_4.addWidget(self.outFileButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.statusLabel = QLabel(HeatForm)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy1)
        self.statusLabel.setMinimumSize(QSize(0, 30))
        self.statusLabel.setMaximumSize(QSize(16777215, 30))
        self.statusLabel.setStyleSheet(u"QLabel {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));\n"
"                color: #e0e5ec;          /* \u6d45\u7070\u767d\u8272\u6587\u5b57\uff0c\u9002\u914d\u6df1\u8272\u80cc\u666f */\n"
"                font-size: 12px;         /* \u57fa\u7840\u5b57\u53f7 */\n"
"                font-family: \"Microsoft YaHei\", Arial, sans-serif; /* \u6e05\u6670\u5b57\u4f53 */\n"
"                padding: 6px 8px;        /* \u5185\u8fb9\u8ddd\uff0c\u63d0\u5347\u53ef\u8bfb\u6027 */\n"
"            }")

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(HeatForm)

        QMetaObject.connectSlotsByName(HeatForm)
    # setupUi

    def retranslateUi(self, HeatForm):
        HeatForm.setWindowTitle(QCoreApplication.translate("HeatForm", u"\u70ed\u529b\u56fe\u751f\u6210\u5668", None))
        self.kmlButton.setText(QCoreApplication.translate("HeatForm", u"\u9009\u62e9\u533a\u57df\u56fe\u5c42", None))
        self.srcButton.setText(QCoreApplication.translate("HeatForm", u"\u9009\u62e9\u70ed\u529b\u6570\u636e", None))
        self.modFileButton.setText(QCoreApplication.translate("HeatForm", u"\u6a21\u677f\u4e0b\u8f7d", None))
        self.label.setText(QCoreApplication.translate("HeatForm", u"\u8bbe\u7f6e\u70ed\u529b\u70b9\u534a\u5f84\uff1a", None))
        self.outFileButton.setText(QCoreApplication.translate("HeatForm", u"\u751f\u6210\u70ed\u529b\u56fe", None))
        self.statusLabel.setText("")
    # retranslateUi

