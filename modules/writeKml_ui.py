# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'writeKml.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_writeKmlForm(object):
    def setupUi(self, writeKmlForm):
        if not writeKmlForm.objectName():
            writeKmlForm.setObjectName(u"writeKmlForm")
        writeKmlForm.resize(792, 305)
        writeKmlForm.setStyleSheet(u"QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));}\n"
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
"QLabel {\n"
"    background-color: #44"
                        "cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"\n"
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
        self.verticalLayout = QVBoxLayout(writeKmlForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(writeKmlForm)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.fileTypeCBox = QComboBox(writeKmlForm)
        self.fileTypeCBox.setObjectName(u"fileTypeCBox")

        self.horizontalLayout.addWidget(self.fileTypeCBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chosePathButton = QPushButton(writeKmlForm)
        self.chosePathButton.setObjectName(u"chosePathButton")

        self.horizontalLayout_2.addWidget(self.chosePathButton)

        self.filePathLEdit = QLineEdit(writeKmlForm)
        self.filePathLEdit.setObjectName(u"filePathLEdit")

        self.horizontalLayout_2.addWidget(self.filePathLEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(writeKmlForm)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.label_2 = QLabel(writeKmlForm)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.comboBox_5 = QComboBox(writeKmlForm)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.gridLayout.addWidget(self.comboBox_5, 3, 0, 1, 1)

        self.comboBox_3 = QComboBox(writeKmlForm)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout.addWidget(self.comboBox_3, 1, 1, 1, 1)

        self.label_5 = QLabel(writeKmlForm)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_7 = QLabel(writeKmlForm)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)

        self.label_6 = QLabel(writeKmlForm)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)

        self.comboBox_4 = QComboBox(writeKmlForm)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout.addWidget(self.comboBox_4, 1, 2, 1, 1)

        self.comboBox_2 = QComboBox(writeKmlForm)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 1, 0, 1, 1)

        self.label_3 = QLabel(writeKmlForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.comboBox_6 = QComboBox(writeKmlForm)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.gridLayout.addWidget(self.comboBox_6, 3, 1, 1, 1)

        self.comboBox_7 = QComboBox(writeKmlForm)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.gridLayout.addWidget(self.comboBox_7, 3, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.outFileButton = QPushButton(writeKmlForm)
        self.outFileButton.setObjectName(u"outFileButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outFileButton.sizePolicy().hasHeightForWidth())
        self.outFileButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.outFileButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.statusLabel = QLabel(writeKmlForm)
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


        self.retranslateUi(writeKmlForm)

        QMetaObject.connectSlotsByName(writeKmlForm)
    # setupUi

    def retranslateUi(self, writeKmlForm):
        writeKmlForm.setWindowTitle(QCoreApplication.translate("writeKmlForm", u"\u56fe\u5c42\u751f\u6210\u5668", None))
        self.label.setText(QCoreApplication.translate("writeKmlForm", u"\u9009\u62e9\u9700\u751f\u6210\u56fe\u5c42\u7c7b\u578b", None))
        self.chosePathButton.setText(QCoreApplication.translate("writeKmlForm", u"\u9009\u62e9\u8d44\u6e90\u6570\u636e", None))
        self.label_4.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("writeKmlForm", u"TextLabel", None))
        self.outFileButton.setText(QCoreApplication.translate("writeKmlForm", u"\u751f\u6210\u56fe\u5c42", None))
        self.statusLabel.setText("")
    # retranslateUi

