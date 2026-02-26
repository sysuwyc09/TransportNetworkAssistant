# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'convertCoord.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_ConvertCoordForm(object):
    def setupUi(self, ConvertCoordForm):
        if not ConvertCoordForm.objectName():
            ConvertCoordForm.setObjectName(u"ConvertCoordForm")
        ConvertCoordForm.resize(631, 434)
        ConvertCoordForm.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));")
        self.verticalLayout = QVBoxLayout(ConvertCoordForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame1 = QFrame(ConvertCoordForm)
        self.frame1.setObjectName(u"frame1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame1.sizePolicy().hasHeightForWidth())
        self.frame1.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.frame1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame1)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 30))
        self.label.setMaximumSize(QSize(100, 30))
        self.label.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.src_cb = QComboBox(self.frame1)
        self.src_cb.setObjectName(u"src_cb")
        self.src_cb.setMinimumSize(QSize(120, 30))
        self.src_cb.setMaximumSize(QSize(120, 30))
        self.src_cb.setStyleSheet(u"QComboBox {\n"
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
"}")

        self.horizontalLayout.addWidget(self.src_cb)


        self.verticalLayout.addWidget(self.frame1)

        self.frame2 = QFrame(ConvertCoordForm)
        self.frame2.setObjectName(u"frame2")
        sizePolicy.setHeightForWidth(self.frame2.sizePolicy().hasHeightForWidth())
        self.frame2.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.frame2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 30))
        self.label_2.setMaximumSize(QSize(100, 30))
        self.label_2.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.obj_cb = QComboBox(self.frame2)
        self.obj_cb.setObjectName(u"obj_cb")
        self.obj_cb.setMinimumSize(QSize(120, 30))
        self.obj_cb.setMaximumSize(QSize(120, 30))
        self.obj_cb.setStyleSheet(u"QComboBox {\n"
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
"}")

        self.horizontalLayout_2.addWidget(self.obj_cb)


        self.verticalLayout.addWidget(self.frame2)

        self.frame3 = QFrame(ConvertCoordForm)
        self.frame3.setObjectName(u"frame3")
        sizePolicy.setHeightForWidth(self.frame3.sizePolicy().hasHeightForWidth())
        self.frame3.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.frame3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 30))
        self.label_3.setMaximumSize(QSize(100, 30))
        self.label_3.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.src_coord_str_le = QLineEdit(self.frame3)
        self.src_coord_str_le.setObjectName(u"src_coord_str_le")
        self.src_coord_str_le.setMinimumSize(QSize(250, 30))
        self.src_coord_str_le.setMaximumSize(QSize(250, 30))
        self.src_coord_str_le.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")

        self.horizontalLayout_3.addWidget(self.src_coord_str_le)

        self.convert_bt = QPushButton(self.frame3)
        self.convert_bt.setObjectName(u"convert_bt")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.convert_bt.sizePolicy().hasHeightForWidth())
        self.convert_bt.setSizePolicy(sizePolicy1)
        self.convert_bt.setMinimumSize(QSize(100, 30))
        self.convert_bt.setMaximumSize(QSize(100, 30))
        self.convert_bt.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_3.addWidget(self.convert_bt)


        self.verticalLayout.addWidget(self.frame3)

        self.frame5 = QFrame(ConvertCoordForm)
        self.frame5.setObjectName(u"frame5")
        sizePolicy.setHeightForWidth(self.frame5.sizePolicy().hasHeightForWidth())
        self.frame5.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.frame5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.frame5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 30))
        self.label_4.setMaximumSize(QSize(100, 30))
        self.label_4.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.obj_coord_str_le = QLineEdit(self.frame5)
        self.obj_coord_str_le.setObjectName(u"obj_coord_str_le")
        self.obj_coord_str_le.setMinimumSize(QSize(250, 30))
        self.obj_coord_str_le.setMaximumSize(QSize(250, 30))
        self.obj_coord_str_le.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.obj_coord_str_le)


        self.verticalLayout.addWidget(self.frame5)

        self.frame4 = QFrame(ConvertCoordForm)
        self.frame4.setObjectName(u"frame4")
        sizePolicy.setHeightForWidth(self.frame4.sizePolicy().hasHeightForWidth())
        self.frame4.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.frame4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.chose_file_bt = QPushButton(self.frame4)
        self.chose_file_bt.setObjectName(u"chose_file_bt")
        sizePolicy1.setHeightForWidth(self.chose_file_bt.sizePolicy().hasHeightForWidth())
        self.chose_file_bt.setSizePolicy(sizePolicy1)
        self.chose_file_bt.setMinimumSize(QSize(100, 30))
        self.chose_file_bt.setMaximumSize(QSize(100, 30))
        self.chose_file_bt.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_5.addWidget(self.chose_file_bt)

        self.filepath_le = QLineEdit(self.frame4)
        self.filepath_le.setObjectName(u"filepath_le")
        self.filepath_le.setMinimumSize(QSize(250, 30))
        self.filepath_le.setMaximumSize(QSize(250, 30))
        self.filepath_le.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")

        self.horizontalLayout_5.addWidget(self.filepath_le)

        self.many_convert_bt = QPushButton(self.frame4)
        self.many_convert_bt.setObjectName(u"many_convert_bt")
        sizePolicy1.setHeightForWidth(self.many_convert_bt.sizePolicy().hasHeightForWidth())
        self.many_convert_bt.setSizePolicy(sizePolicy1)
        self.many_convert_bt.setMinimumSize(QSize(100, 30))
        self.many_convert_bt.setMaximumSize(QSize(100, 30))
        self.many_convert_bt.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_5.addWidget(self.many_convert_bt)


        self.verticalLayout.addWidget(self.frame4)

        self.textEdit = QTextEdit(ConvertCoordForm)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"QTextEdit {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"        padding: 5px;\n"
