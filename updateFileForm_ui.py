# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updateFileForm.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_ImportFileForm(object):
    def setupUi(self, ImportFileForm):
        if not ImportFileForm.objectName():
            ImportFileForm.setObjectName(u"ImportFileForm")
        ImportFileForm.resize(659, 268)
        icon = QIcon()
        icon.addFile(u"icon/dataUpdate.ico", QSize(), QIcon.Normal, QIcon.Off)
        ImportFileForm.setWindowIcon(icon)
        ImportFileForm.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));")
        self.fileTypeCBox = QComboBox(ImportFileForm)
        self.fileTypeCBox.setObjectName(u"fileTypeCBox")
        self.fileTypeCBox.setGeometry(QRect(20, 30, 111, 27))
        self.importFileButton = QPushButton(ImportFileForm)
        self.importFileButton.setObjectName(u"importFileButton")
        self.importFileButton.setGeometry(QRect(530, 30, 111, 28))
        self.importFileButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(68, 204, 136);\n"
"	border: none;\n"
"	border-radius: 23;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(59, 173, 116);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: rgb(51, 150, 101);\n"
"}")
        self.importFileButton.setIcon(icon)
        self.importFileButton.setIconSize(QSize(24, 24))
        self.filePathLEdit = QLineEdit(ImportFileForm)
        self.filePathLEdit.setObjectName(u"filePathLEdit")
        self.filePathLEdit.setEnabled(True)
        self.filePathLEdit.setGeometry(QRect(140, 30, 261, 27))
        self.filePathLEdit.setReadOnly(True)
        self.chosePathButton = QPushButton(ImportFileForm)
        self.chosePathButton.setObjectName(u"chosePathButton")
        self.chosePathButton.setGeometry(QRect(410, 30, 111, 28))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chosePathButton.sizePolicy().hasHeightForWidth())
        self.chosePathButton.setSizePolicy(sizePolicy)
        self.chosePathButton.setMaximumSize(QSize(16777215, 46))
        self.chosePathButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(68, 204, 136);\n"
"	border: none;\n"
"	border-radius: 23;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(59, 173, 116);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: rgb(51, 150, 101);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"icon/packet.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.chosePathButton.setIcon(icon1)
        self.chosePathButton.setIconSize(QSize(20, 20))
        self.gridLayoutWidget = QWidget(ImportFileForm)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 80, 621, 143))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)

        self.comboBox_7 = QComboBox(self.gridLayoutWidget)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.gridLayout.addWidget(self.comboBox_7, 3, 2, 1, 1)

        self.comboBox_3 = QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout.addWidget(self.comboBox_3, 1, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)

        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)

        self.comboBox_8 = QComboBox(self.gridLayoutWidget)
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.gridLayout.addWidget(self.comboBox_8, 3, 3, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_11, 4, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_13, 4, 3, 1, 1)

        self.comboBox_6 = QComboBox(self.gridLayoutWidget)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.gridLayout.addWidget(self.comboBox_6, 3, 1, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 2, 3, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_12, 4, 2, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.comboBox_4 = QComboBox(self.gridLayoutWidget)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout.addWidget(self.comboBox_4, 1, 3, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)

        self.comboBox_5 = QComboBox(self.gridLayoutWidget)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.gridLayout.addWidget(self.comboBox_5, 3, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.comboBox_9 = QComboBox(self.gridLayoutWidget)
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.gridLayout.addWidget(self.comboBox_9, 5, 0, 1, 1)

        self.comboBox_10 = QComboBox(self.gridLayoutWidget)
        self.comboBox_10.setObjectName(u"comboBox_10")

        self.gridLayout.addWidget(self.comboBox_10, 5, 1, 1, 1)

        self.comboBox_11 = QComboBox(self.gridLayoutWidget)
        self.comboBox_11.setObjectName(u"comboBox_11")

        self.gridLayout.addWidget(self.comboBox_11, 5, 2, 1, 1)

        self.comboBox_12 = QComboBox(self.gridLayoutWidget)
        self.comboBox_12.setObjectName(u"comboBox_12")

        self.gridLayout.addWidget(self.comboBox_12, 5, 3, 1, 1)

        self.statusLabel = QLabel(ImportFileForm)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(20, 230, 621, 31))

        self.retranslateUi(ImportFileForm)

        QMetaObject.connectSlotsByName(ImportFileForm)
    # setupUi

    def retranslateUi(self, ImportFileForm):
        ImportFileForm.setWindowTitle(QCoreApplication.translate("ImportFileForm", u"\u66f4\u65b0\u7f13\u5b58\u6587\u4ef6", None))
        self.importFileButton.setText(QCoreApplication.translate("ImportFileForm", u" \u66f4\u65b0\u7f13\u5b58", None))
        self.chosePathButton.setText(QCoreApplication.translate("ImportFileForm", u" \u9009\u62e9\u6587\u4ef6", None))
        self.label_7.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_3.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_5.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_8.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_11.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_13.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_9.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_12.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_2.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_4.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_10.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.label_6.setText(QCoreApplication.translate("ImportFileForm", u"- -", None))
        self.statusLabel.setText("")
    # retranslateUi

