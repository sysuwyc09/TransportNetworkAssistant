# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'olinkPageWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_OlinkPageWidget(object):
    def setupUi(self, olinkPageWidget):
        if not olinkPageWidget.objectName():
            olinkPageWidget.setObjectName(u"olinkPageWidget")
        self.verticalLayout_18 = QVBoxLayout(olinkPageWidget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.groupBox_3 = QGroupBox(olinkPageWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid #546391;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"    margin-top: 2ex; /* \u4e0a\u8fb9\u8ddd */\n"
"}\n"
"QGroupBox:title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \u6807\u9898\u4f4d\u7f6e */\n"
"    padding: 0 3px; /* \u5185\u8fb9\u8ddd */\n"
"    color: #FFFFFF; /* \u767d\u8272\u5b57\u4f53 */\n"
"    background-color: #546391;\n"
"	border-radius: 3px;\n"
"}")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.a_ne_le = QLineEdit(self.groupBox_3)
        self.a_ne_le.setObjectName(u"a_ne_le")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.a_ne_le.sizePolicy().hasHeightForWidth())
        self.a_ne_le.setSizePolicy(sizePolicy)
        self.a_ne_le.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.a_ne_le, 1, 0, 1, 1)

        self.a_ne_cb = QComboBox(self.groupBox_3)
        self.a_ne_cb.setObjectName(u"a_ne_cb")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.a_ne_cb.sizePolicy().hasHeightForWidth())
        self.a_ne_cb.setSizePolicy(sizePolicy1)
        self.a_ne_cb.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.a_ne_cb, 1, 1, 1, 1)

        self.z_ne_cb = QComboBox(self.groupBox_3)
        self.z_ne_cb.setObjectName(u"z_ne_cb")
        sizePolicy1.setHeightForWidth(self.z_ne_cb.sizePolicy().hasHeightForWidth())
        self.z_ne_cb.setSizePolicy(sizePolicy1)
        self.z_ne_cb.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.z_ne_cb, 1, 2, 1, 1)

        self.search_link_bt = QPushButton(self.groupBox_3)
        self.search_link_bt.setObjectName(u"search_link_bt")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.search_link_bt.sizePolicy().hasHeightForWidth())
        self.search_link_bt.setSizePolicy(sizePolicy2)
        self.search_link_bt.setMaximumSize(QSize(16777215, 30))
        self.search_link_bt.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	border: 2px solid #ff79c6;\n"
"}")

        self.gridLayout.addWidget(self.search_link_bt, 1, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setColumnStretch(3, 1)

        self.verticalLayout_17.addLayout(self.gridLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout.addWidget(self.label_11)

        self.olink_name_le = QLineEdit(self.groupBox_3)
        self.olink_name_le.setObjectName(u"olink_name_le")
        sizePolicy.setHeightForWidth(self.olink_name_le.sizePolicy().hasHeightForWidth())
        self.olink_name_le.setSizePolicy(sizePolicy)
        self.olink_name_le.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.olink_name_le)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout.addWidget(self.label_12)

        self.olink_text_te = QTextEdit(self.groupBox_3)
        self.olink_text_te.setObjectName(u"olink_text_te")

        self.verticalLayout.addWidget(self.olink_text_te)


        self.verticalLayout_17.addLayout(self.verticalLayout)


        self.verticalLayout_18.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(olinkPageWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid #546391;\n"
"    border-radius: 5px; /* \u5706\u89d2 */\n"
"    margin-top: 2ex; /* \u4e0a\u8fb9\u8ddd */\n"
"}\n"
"QGroupBox:title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \u6807\u9898\u4f4d\u7f6e */\n"
"    padding: 0 3px; /* \u5185\u8fb9\u8ddd */\n"
"    color: #FFFFFF; /* \u767d\u8272\u5b57\u4f53 */\n"
"    background-color: #546391;\n"
"	border-radius: 3px;\n"
"}")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet(u"font: bold 10pt '\u5fae\u8f6f\u96c5\u9ed1'; color: #6272a4;")

        self.horizontalLayout_9.addWidget(self.label_13)

        self.olink_key_le = QLineEdit(self.groupBox_4)
        self.olink_key_le.setObjectName(u"olink_key_le")
        sizePolicy.setHeightForWidth(self.olink_key_le.sizePolicy().hasHeightForWidth())
        self.olink_key_le.setSizePolicy(sizePolicy)
        self.olink_key_le.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_9.addWidget(self.olink_key_le)

        self.search_all_olink_bt = QPushButton(self.groupBox_4)
        self.search_all_olink_bt.setObjectName(u"search_all_olink_bt")
        sizePolicy2.setHeightForWidth(self.search_all_olink_bt.sizePolicy().hasHeightForWidth())
        self.search_all_olink_bt.setSizePolicy(sizePolicy2)
        self.search_all_olink_bt.setMaximumSize(QSize(16777215, 25))
        self.search_all_olink_bt.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	border: 2px solid #ff79c6;\n"
"}")

        self.horizontalLayout_9.addWidget(self.search_all_olink_bt)

        self.search_one_olink_bt = QPushButton(self.groupBox_4)
        self.search_one_olink_bt.setObjectName(u"search_one_olink_bt")
        sizePolicy2.setHeightForWidth(self.search_one_olink_bt.sizePolicy().hasHeightForWidth())
        self.search_one_olink_bt.setSizePolicy(sizePolicy2)
        self.search_one_olink_bt.setMaximumSize(QSize(16777215, 25))
        self.search_one_olink_bt.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	border: 2px solid #ff79c6;\n"
