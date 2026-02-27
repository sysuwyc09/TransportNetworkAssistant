# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'site.ui'
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

class Ui_SiteAreaForm(object):
    def setupUi(self, SiteAreaForm):
        if not SiteAreaForm.objectName():
            SiteAreaForm.setObjectName(u"SiteAreaForm")
        SiteAreaForm.resize(516, 237)
        SiteAreaForm.setStyleSheet(u"QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));}\n"
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
        self.verticalLayout = QVBoxLayout(SiteAreaForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.selectKmlButton = QPushButton(SiteAreaForm)
        self.selectKmlButton.setObjectName(u"selectKmlButton")

        self.horizontalLayout.addWidget(self.selectKmlButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.kmlFilePathLE = QLineEdit(SiteAreaForm)
        self.kmlFilePathLE.setObjectName(u"kmlFilePathLE")

        self.verticalLayout.addWidget(self.kmlFilePathLE)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 250, -1)
        self.selectFileButton = QPushButton(SiteAreaForm)
        self.selectFileButton.setObjectName(u"selectFileButton")

        self.horizontalLayout_3.addWidget(self.selectFileButton)

        self.modFileButton = QPushButton(SiteAreaForm)
        self.modFileButton.setObjectName(u"modFileButton")

        self.horizontalLayout_3.addWidget(self.modFileButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.filePathLE = QLineEdit(SiteAreaForm)
        self.filePathLE.setObjectName(u"filePathLE")

        self.verticalLayout.addWidget(self.filePathLE)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.analysisButton = QPushButton(SiteAreaForm)
        self.analysisButton.setObjectName(u"analysisButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analysisButton.sizePolicy().hasHeightForWidth())
        self.analysisButton.setSizePolicy(sizePolicy)
        self.analysisButton.setMinimumSize(QSize(0, 40))
        self.analysisButton.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.analysisButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.statusLabel = QLabel(SiteAreaForm)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setStyleSheet(u"QLabel {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));\n"
"                color: #e0e5ec;          /* \u6d45\u7070\u767d\u8272\u6587\u5b57\uff0c\u9002\u914d\u6df1\u8272\u80cc\u666f */\n"
"                font-size: 12px;         /* \u57fa\u7840\u5b57\u53f7 */\n"
"                font-family: \"Microsoft YaHei\", Arial, sans-serif; /* \u6e05\u6670\u5b57\u4f53 */\n"
"                padding: 6px 8px;        /* \u5185\u8fb9\u8ddd\uff0c\u63d0\u5347\u53ef\u8bfb\u6027 */\n"
"            }")

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(SiteAreaForm)

        QMetaObject.connectSlotsByName(SiteAreaForm)
    # setupUi

    def retranslateUi(self, SiteAreaForm):
        SiteAreaForm.setWindowTitle(QCoreApplication.translate("SiteAreaForm", u"\u5730\u70b9\u5f52\u5c5e", None))
        self.selectKmlButton.setText(QCoreApplication.translate("SiteAreaForm", u"\u9009\u62e9\u76ee\u6807\u533a\u57df\u56fe\u5c42", None))
        self.selectFileButton.setText(QCoreApplication.translate("SiteAreaForm", u"\u9009\u62e9\u9700\u6c42\u6587\u4ef6", None))
        self.modFileButton.setText(QCoreApplication.translate("SiteAreaForm", u"\u6a21\u677f\u4e0b\u8f7d", None))
        self.analysisButton.setText(QCoreApplication.translate("SiteAreaForm", u"\u5730\u70b9\u4f4d\u7f6e\u5f52\u5c5e\u5206\u6790", None))
        self.statusLabel.setText("")
    # retranslateUi