"        font-size: 12px;\n"
"    }\n"
"    \n"
"    QTextEdit:focus {\n"
"        border: 2px solid #44cc88;\n"
"    }\n"
"    \n"
"    QScrollBar:vertical {\n"
"        background: rgba(28, 33, 44, 255);\n"
"        width: 10px;\n"
"    }\n"
"    \n"
"    QScrollBar::handle:vertical {\n"
"        background: #44cc88;\n"
"        min-height: 20px;\n"
"    }")

        self.verticalLayout.addWidget(self.textEdit)


        self.retranslateUi(ConvertCoordForm)

        QMetaObject.connectSlotsByName(ConvertCoordForm)
    # setupUi

    def retranslateUi(self, ConvertCoordForm):
        ConvertCoordForm.setWindowTitle(QCoreApplication.translate("ConvertCoordForm", u"\u5750\u6807\u7cfb\u8f6c\u6362", None))
        self.label.setText(QCoreApplication.translate("ConvertCoordForm", u"\u6e90\u5750\u6807\u7cfb", None))
        self.label_2.setText(QCoreApplication.translate("ConvertCoordForm", u"\u76ee\u6807\u5750\u6807\u7cfb", None))
        self.label_3.setText(QCoreApplication.translate("ConvertCoordForm", u"\u7ecf\u5ea6 \u7eac\u5ea6", None))
        self.convert_bt.setText(QCoreApplication.translate("ConvertCoordForm", u"\u8f6c\u6362", None))
        self.label_4.setText(QCoreApplication.translate("ConvertCoordForm", u"\u8f6c\u6362\u540e\u5750\u6807", None))
        self.chose_file_bt.setText(QCoreApplication.translate("ConvertCoordForm", u"\u9009\u62e9\u6587\u4ef6", None))
        self.many_convert_bt.setText(QCoreApplication.translate("ConvertCoordForm", u"\u6279\u91cf\u8f6c\u6362", None))
    # retranslateUi