"}")

        self.horizontalLayout_9.addWidget(self.search_one_olink_bt)

        self.horizontalLayout_9.setStretch(1, 4)
        self.horizontalLayout_9.setStretch(2, 1)
        self.horizontalLayout_9.setStretch(3, 1)

        self.verticalLayout_16.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_34 = QLabel(self.groupBox_4)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setStyleSheet(u"font: bold 10pt '\u5fae\u8f6f\u96c5\u9ed1'; color: #6272a4;")

        self.horizontalLayout_23.addWidget(self.label_34)

        self.circuit_keys_le = QLineEdit(self.groupBox_4)
        self.circuit_keys_le.setObjectName(u"circuit_keys_le")
        sizePolicy.setHeightForWidth(self.circuit_keys_le.sizePolicy().hasHeightForWidth())
        self.circuit_keys_le.setSizePolicy(sizePolicy)
        self.circuit_keys_le.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_23.addWidget(self.circuit_keys_le)

        self.search_all_circuit_bt = QPushButton(self.groupBox_4)
        self.search_all_circuit_bt.setObjectName(u"search_all_circuit_bt")
        sizePolicy2.setHeightForWidth(self.search_all_circuit_bt.sizePolicy().hasHeightForWidth())
        self.search_all_circuit_bt.setSizePolicy(sizePolicy2)
        self.search_all_circuit_bt.setMaximumSize(QSize(16777215, 25))
        self.search_all_circuit_bt.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	border: 2px solid #ff79c6;\n"
"}")

        self.horizontalLayout_23.addWidget(self.search_all_circuit_bt)

        self.search_one_circuit_bt = QPushButton(self.groupBox_4)
        self.search_one_circuit_bt.setObjectName(u"search_one_circuit_bt")
        sizePolicy2.setHeightForWidth(self.search_one_circuit_bt.sizePolicy().hasHeightForWidth())
        self.search_one_circuit_bt.setSizePolicy(sizePolicy2)
        self.search_one_circuit_bt.setMaximumSize(QSize(16777215, 25))
        self.search_one_circuit_bt.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	border: 2px solid #ff79c6;\n"
"}")

        self.horizontalLayout_23.addWidget(self.search_one_circuit_bt)

        self.horizontalLayout_23.setStretch(1, 4)
        self.horizontalLayout_23.setStretch(2, 1)
        self.horizontalLayout_23.setStretch(3, 1)

        self.verticalLayout_16.addLayout(self.horizontalLayout_23)


        self.verticalLayout_18.addWidget(self.groupBox_4)

        self.verticalLayout_18.setStretch(0, 2)
        self.verticalLayout_18.setStretch(1, 1)

        self.retranslateUi(olinkPageWidget)

        QMetaObject.connectSlotsByName(olinkPageWidget)
    # setupUi

    def retranslateUi(self, olinkPageWidget):
        self.groupBox_3.setTitle(QCoreApplication.translate("OlinkPageWidget", u"\u5df2\u5173\u8054\u62d3\u6251\u8fde\u63a5\u5149\u8def", None))
        self.label_9.setText(QCoreApplication.translate("OlinkPageWidget", u"Z\u7aef\u7f51\u5143", None))
        self.search_link_bt.setText(QCoreApplication.translate("OlinkPageWidget", u"\u67e5\u8be2\u94fe\u8def", None))
        self.label_8.setText(QCoreApplication.translate("OlinkPageWidget", u"A\u7aef\u7f51\u5143", None))
        self.label_10.setText(QCoreApplication.translate("OlinkPageWidget", u"A\u7aef\u5173\u952e\u5b57", None))
        self.label_11.setText(QCoreApplication.translate("OlinkPageWidget", u"\u5149\u7535\u8def\u540d\u79f0", None))
        self.label_12.setText(QCoreApplication.translate("OlinkPageWidget", u"\u6587\u672c\u8def\u7531", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OlinkPageWidget", u"\u8d44\u6e90\u6a21\u7cca\u641c\u7d22", None))
        self.label_13.setText(QCoreApplication.translate("OlinkPageWidget", u"\u5149\u7ea4\u5149\u8def\uff1a", None))
        self.search_all_olink_bt.setText(QCoreApplication.translate("OlinkPageWidget", u"\u6a21\u7cca\u67e5\u8be2", None))
        self.search_one_olink_bt.setText(QCoreApplication.translate("OlinkPageWidget", u"\u7cbe\u51c6\u67e5\u8be2", None))
        self.label_34.setText(QCoreApplication.translate("OlinkPageWidget", u"\u4f20\u8f93\u7535\u8def\uff1a", None))
        self.search_all_circuit_bt.setText(QCoreApplication.translate("OlinkPageWidget", u"\u6a21\u7cca\u67e5\u8be2", None))
        self.search_one_circuit_bt.setText(QCoreApplication.translate("OlinkPageWidget", u"\u7cbe\u51c6\u67e5\u8be2", None))
        pass
    # retranslateUi

