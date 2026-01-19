# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

from customnWidget import (OltBoardView, PieChartView, TopologyView)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 650)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(1000, 650))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QSize(1000, 700))
        self.centralwidget.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.236422 rgba(28, 33, 44, 255), stop:0.760383 rgba(41, 48, 60, 255));")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.root = QFrame(self.centralwidget)
        self.root.setObjectName(u"root")
        sizePolicy.setHeightForWidth(self.root.sizePolicy().hasHeightForWidth())
        self.root.setSizePolicy(sizePolicy)
        self.root.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
"border: none;")
        self.root.setFrameShape(QFrame.NoFrame)
        self.root.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.root)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.titleBar = QFrame(self.root)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setMinimumSize(QSize(1000, 60))
        self.titleBar.setMaximumSize(QSize(1000, 60))
        self.titleBar.setFrameShape(QFrame.NoFrame)
        self.titleBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.titleBar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 6, 10, 0)
        self.frame = QFrame(self.titleBar)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(250, 0))
        self.frame.setMaximumSize(QSize(250, 16777215))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 40))
        self.pushButton.setMaximumSize(QSize(40, 40))
        self.pushButton.setStyleSheet(u"border: none;")
        icon = QIcon()
        icon.addFile(u":/icons/assets/logo.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(45, 45))

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)


        self.horizontalLayout_2.addWidget(self.frame)

        self.horizontalSpacer = QSpacerItem(364, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.frame_2 = QFrame(self.titleBar)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(300, 0))
        self.frame_2.setStyleSheet(u"border: none;\n"
"")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.homeBtn = QPushButton(self.frame_2)
        self.homeBtn.setObjectName(u"homeBtn")
        self.homeBtn.setMinimumSize(QSize(95, 0))
        self.homeBtn.setMaximumSize(QSize(95, 16777215))
        font = QFont()
        font.setBold(True)
        self.homeBtn.setFont(font)
        self.homeBtn.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	border: none;\n"
"	color: rgb(199, 199, 199);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	color: rgb(147, 147, 147);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.homeBtn.setIcon(icon1)
        self.homeBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.homeBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.menuBtn = QPushButton(self.frame_2)
        self.menuBtn.setObjectName(u"menuBtn")
        self.menuBtn.setMinimumSize(QSize(60, 0))
        self.menuBtn.setMaximumSize(QSize(60, 16777215))
        self.menuBtn.setFont(font)
        self.menuBtn.setStyleSheet(u"QPushButton {\n"
"	text-align: left;\n"
"	border: none;\n"
"	color: rgb(199, 199, 199);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	color: rgb(147, 147, 147);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/assets/menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menuBtn.setIcon(icon2)
        self.menuBtn.setIconSize(QSize(18, 18))

        self.horizontalLayout_4.addWidget(self.menuBtn)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.miniBtn = QPushButton(self.frame_2)
        self.miniBtn.setObjectName(u"miniBtn")
        self.miniBtn.setMinimumSize(QSize(26, 26))
        self.miniBtn.setMaximumSize(QSize(26, 26))
        self.miniBtn.setStyleSheet(u"QPushButton {\n"
"	background-color:rgb(97, 97, 97);\n"
"	border: none;\n"
"	border-radius: 13;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(134, 134, 134);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(0, 0, 0);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/assets/minus (2).svg", QSize(), QIcon.Normal, QIcon.Off)
        self.miniBtn.setIcon(icon3)
        self.miniBtn.setIconSize(QSize(22, 22))

        self.horizontalLayout_4.addWidget(self.miniBtn)

        self.closeBtn = QPushButton(self.frame_2)
        self.closeBtn.setObjectName(u"closeBtn")
        self.closeBtn.setMinimumSize(QSize(26, 26))
        self.closeBtn.setMaximumSize(QSize(26, 26))
        self.closeBtn.setStyleSheet(u"QPushButton {\n"
"	background-color:rgb(97, 97, 97);\n"
"	border: none;\n"
"	border-radius: 13;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(134, 134, 134);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(0, 0, 0);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/assets/close (3).svg", QSize(), QIcon.Normal, QIcon.Off)
        self.closeBtn.setIcon(icon4)
        self.closeBtn.setIconSize(QSize(22, 22))

        self.horizontalLayout_4.addWidget(self.closeBtn)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.titleBar)

        self.container = QStackedWidget(self.root)
        self.container.setObjectName(u"container")
        sizePolicy.setHeightForWidth(self.container.sizePolicy().hasHeightForWidth())
        self.container.setSizePolicy(sizePolicy)
        self.container.setMinimumSize(QSize(1000, 550))
        self.container.setMaximumSize(QSize(1000, 550))
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setFrameShadow(QFrame.Raised)
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.homePage.setMaximumSize(QSize(1000, 550))
        self.verticalLayout_2 = QVBoxLayout(self.homePage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.headers = QFrame(self.homePage)
        self.headers.setObjectName(u"headers")
        self.headers.setMaximumSize(QSize(16777215, 120))
        self.headers.setStyleSheet(u"")
        self.headers.setFrameShape(QFrame.NoFrame)
        self.headers.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.headers)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(213, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.label_2 = QLabel(self.headers)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(200, 0))
        self.label_2.setMaximumSize(QSize(400, 16777215))

        self.horizontalLayout_5.addWidget(self.label_2)

        self.horizontalSpacer_5 = QSpacerItem(213, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addWidget(self.headers)

        self.title = QFrame(self.homePage)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 30))
        self.title.setMaximumSize(QSize(16777215, 30))
        self.title.setStyleSheet(u"")
        self.title.setFrameShape(QFrame.NoFrame)
        self.title.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.title)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(27, 0, 0, 0)
        self.label_3 = QLabel(self.title)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_6.addWidget(self.label_3)

        self.horizontalSpacer_6 = QSpacerItem(270, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.label_4 = QLabel(self.title)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.horizontalSpacer_7 = QSpacerItem(267, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addWidget(self.title)

        self.cards = QFrame(self.homePage)
        self.cards.setObjectName(u"cards")
        self.cards.setStyleSheet(u"")
        self.cards.setFrameShape(QFrame.NoFrame)
        self.cards.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.cards)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.card1 = QFrame(self.cards)
        self.card1.setObjectName(u"card1")
        self.card1.setMinimumSize(QSize(160, 210))
        self.card1.setMaximumSize(QSize(160, 210))
        self.card1.setStyleSheet(u"background-color: rgb(58, 65, 82);\n"
"border-radius: 15;")
        self.card1.setFrameShape(QFrame.NoFrame)
        self.card1.setFrameShadow(QFrame.Raised)
        self.card1.setLineWidth(5)
        self.verticalLayout_4 = QVBoxLayout(self.card1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.card1)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(150, 120))
        self.frame_4.setMaximumSize(QSize(150, 120))
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.outsideBtn = QPushButton(self.frame_4)
        self.outsideBtn.setObjectName(u"outsideBtn")
        self.outsideBtn.setMinimumSize(QSize(80, 80))
        self.outsideBtn.setMaximumSize(QSize(80, 80))
        icon5 = QIcon()
        icon5.addFile(u":/icons/assets/america.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.outsideBtn.setIcon(icon5)
        self.outsideBtn.setIconSize(QSize(60, 60))

        self.verticalLayout_3.addWidget(self.outsideBtn, 0, Qt.AlignHCenter)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.label_5, 0, Qt.AlignHCenter)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        font1.setPointSize(8)
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"text-align: center;")

        self.verticalLayout_3.addWidget(self.label_6, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addWidget(self.frame_4, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_7.addWidget(self.card1)

        self.card2 = QFrame(self.cards)
        self.card2.setObjectName(u"card2")
        self.card2.setMinimumSize(QSize(160, 210))
        self.card2.setMaximumSize(QSize(160, 210))
        self.card2.setStyleSheet(u"background-color: rgb(58, 65, 82);\n"
"border-radius: 15;")
        self.card2.setFrameShape(QFrame.NoFrame)
        self.card2.setFrameShadow(QFrame.Raised)
        self.card2.setLineWidth(5)
        self.verticalLayout_5 = QVBoxLayout(self.card2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.card2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(150, 120))
        self.frame_6.setMaximumSize(QSize(150, 120))
        self.frame_6.setStyleSheet(u"")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.insideBtn = QPushButton(self.frame_6)
        self.insideBtn.setObjectName(u"insideBtn")
        self.insideBtn.setMinimumSize(QSize(80, 80))
        self.insideBtn.setMaximumSize(QSize(80, 80))
        icon6 = QIcon()
        icon6.addFile(u":/icons/assets/router.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.insideBtn.setIcon(icon6)
        self.insideBtn.setIconSize(QSize(60, 60))

        self.verticalLayout_6.addWidget(self.insideBtn, 0, Qt.AlignHCenter)

        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.verticalLayout_6.addWidget(self.label_7, 0, Qt.AlignHCenter)

        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setStyleSheet(u"text-align: center;")

        self.verticalLayout_6.addWidget(self.label_8, 0, Qt.AlignHCenter)


        self.verticalLayout_5.addWidget(self.frame_6, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_7.addWidget(self.card2)

        self.horizontalSpacer_8 = QSpacerItem(25, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)

        self.card3 = QFrame(self.cards)
        self.card3.setObjectName(u"card3")
        self.card3.setMinimumSize(QSize(160, 210))
        self.card3.setMaximumSize(QSize(160, 210))
        self.card3.setStyleSheet(u"background-color: rgb(58, 65, 82);\n"
"border-radius: 15;")
        self.card3.setFrameShape(QFrame.NoFrame)
        self.card3.setFrameShadow(QFrame.Raised)
        self.card3.setLineWidth(5)
        self.verticalLayout_9 = QVBoxLayout(self.card3)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.card3)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(150, 120))
        self.frame_10.setMaximumSize(QSize(150, 120))
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.odevBtn = QPushButton(self.frame_10)
        self.odevBtn.setObjectName(u"odevBtn")
        self.odevBtn.setMinimumSize(QSize(80, 80))
        self.odevBtn.setMaximumSize(QSize(80, 80))
        icon7 = QIcon()
        icon7.addFile(u":/icons/assets/box.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.odevBtn.setIcon(icon7)
        self.odevBtn.setIconSize(QSize(60, 60))

        self.verticalLayout_10.addWidget(self.odevBtn, 0, Qt.AlignHCenter)

        self.label_11 = QLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.verticalLayout_10.addWidget(self.label_11, 0, Qt.AlignHCenter)

        self.label_12 = QLabel(self.frame_10)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)
        self.label_12.setStyleSheet(u"text-align: center;")

        self.verticalLayout_10.addWidget(self.label_12, 0, Qt.AlignHCenter)


        self.verticalLayout_9.addWidget(self.frame_10, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_7.addWidget(self.card3)

        self.card4 = QFrame(self.cards)
        self.card4.setObjectName(u"card4")
        self.card4.setMinimumSize(QSize(160, 210))
        self.card4.setMaximumSize(QSize(160, 210))
        self.card4.setStyleSheet(u"background-color: rgb(58, 65, 82);\n"
"border-radius: 15;")
        self.card4.setFrameShape(QFrame.NoFrame)
        self.card4.setFrameShadow(QFrame.Raised)
        self.card4.setLineWidth(5)
        self.verticalLayout_11 = QVBoxLayout(self.card4)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.card4)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(150, 120))
        self.frame_12.setMaximumSize(QSize(150, 120))
        self.frame_12.setStyleSheet(u"")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_12)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.oltBtn = QPushButton(self.frame_12)
        self.oltBtn.setObjectName(u"oltBtn")
        self.oltBtn.setMinimumSize(QSize(80, 80))
        self.oltBtn.setMaximumSize(QSize(80, 80))
        icon8 = QIcon()
        icon8.addFile(u":/icons/assets/olt.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.oltBtn.setIcon(icon8)
        self.oltBtn.setIconSize(QSize(60, 60))

        self.verticalLayout_12.addWidget(self.oltBtn, 0, Qt.AlignHCenter)

        self.label_13 = QLabel(self.frame_12)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.verticalLayout_12.addWidget(self.label_13, 0, Qt.AlignHCenter)

        self.label_14 = QLabel(self.frame_12)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)
        self.label_14.setStyleSheet(u"text-align: center;")

        self.verticalLayout_12.addWidget(self.label_14, 0, Qt.AlignHCenter)


        self.verticalLayout_11.addWidget(self.frame_12, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_7.addWidget(self.card4)

        self.card5 = QFrame(self.cards)
        self.card5.setObjectName(u"card5")
        self.card5.setMinimumSize(QSize(160, 210))
        self.card5.setMaximumSize(QSize(160, 210))
        self.card5.setStyleSheet(u"background-color: rgb(58, 65, 82);\n"
"border-radius: 15;")
        self.card5.setFrameShape(QFrame.NoFrame)
        self.card5.setFrameShadow(QFrame.Raised)
        self.card5.setLineWidth(5)
        self.verticalLayout_7 = QVBoxLayout(self.card5)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.card5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(150, 120))
        self.frame_8.setMaximumSize(QSize(150, 120))
        self.frame_8.setStyleSheet(u"")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.linkBtn = QPushButton(self.frame_8)
        self.linkBtn.setObjectName(u"linkBtn")
        self.linkBtn.setMinimumSize(QSize(80, 80))
        self.linkBtn.setMaximumSize(QSize(80, 80))
        icon9 = QIcon()
        icon9.addFile(u":/icons/assets/link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.linkBtn.setIcon(icon9)
        self.linkBtn.setIconSize(QSize(60, 60))

        self.verticalLayout_8.addWidget(self.linkBtn, 0, Qt.AlignHCenter)

        self.label_9 = QLabel(self.frame_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.verticalLayout_8.addWidget(self.label_9, 0, Qt.AlignHCenter)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)
        self.label_10.setStyleSheet(u"text-align: center;")

        self.verticalLayout_8.addWidget(self.label_10, 0, Qt.AlignHCenter)


        self.verticalLayout_7.addWidget(self.frame_8, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_7.addWidget(self.card5)


        self.verticalLayout_2.addWidget(self.cards)

        self.action_frame = QFrame(self.homePage)
        self.action_frame.setObjectName(u"action_frame")
        self.action_frame.setMaximumSize(QSize(16777215, 120))
        self.action_frame.setStyleSheet(u"")
        self.action_frame.setFrameShape(QFrame.NoFrame)
        self.action_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.action_frame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_10 = QSpacerItem(170, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)

        self.dbmsBtn = QPushButton(self.action_frame)
        self.dbmsBtn.setObjectName(u"dbmsBtn")
        self.dbmsBtn.setMinimumSize(QSize(150, 46))
        self.dbmsBtn.setMaximumSize(QSize(150, 46))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.dbmsBtn.setFont(font2)
        self.dbmsBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(68, 204, 136);\n"
"	border: none;\n"
"	border-radius: 23;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(59, 173, 116);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: rgb(51, 150, 101);\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icons/assets/database.svg", QSize(), QIcon.Normal, QIcon.On)
        self.dbmsBtn.setIcon(icon10)

        self.horizontalLayout_8.addWidget(self.dbmsBtn)

        self.horizontalSpacer_9 = QSpacerItem(170, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)


        self.verticalLayout_2.addWidget(self.action_frame)

        self.container.addWidget(self.homePage)
        self.updatePage = QWidget()
        self.updatePage.setObjectName(u"updatePage")
        self.verticalLayout_16 = QVBoxLayout(self.updatePage)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer_2 = QSpacerItem(20, 69, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_2)

        self.frame_3 = QFrame(self.updatePage)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 50))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_12 = QSpacerItem(180, 19, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_12)

        self.fileTypeCB = QComboBox(self.frame_3)
        self.fileTypeCB.setObjectName(u"fileTypeCB")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fileTypeCB.sizePolicy().hasHeightForWidth())
        self.fileTypeCB.setSizePolicy(sizePolicy2)
        self.fileTypeCB.setMinimumSize(QSize(150, 0))
        self.fileTypeCB.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_11.addWidget(self.fileTypeCB)

        self.filePathLE = QLineEdit(self.frame_3)
        self.filePathLE.setObjectName(u"filePathLE")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filePathLE.sizePolicy().hasHeightForWidth())
        self.filePathLE.setSizePolicy(sizePolicy3)
        self.filePathLE.setMaximumSize(QSize(16777215, 30))
        self.filePathLE.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #55dd99;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #66eeaa;\n"
"}\n"
"")

        self.horizontalLayout_11.addWidget(self.filePathLE)

        self.choseFileBtn = QPushButton(self.frame_3)
        self.choseFileBtn.setObjectName(u"choseFileBtn")
        sizePolicy2.setHeightForWidth(self.choseFileBtn.sizePolicy().hasHeightForWidth())
        self.choseFileBtn.setSizePolicy(sizePolicy2)
        self.choseFileBtn.setMinimumSize(QSize(100, 0))
        self.choseFileBtn.setMaximumSize(QSize(100, 30))
        self.choseFileBtn.setStyleSheet(u"QPushButton {\n"
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
        icon11 = QIcon()
        icon11.addFile(u":/icons/assets/file.svg", QSize(), QIcon.Normal, QIcon.On)
        self.choseFileBtn.setIcon(icon11)

        self.horizontalLayout_11.addWidget(self.choseFileBtn)

        self.updateDataBaseBtn = QPushButton(self.frame_3)
        self.updateDataBaseBtn.setObjectName(u"updateDataBaseBtn")
        sizePolicy2.setHeightForWidth(self.updateDataBaseBtn.sizePolicy().hasHeightForWidth())
        self.updateDataBaseBtn.setSizePolicy(sizePolicy2)
        self.updateDataBaseBtn.setMinimumSize(QSize(100, 0))
        self.updateDataBaseBtn.setMaximumSize(QSize(16777215, 30))
        self.updateDataBaseBtn.setStyleSheet(u"QPushButton {\n"
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
        icon12 = QIcon()
        icon12.addFile(u":/icons/assets/update.svg", QSize(), QIcon.Normal, QIcon.On)
        self.updateDataBaseBtn.setIcon(icon12)

        self.horizontalLayout_11.addWidget(self.updateDataBaseBtn)


        self.verticalLayout_16.addWidget(self.frame_3)

        self.frame_28 = QFrame(self.updatePage)
        self.frame_28.setObjectName(u"frame_28")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_28.sizePolicy().hasHeightForWidth())
        self.frame_28.setSizePolicy(sizePolicy4)
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalSpacer_15 = QSpacerItem(728, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_15)

        self.muti_file_cb = QCheckBox(self.frame_28)
        self.muti_file_cb.setObjectName(u"muti_file_cb")
        self.muti_file_cb.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 12px;\n"
"    height:12px;\n"
"    border: 2px solid #44cc88; /* \u53ef\u9009\u6846\u9ed8\u8ba4\u8fb9\u6846\u989c\u8272 */\n"
"    border-radius: 2px;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001\u7684\u53ef\u9009\u6846\u6837\u5f0f\uff08:checked \u4f2a\u72b6\u6001\uff09 */\n"
"QCheckBox::indicator:checked {\n"
"    border-color: #44cc88; /* \u9009\u4e2d\u540e\u8fb9\u6846\u4ecd\u4fdd\u6301#44cc88 */\n"
"    background-color: #44cc88; /* \u9009\u4e2d\u540e\u80cc\u666f\u8272\u8bbe\u4e3a#44cc88 */\n"
"    /* \u53ef\u9009\uff1a\u6dfb\u52a0\u52fe\u9009\u6807\u8bb0\uff08\u9ed8\u8ba4\u52fe\u9009\u6807\u8bb0\u4f1a\u663e\u793a\uff0c\u53ef\u81ea\u5b9a\u4e49\uff09 */\n"
"}\n"
"\n"
"/* \u53ef\u9009\uff1a\u9f20\u6807\u60ac\u6d6e\u65f6\u53ef\u9009\u6846\u8fb9\u6846\u52a0\u6df1 */\n"
"QCheckBox::indicator:hover {\n"
"    border-color: #33aa77; /* \u7565\u6df1\u7684\u7eff\u8272\uff0c\u63d0\u5347\u4ea4\u4e92\u4f53\u9a8c */\n"
"}\n"
"\n"
"QCheckBox {\n"
"    "
                        "padding-left: 8px;\n"
"    color: #44cc88;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"}")
        self.muti_file_cb.setChecked(False)

        self.horizontalLayout_27.addWidget(self.muti_file_cb)

        self.label_35 = QLabel(self.frame_28)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setStyleSheet(u"QLabel{\n"
"	padding-left:8px;\n"
"    color: #44cc88;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"}")

        self.horizontalLayout_27.addWidget(self.label_35)

        self.header_sb = QSpinBox(self.frame_28)
        self.header_sb.setObjectName(u"header_sb")
        self.header_sb.setMinimumSize(QSize(0, 25))
        self.header_sb.setMaximumSize(QSize(16777215, 25))
        self.header_sb.setStyleSheet(u"QSpinBox {\n"
"    border: 1px solid #44cc88;\n"
"    font-size: 12px;\n"
"    color: #44cc88;\n"
"}\n"
"\n"
"")
        self.header_sb.setMinimum(1)

        self.horizontalLayout_27.addWidget(self.header_sb)


        self.verticalLayout_16.addWidget(self.frame_28)

        self.verticalSpacer_3 = QSpacerItem(20, 31, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_3)

        self.frame_5 = QFrame(self.updatePage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy4.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy4)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.colsGridLayout = QGridLayout(self.frame_5)
        self.colsGridLayout.setSpacing(5)
        self.colsGridLayout.setObjectName(u"colsGridLayout")
        self.fileTypeCB_12 = QComboBox(self.frame_5)
        self.fileTypeCB_12.setObjectName(u"fileTypeCB_12")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_12.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_12.setSizePolicy(sizePolicy2)
        self.fileTypeCB_12.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_12.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_12.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_12, 5, 2, 1, 1)

        self.label_26 = QLabel(self.frame_5)
        self.label_26.setObjectName(u"label_26")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy5)
        self.label_26.setMaximumSize(QSize(16777215, 30))
        self.label_26.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_26.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_26, 2, 3, 1, 1)

        self.fileTypeCB_3 = QComboBox(self.frame_5)
        self.fileTypeCB_3.setObjectName(u"fileTypeCB_3")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_3.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_3.setSizePolicy(sizePolicy2)
        self.fileTypeCB_3.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_3.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_3.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_3, 1, 1, 1, 1)

        self.label_30 = QLabel(self.frame_5)
        self.label_30.setObjectName(u"label_30")
        sizePolicy5.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy5)
        self.label_30.setMaximumSize(QSize(16777215, 30))
        self.label_30.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_30.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_30, 4, 2, 1, 1)

        self.label_24 = QLabel(self.frame_5)
        self.label_24.setObjectName(u"label_24")
        sizePolicy5.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy5)
        self.label_24.setMaximumSize(QSize(16777215, 30))
        self.label_24.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_24.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_24, 2, 1, 1, 1)

        self.fileTypeCB_4 = QComboBox(self.frame_5)
        self.fileTypeCB_4.setObjectName(u"fileTypeCB_4")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_4.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_4.setSizePolicy(sizePolicy2)
        self.fileTypeCB_4.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_4.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_4.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_4, 1, 2, 1, 1)

        self.fileTypeCB_15 = QComboBox(self.frame_5)
        self.fileTypeCB_15.setObjectName(u"fileTypeCB_15")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_15.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_15.setSizePolicy(sizePolicy2)
        self.fileTypeCB_15.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_15.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_15.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_15, 3, 4, 1, 1)

        self.fileTypeCB_13 = QComboBox(self.frame_5)
        self.fileTypeCB_13.setObjectName(u"fileTypeCB_13")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_13.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_13.setSizePolicy(sizePolicy2)
        self.fileTypeCB_13.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_13.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_13.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_13, 5, 3, 1, 1)

        self.fileTypeCB_11 = QComboBox(self.frame_5)
        self.fileTypeCB_11.setObjectName(u"fileTypeCB_11")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_11.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_11.setSizePolicy(sizePolicy2)
        self.fileTypeCB_11.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_11.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_11.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_11, 5, 1, 1, 1)

        self.fileTypeCB_6 = QComboBox(self.frame_5)
        self.fileTypeCB_6.setObjectName(u"fileTypeCB_6")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_6.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_6.setSizePolicy(sizePolicy2)
        self.fileTypeCB_6.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_6.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_6.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_6, 3, 0, 1, 1)

        self.label_29 = QLabel(self.frame_5)
        self.label_29.setObjectName(u"label_29")
        sizePolicy5.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy5)
        self.label_29.setMaximumSize(QSize(16777215, 30))
        self.label_29.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_29.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_29, 4, 1, 1, 1)

        self.label_28 = QLabel(self.frame_5)
        self.label_28.setObjectName(u"label_28")
        sizePolicy5.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy5)
        self.label_28.setMaximumSize(QSize(16777215, 30))
        self.label_28.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_28.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_28, 4, 0, 1, 1)

        self.fileTypeCB_9 = QComboBox(self.frame_5)
        self.fileTypeCB_9.setObjectName(u"fileTypeCB_9")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_9.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_9.setSizePolicy(sizePolicy2)
        self.fileTypeCB_9.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_9.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_9.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_9, 3, 3, 1, 1)

        self.label_21 = QLabel(self.frame_5)
        self.label_21.setObjectName(u"label_21")
        sizePolicy5.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy5)
        self.label_21.setMaximumSize(QSize(16777215, 30))
        self.label_21.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_21.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_21, 0, 3, 1, 1)

        self.fileTypeCB_10 = QComboBox(self.frame_5)
        self.fileTypeCB_10.setObjectName(u"fileTypeCB_10")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_10.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_10.setSizePolicy(sizePolicy2)
        self.fileTypeCB_10.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_10.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_10.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_10, 5, 0, 1, 1)

        self.label_20 = QLabel(self.frame_5)
        self.label_20.setObjectName(u"label_20")
        sizePolicy5.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy5)
        self.label_20.setMaximumSize(QSize(16777215, 30))
        self.label_20.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_20.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_20, 0, 2, 1, 1)

        self.fileTypeCB_14 = QComboBox(self.frame_5)
        self.fileTypeCB_14.setObjectName(u"fileTypeCB_14")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_14.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_14.setSizePolicy(sizePolicy2)
        self.fileTypeCB_14.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_14.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_14.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_14, 5, 4, 1, 1)

        self.label_32 = QLabel(self.frame_5)
        self.label_32.setObjectName(u"label_32")
        sizePolicy5.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy5)
        self.label_32.setMaximumSize(QSize(16777215, 30))
        self.label_32.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_32.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_32, 4, 4, 1, 1)

        self.label_27 = QLabel(self.frame_5)
        self.label_27.setObjectName(u"label_27")
        sizePolicy5.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy5)
        self.label_27.setMaximumSize(QSize(16777215, 30))
        self.label_27.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_27, 2, 4, 1, 1)

        self.label_23 = QLabel(self.frame_5)
        self.label_23.setObjectName(u"label_23")
        sizePolicy5.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy5)
        self.label_23.setMaximumSize(QSize(16777215, 30))
        self.label_23.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_23.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_23, 2, 0, 1, 1)

        self.label_19 = QLabel(self.frame_5)
        self.label_19.setObjectName(u"label_19")
        sizePolicy5.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy5)
        self.label_19.setMaximumSize(QSize(16777215, 30))
        self.label_19.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_19.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_19, 0, 1, 1, 1)

        self.fileTypeCB_5 = QComboBox(self.frame_5)
        self.fileTypeCB_5.setObjectName(u"fileTypeCB_5")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_5.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_5.setSizePolicy(sizePolicy2)
        self.fileTypeCB_5.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_5.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_5.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_5, 1, 3, 1, 1)

        self.label_25 = QLabel(self.frame_5)
        self.label_25.setObjectName(u"label_25")
        sizePolicy5.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy5)
        self.label_25.setMaximumSize(QSize(16777215, 30))
        self.label_25.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_25.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_25, 2, 2, 1, 1)

        self.label_22 = QLabel(self.frame_5)
        self.label_22.setObjectName(u"label_22")
        sizePolicy5.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy5)
        self.label_22.setMaximumSize(QSize(16777215, 30))
        self.label_22.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_22.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_22, 0, 4, 1, 1)

        self.fileTypeCB_16 = QComboBox(self.frame_5)
        self.fileTypeCB_16.setObjectName(u"fileTypeCB_16")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_16.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_16.setSizePolicy(sizePolicy2)
        self.fileTypeCB_16.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_16.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_16.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_16, 1, 4, 1, 1)

        self.label_18 = QLabel(self.frame_5)
        self.label_18.setObjectName(u"label_18")
        sizePolicy5.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy5)
        self.label_18.setMaximumSize(QSize(16777215, 30))
        self.label_18.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_18.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_18, 0, 0, 1, 1)

        self.fileTypeCB_2 = QComboBox(self.frame_5)
        self.fileTypeCB_2.setObjectName(u"fileTypeCB_2")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_2.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_2.setSizePolicy(sizePolicy2)
        self.fileTypeCB_2.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_2.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_2.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_2, 1, 0, 1, 1)

        self.fileTypeCB_8 = QComboBox(self.frame_5)
        self.fileTypeCB_8.setObjectName(u"fileTypeCB_8")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_8.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_8.setSizePolicy(sizePolicy2)
        self.fileTypeCB_8.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_8.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_8.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_8, 3, 2, 1, 1)

        self.fileTypeCB_7 = QComboBox(self.frame_5)
        self.fileTypeCB_7.setObjectName(u"fileTypeCB_7")
        sizePolicy2.setHeightForWidth(self.fileTypeCB_7.sizePolicy().hasHeightForWidth())
        self.fileTypeCB_7.setSizePolicy(sizePolicy2)
        self.fileTypeCB_7.setMinimumSize(QSize(150, 0))
        self.fileTypeCB_7.setMaximumSize(QSize(16777215, 30))
        self.fileTypeCB_7.setStyleSheet(u"QComboBox {\n"
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

        self.colsGridLayout.addWidget(self.fileTypeCB_7, 3, 1, 1, 1)

        self.label_31 = QLabel(self.frame_5)
        self.label_31.setObjectName(u"label_31")
        sizePolicy5.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy5)
        self.label_31.setMaximumSize(QSize(16777215, 30))
        self.label_31.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}")
        self.label_31.setAlignment(Qt.AlignCenter)

        self.colsGridLayout.addWidget(self.label_31, 4, 3, 1, 1)


        self.verticalLayout_16.addWidget(self.frame_5)

        self.verticalSpacer = QSpacerItem(20, 91, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer)

        self.container.addWidget(self.updatePage)
        self.analysisPage = QWidget()
        self.analysisPage.setObjectName(u"analysisPage")
        self.verticalLayout_18 = QVBoxLayout(self.analysisPage)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.frame_9 = QFrame(self.analysisPage)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_9)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.analysisLabel = QLabel(self.frame_9)
        self.analysisLabel.setObjectName(u"analysisLabel")
        self.analysisLabel.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.analysisLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.analysisLabel)

        self.needTalbeTE = QTextEdit(self.frame_9)
        self.needTalbeTE.setObjectName(u"needTalbeTE")
        self.needTalbeTE.setStyleSheet(u"QTextEdit {\n"
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

        self.verticalLayout_17.addWidget(self.needTalbeTE)


        self.verticalLayout_18.addWidget(self.frame_9)

        self.frame_11 = QFrame(self.analysisPage)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy5.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy5)
        self.frame_11.setMaximumSize(QSize(16777215, 40))
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_13 = QSpacerItem(855, 19, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_13)

        self.checkTableBtn = QPushButton(self.frame_11)
        self.checkTableBtn.setObjectName(u"checkTableBtn")
        self.checkTableBtn.setMinimumSize(QSize(100, 30))
        self.checkTableBtn.setMaximumSize(QSize(100, 30))
        self.checkTableBtn.setStyleSheet(u"QPushButton {\n"
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
        icon13 = QIcon()
        icon13.addFile(u":/icons/assets/check.svg", QSize(), QIcon.Normal, QIcon.On)
        self.checkTableBtn.setIcon(icon13)

        self.horizontalLayout_14.addWidget(self.checkTableBtn)

        self.runAnalysisBtn = QPushButton(self.frame_11)
        self.runAnalysisBtn.setObjectName(u"runAnalysisBtn")
        self.runAnalysisBtn.setMinimumSize(QSize(100, 30))
        self.runAnalysisBtn.setMaximumSize(QSize(100, 30))
        self.runAnalysisBtn.setStyleSheet(u"QPushButton {\n"
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
        icon14 = QIcon()
        icon14.addFile(u":/icons/assets/run.svg", QSize(), QIcon.Normal, QIcon.On)
        self.runAnalysisBtn.setIcon(icon14)

        self.horizontalLayout_14.addWidget(self.runAnalysisBtn)


        self.verticalLayout_18.addWidget(self.frame_11)

        self.processBarFrame = QFrame(self.analysisPage)
        self.processBarFrame.setObjectName(u"processBarFrame")
        sizePolicy5.setHeightForWidth(self.processBarFrame.sizePolicy().hasHeightForWidth())
        self.processBarFrame.setSizePolicy(sizePolicy5)
        self.processBarFrame.setMaximumSize(QSize(16777215, 40))
        self.processBarFrame.setFrameShape(QFrame.StyledPanel)
        self.processBarFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.processBarFrame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.runProgressBar = QProgressBar(self.processBarFrame)
        self.runProgressBar.setObjectName(u"runProgressBar")
        self.runProgressBar.setStyleSheet(u"QProgressBar {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"        text-align: center;\n"
"        color: #44cc88;\n"
"    }\n"
"    \n"
"    QProgressBar::chunk {\n"
"        background-color: #44cc88;\n"
"        border-radius: 3px;\n"
"    }")
        self.runProgressBar.setValue(24)
        self.runProgressBar.setTextVisible(True)

        self.horizontalLayout_13.addWidget(self.runProgressBar)

        self.needTime = QLabel(self.processBarFrame)
        self.needTime.setObjectName(u"needTime")
        self.needTime.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"	font-weight:700;\n"
"}")

        self.horizontalLayout_13.addWidget(self.needTime)


        self.verticalLayout_18.addWidget(self.processBarFrame)

        self.container.addWidget(self.analysisPage)
        self.dbTablePage = QWidget()
        self.dbTablePage.setObjectName(u"dbTablePage")
        self.verticalLayout_19 = QVBoxLayout(self.dbTablePage)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(9, -1, -1, 0)
        self.frame_15 = QFrame(self.dbTablePage)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy5.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy5)
        self.frame_15.setMaximumSize(QSize(16777215, 50))
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalSpacer_14 = QSpacerItem(855, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_14)

        self.dbTableBtn = QPushButton(self.frame_15)
        self.dbTableBtn.setObjectName(u"dbTableBtn")
        self.dbTableBtn.setMinimumSize(QSize(100, 30))
        self.dbTableBtn.setMaximumSize(QSize(100, 30))
        self.dbTableBtn.setStyleSheet(u"QPushButton {\n"
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
        icon15 = QIcon()
        icon15.addFile(u":/icons/assets/search.svg", QSize(), QIcon.Normal, QIcon.On)
        self.dbTableBtn.setIcon(icon15)

        self.horizontalLayout_15.addWidget(self.dbTableBtn)


        self.verticalLayout_19.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.dbTablePage)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.dbTableTw = QTableWidget(self.frame_16)
        self.dbTableTw.setObjectName(u"dbTableTw")
        self.dbTableTw.setStyleSheet(u"QTableWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        gridline-color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"    }\n"
"    \n"
"    QTableWidget::item {\n"
"        border: none;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableWidget::item:selected {\n"
"        background-color: #44cc88;\n"
"        color: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QHeaderView::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableCornerButton::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"    }")

        self.horizontalLayout_16.addWidget(self.dbTableTw)


        self.verticalLayout_19.addWidget(self.frame_16)

        self.container.addWidget(self.dbTablePage)
        self.kpiPage = QWidget()
        self.kpiPage.setObjectName(u"kpiPage")
        self.verticalLayout_20 = QVBoxLayout(self.kpiPage)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.frame_19 = QFrame(self.kpiPage)
        self.frame_19.setObjectName(u"frame_19")
        sizePolicy5.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy5)
        self.frame_19.setMaximumSize(QSize(16777215, 50))
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_34 = QLabel(self.frame_19)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")

        self.horizontalLayout_18.addWidget(self.label_34)


        self.verticalLayout_20.addWidget(self.frame_19)

        self.frame_18 = QFrame(self.kpiPage)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_18)
        self.gridLayout.setObjectName(u"gridLayout")
        self.writeAggrHouseBtn = QPushButton(self.frame_18)
        self.writeAggrHouseBtn.setObjectName(u"writeAggrHouseBtn")
        sizePolicy2.setHeightForWidth(self.writeAggrHouseBtn.sizePolicy().hasHeightForWidth())
        self.writeAggrHouseBtn.setSizePolicy(sizePolicy2)
        self.writeAggrHouseBtn.setMinimumSize(QSize(100, 100))
        self.writeAggrHouseBtn.setMaximumSize(QSize(100, 100))
        self.writeAggrHouseBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.writeAggrHouseBtn, 0, 0, 1, 1)

        self.redOltPortSiteBtn = QPushButton(self.frame_18)
        self.redOltPortSiteBtn.setObjectName(u"redOltPortSiteBtn")
        sizePolicy2.setHeightForWidth(self.redOltPortSiteBtn.sizePolicy().hasHeightForWidth())
        self.redOltPortSiteBtn.setSizePolicy(sizePolicy2)
        self.redOltPortSiteBtn.setMinimumSize(QSize(100, 100))
        self.redOltPortSiteBtn.setMaximumSize(QSize(100, 100))
        self.redOltPortSiteBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.redOltPortSiteBtn, 0, 1, 1, 1)

        self.notOltAggrSiteBtn = QPushButton(self.frame_18)
        self.notOltAggrSiteBtn.setObjectName(u"notOltAggrSiteBtn")
        sizePolicy2.setHeightForWidth(self.notOltAggrSiteBtn.sizePolicy().hasHeightForWidth())
        self.notOltAggrSiteBtn.setSizePolicy(sizePolicy2)
        self.notOltAggrSiteBtn.setMinimumSize(QSize(100, 100))
        self.notOltAggrSiteBtn.setMaximumSize(QSize(100, 100))
        self.notOltAggrSiteBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.notOltAggrSiteBtn, 0, 2, 1, 1)

        self.notXgOltBtn = QPushButton(self.frame_18)
        self.notXgOltBtn.setObjectName(u"notXgOltBtn")
        sizePolicy2.setHeightForWidth(self.notXgOltBtn.sizePolicy().hasHeightForWidth())
        self.notXgOltBtn.setSizePolicy(sizePolicy2)
        self.notXgOltBtn.setMinimumSize(QSize(100, 100))
        self.notXgOltBtn.setMaximumSize(QSize(100, 100))
        self.notXgOltBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.notXgOltBtn, 0, 3, 1, 1)

        self.blueAggrSiteBtn = QPushButton(self.frame_18)
        self.blueAggrSiteBtn.setObjectName(u"blueAggrSiteBtn")
        sizePolicy2.setHeightForWidth(self.blueAggrSiteBtn.sizePolicy().hasHeightForWidth())
        self.blueAggrSiteBtn.setSizePolicy(sizePolicy2)
        self.blueAggrSiteBtn.setMinimumSize(QSize(100, 100))
        self.blueAggrSiteBtn.setMaximumSize(QSize(100, 100))
        self.blueAggrSiteBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.blueAggrSiteBtn, 0, 4, 1, 1)

        self.boxUplinkBusyBtn = QPushButton(self.frame_18)
        self.boxUplinkBusyBtn.setObjectName(u"boxUplinkBusyBtn")
        sizePolicy2.setHeightForWidth(self.boxUplinkBusyBtn.sizePolicy().hasHeightForWidth())
        self.boxUplinkBusyBtn.setSizePolicy(sizePolicy2)
        self.boxUplinkBusyBtn.setMinimumSize(QSize(100, 100))
        self.boxUplinkBusyBtn.setMaximumSize(QSize(100, 100))
        self.boxUplinkBusyBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.boxUplinkBusyBtn, 1, 0, 1, 1)

        self.onuBtn = QPushButton(self.frame_18)
        self.onuBtn.setObjectName(u"onuBtn")
        sizePolicy2.setHeightForWidth(self.onuBtn.sizePolicy().hasHeightForWidth())
        self.onuBtn.setSizePolicy(sizePolicy2)
        self.onuBtn.setMinimumSize(QSize(100, 100))
        self.onuBtn.setMaximumSize(QSize(100, 100))
        self.onuBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.onuBtn, 1, 1, 1, 1)

        self.ponLineProjectBtn = QPushButton(self.frame_18)
        self.ponLineProjectBtn.setObjectName(u"ponLineProjectBtn")
        sizePolicy2.setHeightForWidth(self.ponLineProjectBtn.sizePolicy().hasHeightForWidth())
        self.ponLineProjectBtn.setSizePolicy(sizePolicy2)
        self.ponLineProjectBtn.setMinimumSize(QSize(100, 100))
        self.ponLineProjectBtn.setMaximumSize(QSize(100, 100))
        self.ponLineProjectBtn.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout.addWidget(self.ponLineProjectBtn, 1, 2, 1, 1)


        self.verticalLayout_20.addWidget(self.frame_18)

        self.container.addWidget(self.kpiPage)
        self.outsidePage = QWidget()
        self.outsidePage.setObjectName(u"outsidePage")
        self.verticalLayout_21 = QVBoxLayout(self.outsidePage)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(-1, -1, 18, -1)
        self.tabWidget = QTabWidget(self.outsidePage)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"    }\n"
"QTabWidget::pane {\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"QTabBar::tab {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 8px;\n"
"        border-top-left-radius: 8px;\n"
"        border-top-right-radius: 8px;\n"
"    }\n"
"QTabBar::tab:selected {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    border: 1px solid #44cc88;\n"
"	font: 700 10pt;\n"
"}\n"
"QTabBar::tab:hover {\n"
"        background-color: rgba(50, 55, 66, 255);\n"
"    }")
        self.oDevPage = QWidget()
        self.oDevPage.setObjectName(u"oDevPage")
        self.verticalLayout_25 = QVBoxLayout(self.oDevPage)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(-1, -1, 9, -1)
        self.frame_21 = QFrame(self.oDevPage)
        self.frame_21.setObjectName(u"frame_21")
        sizePolicy5.setHeightForWidth(self.frame_21.sizePolicy().hasHeightForWidth())
        self.frame_21.setSizePolicy(sizePolicy5)
        self.frame_21.setMinimumSize(QSize(0, 50))
        self.frame_21.setMaximumSize(QSize(16777215, 50))
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_36 = QLabel(self.frame_21)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"}")

        self.horizontalLayout_20.addWidget(self.label_36)

        self.odevNameKeysLe = QLineEdit(self.frame_21)
        self.odevNameKeysLe.setObjectName(u"odevNameKeysLe")
        self.odevNameKeysLe.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #55dd99;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #66eeaa;\n"
"}\n"
"")

        self.horizontalLayout_20.addWidget(self.odevNameKeysLe)

        self.odevNamesCB = QComboBox(self.frame_21)
        self.odevNamesCB.setObjectName(u"odevNamesCB")
        sizePolicy2.setHeightForWidth(self.odevNamesCB.sizePolicy().hasHeightForWidth())
        self.odevNamesCB.setSizePolicy(sizePolicy2)
        self.odevNamesCB.setMinimumSize(QSize(400, 30))
        self.odevNamesCB.setMaximumSize(QSize(16777215, 30))
        self.odevNamesCB.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_20.addWidget(self.odevNamesCB)

        self.searchDevUplinkBtn = QPushButton(self.frame_21)
        self.searchDevUplinkBtn.setObjectName(u"searchDevUplinkBtn")
        sizePolicy2.setHeightForWidth(self.searchDevUplinkBtn.sizePolicy().hasHeightForWidth())
        self.searchDevUplinkBtn.setSizePolicy(sizePolicy2)
        self.searchDevUplinkBtn.setMinimumSize(QSize(100, 30))
        self.searchDevUplinkBtn.setMaximumSize(QSize(100, 30))
        self.searchDevUplinkBtn.setStyleSheet(u"QPushButton {\n"
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
        self.searchDevUplinkBtn.setIcon(icon15)

        self.horizontalLayout_20.addWidget(self.searchDevUplinkBtn)


        self.verticalLayout_25.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.oDevPage)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.upLinkTW = QTableWidget(self.frame_22)
        self.upLinkTW.setObjectName(u"upLinkTW")
        sizePolicy3.setHeightForWidth(self.upLinkTW.sizePolicy().hasHeightForWidth())
        self.upLinkTW.setSizePolicy(sizePolicy3)
        self.upLinkTW.setMinimumSize(QSize(0, 130))
        self.upLinkTW.setMaximumSize(QSize(16777215, 130))
        self.upLinkTW.setStyleSheet(u"QTableWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        gridline-color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"    }\n"
"    \n"
"    QTableWidget::item {\n"
"        border: none;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableWidget::item:selected {\n"
"        background-color: #44cc88;\n"
"        color: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QHeaderView::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableCornerButton::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"    }")

        self.horizontalLayout_21.addWidget(self.upLinkTW)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.highScoreBtn = QPushButton(self.frame_22)
        self.highScoreBtn.setObjectName(u"highScoreBtn")
        sizePolicy.setHeightForWidth(self.highScoreBtn.sizePolicy().hasHeightForWidth())
        self.highScoreBtn.setSizePolicy(sizePolicy)
        self.highScoreBtn.setMinimumSize(QSize(80, 30))
        self.highScoreBtn.setMaximumSize(QSize(80, 30))
        self.highScoreBtn.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_22.addWidget(self.highScoreBtn)

        self.dbmMinBtn = QPushButton(self.frame_22)
        self.dbmMinBtn.setObjectName(u"dbmMinBtn")
        sizePolicy.setHeightForWidth(self.dbmMinBtn.sizePolicy().hasHeightForWidth())
        self.dbmMinBtn.setSizePolicy(sizePolicy)
        self.dbmMinBtn.setMinimumSize(QSize(80, 30))
        self.dbmMinBtn.setMaximumSize(QSize(80, 30))
        self.dbmMinBtn.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_22.addWidget(self.dbmMinBtn)

        self.numMaxBtn = QPushButton(self.frame_22)
        self.numMaxBtn.setObjectName(u"numMaxBtn")
        sizePolicy.setHeightForWidth(self.numMaxBtn.sizePolicy().hasHeightForWidth())
        self.numMaxBtn.setSizePolicy(sizePolicy)
        self.numMaxBtn.setMinimumSize(QSize(80, 30))
        self.numMaxBtn.setMaximumSize(QSize(80, 30))
        self.numMaxBtn.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_22.addWidget(self.numMaxBtn)


        self.horizontalLayout_21.addLayout(self.verticalLayout_22)


        self.verticalLayout_25.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.oDevPage)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.uplink_text = QTextEdit(self.frame_23)
        self.uplink_text.setObjectName(u"uplink_text")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.uplink_text.sizePolicy().hasHeightForWidth())
        self.uplink_text.setSizePolicy(sizePolicy6)
        self.uplink_text.setMinimumSize(QSize(0, 80))
        self.uplink_text.setMaximumSize(QSize(16777215, 80))
        self.uplink_text.setStyleSheet(u"QTextEdit {\n"
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

        self.verticalLayout_24.addWidget(self.uplink_text)

        self.uplink_topo = TopologyView(self.frame_23)
        self.uplink_topo.setObjectName(u"uplink_topo")
        self.uplink_topo.setStyleSheet(u"QGraphicsView {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    /* \u6eda\u52a8\u6761\u6837\u5f0f */\n"
"    QScrollBar:horizontal {\n"
"        height: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar:vertical {\n"
"        width: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar::handle {\n"
"        background: #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    QScrollBar::add-line, QScrollBar::sub-line {\n"
"        background: none;\n"
"    }")

        self.verticalLayout_24.addWidget(self.uplink_topo)


        self.horizontalLayout_22.addLayout(self.verticalLayout_24)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_37 = QLabel(self.frame_23)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(80, 80))
        self.label_37.setMaximumSize(QSize(80, 80))
        self.label_37.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_37.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.label_37)

        self.label_38 = QLabel(self.frame_23)
        self.label_38.setObjectName(u"label_38")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy7)
        self.label_38.setMinimumSize(QSize(80, 80))
        self.label_38.setMaximumSize(QSize(80, 10000))
        self.label_38.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_38.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.label_38)


        self.horizontalLayout_22.addLayout(self.verticalLayout_23)


        self.verticalLayout_25.addWidget(self.frame_23)

        self.tabWidget.addTab(self.oDevPage, "")
        self.linePage = QWidget()
        self.linePage.setObjectName(u"linePage")
        self.verticalLayout_30 = QVBoxLayout(self.linePage)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.frame_27 = QFrame(self.linePage)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_33 = QLabel(self.frame_27)
        self.label_33.setObjectName(u"label_33")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy8)
        self.label_33.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"}")

        self.horizontalLayout_26.addWidget(self.label_33)

        self.lineKeysLE = QLineEdit(self.frame_27)
        self.lineKeysLE.setObjectName(u"lineKeysLE")
        sizePolicy3.setHeightForWidth(self.lineKeysLE.sizePolicy().hasHeightForWidth())
        self.lineKeysLE.setSizePolicy(sizePolicy3)
        self.lineKeysLE.setMinimumSize(QSize(0, 30))
        self.lineKeysLE.setMaximumSize(QSize(16777215, 30))
        self.lineKeysLE.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #55dd99;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #66eeaa;\n"
"}\n"
"")

        self.horizontalLayout_26.addWidget(self.lineKeysLE)

        self.searchLineBtn = QPushButton(self.frame_27)
        self.searchLineBtn.setObjectName(u"searchLineBtn")
        sizePolicy2.setHeightForWidth(self.searchLineBtn.sizePolicy().hasHeightForWidth())
        self.searchLineBtn.setSizePolicy(sizePolicy2)
        self.searchLineBtn.setMinimumSize(QSize(100, 30))
        self.searchLineBtn.setMaximumSize(QSize(100, 30))
        self.searchLineBtn.setStyleSheet(u"QPushButton {\n"
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
        icon16 = QIcon()
        icon16.addFile(u":/icons/assets/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.searchLineBtn.setIcon(icon16)

        self.horizontalLayout_26.addWidget(self.searchLineBtn)


        self.verticalLayout_30.addWidget(self.frame_27)

        self.frame_7 = QFrame(self.linePage)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.devLE = QLineEdit(self.frame_7)
        self.devLE.setObjectName(u"devLE")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.devLE.sizePolicy().hasHeightForWidth())
        self.devLE.setSizePolicy(sizePolicy9)
        self.devLE.setMinimumSize(QSize(150, 30))
        self.devLE.setMaximumSize(QSize(150, 30))
        self.devLE.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")

        self.horizontalLayout_12.addWidget(self.devLE)

        self.devCB = QComboBox(self.frame_7)
        self.devCB.setObjectName(u"devCB")
        self.devCB.setMinimumSize(QSize(0, 30))
        self.devCB.setMaximumSize(QSize(16777215, 30))
        self.devCB.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_12.addWidget(self.devCB)

        self.aSiteBtn = QPushButton(self.frame_7)
        self.aSiteBtn.setObjectName(u"aSiteBtn")
        sizePolicy9.setHeightForWidth(self.aSiteBtn.sizePolicy().hasHeightForWidth())
        self.aSiteBtn.setSizePolicy(sizePolicy9)
        self.aSiteBtn.setMinimumSize(QSize(100, 30))
        self.aSiteBtn.setMaximumSize(QSize(100, 30))
        self.aSiteBtn.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_12.addWidget(self.aSiteBtn)

        self.bSiteBtn = QPushButton(self.frame_7)
        self.bSiteBtn.setObjectName(u"bSiteBtn")
        self.bSiteBtn.setMinimumSize(QSize(100, 30))
        self.bSiteBtn.setMaximumSize(QSize(100, 30))
        self.bSiteBtn.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_12.addWidget(self.bSiteBtn)

        self.mustDevBtn = QPushButton(self.frame_7)
        self.mustDevBtn.setObjectName(u"mustDevBtn")
        self.mustDevBtn.setMinimumSize(QSize(100, 30))
        self.mustDevBtn.setMaximumSize(QSize(100, 30))
        self.mustDevBtn.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_12.addWidget(self.mustDevBtn)

        self.notDevBtn = QPushButton(self.frame_7)
        self.notDevBtn.setObjectName(u"notDevBtn")
        self.notDevBtn.setMinimumSize(QSize(100, 30))
        self.notDevBtn.setMaximumSize(QSize(100, 30))
        self.notDevBtn.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_12.addWidget(self.notDevBtn)


        self.verticalLayout_30.addWidget(self.frame_7)

        self.frame_29 = QFrame(self.linePage)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_15 = QLabel(self.frame_29)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(50, 30))
        self.label_15.setMaximumSize(QSize(50, 30))
        self.label_15.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_15)

        self.aSiteLabel = QLabel(self.frame_29)
        self.aSiteLabel.setObjectName(u"aSiteLabel")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.aSiteLabel.sizePolicy().hasHeightForWidth())
        self.aSiteLabel.setSizePolicy(sizePolicy10)
        self.aSiteLabel.setMinimumSize(QSize(250, 30))
        self.aSiteLabel.setMaximumSize(QSize(250, 30))
        self.aSiteLabel.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"}")

        self.horizontalLayout_17.addWidget(self.aSiteLabel)

        self.label_17 = QLabel(self.frame_29)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(50, 30))
        self.label_17.setMaximumSize(QSize(50, 30))
        self.label_17.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_17.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_17)

        self.bSiteLabel = QLabel(self.frame_29)
        self.bSiteLabel.setObjectName(u"bSiteLabel")
        sizePolicy10.setHeightForWidth(self.bSiteLabel.sizePolicy().hasHeightForWidth())
        self.bSiteLabel.setSizePolicy(sizePolicy10)
        self.bSiteLabel.setMinimumSize(QSize(250, 30))
        self.bSiteLabel.setMaximumSize(QSize(250, 30))
        self.bSiteLabel.setStyleSheet(u"QLabel {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"}")

        self.horizontalLayout_17.addWidget(self.bSiteLabel)

        self.label_41 = QLabel(self.frame_29)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(50, 30))
        self.label_41.setMaximumSize(QSize(50, 30))
        self.label_41.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_41.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_41)

        self.jumpNumSB = QSpinBox(self.frame_29)
        self.jumpNumSB.setObjectName(u"jumpNumSB")
        self.jumpNumSB.setMinimumSize(QSize(55, 30))
        self.jumpNumSB.setMaximumSize(QSize(55, 30))
        self.jumpNumSB.setStyleSheet(u"QSpinBox {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")
        self.jumpNumSB.setMinimum(3)
        self.jumpNumSB.setMaximum(8)
        self.jumpNumSB.setValue(5)

        self.horizontalLayout_17.addWidget(self.jumpNumSB)

        self.label_42 = QLabel(self.frame_29)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(50, 30))
        self.label_42.setMaximumSize(QSize(50, 30))
        self.label_42.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_42.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_42)

        self.dBmNumSB = QSpinBox(self.frame_29)
        self.dBmNumSB.setObjectName(u"dBmNumSB")
        self.dBmNumSB.setMinimumSize(QSize(55, 30))
        self.dBmNumSB.setMaximumSize(QSize(55, 30))
        self.dBmNumSB.setStyleSheet(u"QSpinBox {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")
        self.dBmNumSB.setMinimum(6)
        self.dBmNumSB.setMaximum(21)
        self.dBmNumSB.setSingleStep(1)
        self.dBmNumSB.setValue(14)

        self.horizontalLayout_17.addWidget(self.dBmNumSB)


        self.verticalLayout_30.addWidget(self.frame_29)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.frame_14 = QFrame(self.linePage)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_14)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_45 = QLabel(self.frame_14)
        self.label_45.setObjectName(u"label_45")
        sizePolicy6.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy6)
        self.label_45.setMinimumSize(QSize(0, 30))
        self.label_45.setMaximumSize(QSize(16777215, 30))
        self.label_45.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_45.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.label_45)

        self.mustDevLW = QListWidget(self.frame_14)
        self.mustDevLW.setObjectName(u"mustDevLW")
        self.mustDevLW.setStyleSheet(u"QListWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        gridline-color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"    }\n"
"    \n"
"    QListWidget::item {\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QListWidget::item:selected {\n"
"        background-color: #44cc88;\n"
"        color: rgba(28, 33, 44, 255);\n"
"    }\n"
"    ")

        self.verticalLayout_27.addWidget(self.mustDevLW)


        self.horizontalLayout_29.addWidget(self.frame_14)

        self.frame_17 = QFrame(self.linePage)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_17)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.label_46 = QLabel(self.frame_17)
        self.label_46.setObjectName(u"label_46")
        sizePolicy6.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy6)
        self.label_46.setMinimumSize(QSize(0, 30))
        self.label_46.setMaximumSize(QSize(16777215, 30))
        self.label_46.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_46.setAlignment(Qt.AlignCenter)

        self.verticalLayout_28.addWidget(self.label_46)

        self.notDevLW = QListWidget(self.frame_17)
        self.notDevLW.setObjectName(u"notDevLW")
        self.notDevLW.setStyleSheet(u"QListWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        gridline-color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"    }\n"
"    \n"
"    QListWidget::item {\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QListWidget::item:selected {\n"
"        background-color: #44cc88;\n"
"        color: rgba(28, 33, 44, 255);\n"
"    }\n"
"    ")

        self.verticalLayout_28.addWidget(self.notDevLW)


        self.horizontalLayout_29.addWidget(self.frame_17)

        self.frame_30 = QFrame(self.linePage)
        self.frame_30.setObjectName(u"frame_30")
        self.verticalLayout_29 = QVBoxLayout(self.frame_30)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.delMustDevBtn = QPushButton(self.frame_30)
        self.delMustDevBtn.setObjectName(u"delMustDevBtn")
        self.delMustDevBtn.setMinimumSize(QSize(100, 30))
        self.delMustDevBtn.setMaximumSize(QSize(100, 30))
        self.delMustDevBtn.setStyleSheet(u"QPushButton {\n"
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
        icon17 = QIcon()
        icon17.addFile(u":/icons/assets/delete.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.delMustDevBtn.setIcon(icon17)

        self.verticalLayout_29.addWidget(self.delMustDevBtn)

        self.delNotDevBtn = QPushButton(self.frame_30)
        self.delNotDevBtn.setObjectName(u"delNotDevBtn")
        self.delNotDevBtn.setMinimumSize(QSize(100, 30))
        self.delNotDevBtn.setMaximumSize(QSize(100, 30))
        self.delNotDevBtn.setStyleSheet(u"QPushButton {\n"
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
        self.delNotDevBtn.setIcon(icon17)

        self.verticalLayout_29.addWidget(self.delNotDevBtn)

        self.devToLeftBtn = QPushButton(self.frame_30)
        self.devToLeftBtn.setObjectName(u"devToLeftBtn")
        self.devToLeftBtn.setMinimumSize(QSize(100, 30))
        self.devToLeftBtn.setMaximumSize(QSize(100, 30))
        self.devToLeftBtn.setStyleSheet(u"QPushButton {\n"
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
        icon18 = QIcon()
        icon18.addFile(u":/icons/assets/left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.devToLeftBtn.setIcon(icon18)

        self.verticalLayout_29.addWidget(self.devToLeftBtn)

        self.devToRightBtn = QPushButton(self.frame_30)
        self.devToRightBtn.setObjectName(u"devToRightBtn")
        self.devToRightBtn.setMinimumSize(QSize(100, 30))
        self.devToRightBtn.setMaximumSize(QSize(100, 30))
        self.devToRightBtn.setStyleSheet(u"QPushButton {\n"
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
        icon19 = QIcon()
        icon19.addFile(u":/icons/assets/right.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.devToRightBtn.setIcon(icon19)

        self.verticalLayout_29.addWidget(self.devToRightBtn)


        self.horizontalLayout_29.addWidget(self.frame_30)


        self.verticalLayout_30.addLayout(self.horizontalLayout_29)

        self.frame_20 = QFrame(self.linePage)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.dispatchTypeCB = QComboBox(self.frame_20)
        self.dispatchTypeCB.setObjectName(u"dispatchTypeCB")
        sizePolicy9.setHeightForWidth(self.dispatchTypeCB.sizePolicy().hasHeightForWidth())
        self.dispatchTypeCB.setSizePolicy(sizePolicy9)
        self.dispatchTypeCB.setMinimumSize(QSize(150, 30))
        self.dispatchTypeCB.setMaximumSize(QSize(150, 30))
        self.dispatchTypeCB.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_19.addWidget(self.dispatchTypeCB)

        self.importABsBtn = QPushButton(self.frame_20)
        self.importABsBtn.setObjectName(u"importABsBtn")
        self.importABsBtn.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.importABsBtn.sizePolicy().hasHeightForWidth())
        self.importABsBtn.setSizePolicy(sizePolicy2)
        self.importABsBtn.setMinimumSize(QSize(100, 30))
        self.importABsBtn.setMaximumSize(QSize(100, 30))
        self.importABsBtn.setStyleSheet(u"QPushButton {\n"
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
        icon20 = QIcon()
        icon20.addFile(u":/icons/assets/file.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.importABsBtn.setIcon(icon20)

        self.horizontalLayout_19.addWidget(self.importABsBtn)

        self.absFileLE = QLineEdit(self.frame_20)
        self.absFileLE.setObjectName(u"absFileLE")
        self.absFileLE.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"")
        self.absFileLE.setReadOnly(True)

        self.horizontalLayout_19.addWidget(self.absFileLE)

        self.dispatchBtn = QPushButton(self.frame_20)
        self.dispatchBtn.setObjectName(u"dispatchBtn")
        sizePolicy2.setHeightForWidth(self.dispatchBtn.sizePolicy().hasHeightForWidth())
        self.dispatchBtn.setSizePolicy(sizePolicy2)
        self.dispatchBtn.setMinimumSize(QSize(100, 30))
        self.dispatchBtn.setMaximumSize(QSize(100, 30))
        self.dispatchBtn.setStyleSheet(u"QPushButton {\n"
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
        icon21 = QIcon()
        icon21.addFile(u":/icons/assets/run.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.dispatchBtn.setIcon(icon21)

        self.horizontalLayout_19.addWidget(self.dispatchBtn)


        self.verticalLayout_30.addWidget(self.frame_20)

        self.tabWidget.addTab(self.linePage, "")

        self.verticalLayout_21.addWidget(self.tabWidget)

        self.container.addWidget(self.outsidePage)
        self.insidePage = QWidget()
        self.insidePage.setObjectName(u"insidePage")
        self.verticalLayout_26 = QVBoxLayout(self.insidePage)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.frame_24 = QFrame(self.insidePage)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 50))
        self.frame_24.setMaximumSize(QSize(16777215, 50))
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_39 = QLabel(self.frame_24)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMinimumSize(QSize(100, 30))
        self.label_39.setMaximumSize(QSize(100, 30))
        self.label_39.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_39.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_23.addWidget(self.label_39)

        self.oltKeywordLE = QLineEdit(self.frame_24)
        self.oltKeywordLE.setObjectName(u"oltKeywordLE")
        sizePolicy6.setHeightForWidth(self.oltKeywordLE.sizePolicy().hasHeightForWidth())
        self.oltKeywordLE.setSizePolicy(sizePolicy6)
        self.oltKeywordLE.setMinimumSize(QSize(300, 30))
        self.oltKeywordLE.setMaximumSize(QSize(300, 30))
        self.oltKeywordLE.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(28, 33, 44, 255);\n"
"    color: #44cc88;\n"
"    border: 1px solid #44cc88;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #55dd99;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #66eeaa;\n"
"}\n"
"")

        self.horizontalLayout_23.addWidget(self.oltKeywordLE)

        self.oltSiteNamesCB = QComboBox(self.frame_24)
        self.oltSiteNamesCB.setObjectName(u"oltSiteNamesCB")
        sizePolicy.setHeightForWidth(self.oltSiteNamesCB.sizePolicy().hasHeightForWidth())
        self.oltSiteNamesCB.setSizePolicy(sizePolicy)
        self.oltSiteNamesCB.setMinimumSize(QSize(150, 30))
        self.oltSiteNamesCB.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_23.addWidget(self.oltSiteNamesCB)

        self.searchOltBtn = QPushButton(self.frame_24)
        self.searchOltBtn.setObjectName(u"searchOltBtn")
        sizePolicy10.setHeightForWidth(self.searchOltBtn.sizePolicy().hasHeightForWidth())
        self.searchOltBtn.setSizePolicy(sizePolicy10)
        self.searchOltBtn.setMinimumSize(QSize(100, 30))
        self.searchOltBtn.setMaximumSize(QSize(100, 30))
        self.searchOltBtn.setStyleSheet(u"QPushButton {\n"
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
        self.searchOltBtn.setIcon(icon15)

        self.horizontalLayout_23.addWidget(self.searchOltBtn)


        self.verticalLayout_26.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.insidePage)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setStyleSheet(u"")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.oltNeTw = QTableWidget(self.frame_25)
        self.oltNeTw.setObjectName(u"oltNeTw")
        sizePolicy6.setHeightForWidth(self.oltNeTw.sizePolicy().hasHeightForWidth())
        self.oltNeTw.setSizePolicy(sizePolicy6)
        self.oltNeTw.setMinimumSize(QSize(0, 129))
        self.oltNeTw.setMaximumSize(QSize(16777215, 129))
        self.oltNeTw.setStyleSheet(u"QTableWidget {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        gridline-color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"    }\n"
"    \n"
"    QTableWidget::item {\n"
"        border: none;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableWidget::item:selected {\n"
"        background-color: #44cc88;\n"
"        color: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QHeaderView::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        color: #44cc88;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"    }\n"
"    \n"
"    QTableCornerButton::section {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"    }")

        self.horizontalLayout_24.addWidget(self.oltNeTw)

        self.label_40 = QLabel(self.frame_25)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(80, 129))
        self.label_40.setMaximumSize(QSize(80, 129))
        self.label_40.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_40.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.label_40)


        self.verticalLayout_26.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.insidePage)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.portUsePie = PieChartView(self.frame_26)
        self.portUsePie.setObjectName(u"portUsePie")
        self.portUsePie.setStyleSheet(u"QGraphicsView {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    /* \u6eda\u52a8\u6761\u6837\u5f0f */\n"
"    QScrollBar:horizontal {\n"
"        height: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar:vertical {\n"
"        width: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar::handle {\n"
"        background: #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    QScrollBar::add-line, QScrollBar::sub-line {\n"
"        background: none;\n"
"    }")

        self.horizontalLayout_25.addWidget(self.portUsePie)

        self.xgPortUsePie = PieChartView(self.frame_26)
        self.xgPortUsePie.setObjectName(u"xgPortUsePie")
        self.xgPortUsePie.setStyleSheet(u"QGraphicsView {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    /* \u6eda\u52a8\u6761\u6837\u5f0f */\n"
"    QScrollBar:horizontal {\n"
"        height: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar:vertical {\n"
"        width: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar::handle {\n"
"        background: #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    QScrollBar::add-line, QScrollBar::sub-line {\n"
"        background: none;\n"
"    }")

        self.horizontalLayout_25.addWidget(self.xgPortUsePie)

        self.oltBoardView = OltBoardView(self.frame_26)
        self.oltBoardView.setObjectName(u"oltBoardView")
        self.oltBoardView.setStyleSheet(u"QGraphicsView {\n"
"        background-color: rgba(28, 33, 44, 255);\n"
"        border: 1px solid #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    /* \u6eda\u52a8\u6761\u6837\u5f0f */\n"
"    QScrollBar:horizontal {\n"
"        height: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar:vertical {\n"
"        width: 10px;\n"
"        background: rgba(28, 33, 44, 255);\n"
"    }\n"
"    \n"
"    QScrollBar::handle {\n"
"        background: #44cc88;\n"
"        border-radius: 5px;\n"
"    }\n"
"    \n"
"    QScrollBar::add-line, QScrollBar::sub-line {\n"
"        background: none;\n"
"    }")

        self.horizontalLayout_25.addWidget(self.oltBoardView)

        self.horizontalLayout_25.setStretch(0, 1)
        self.horizontalLayout_25.setStretch(1, 1)
        self.horizontalLayout_25.setStretch(2, 2)

        self.verticalLayout_26.addWidget(self.frame_26)

        self.container.addWidget(self.insidePage)
        self.logPage = QWidget()
        self.logPage.setObjectName(u"logPage")
        self.verticalLayout_31 = QVBoxLayout(self.logPage)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(-1, -1, 20, -1)
        self.label_43 = QLabel(self.logPage)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_43.setAlignment(Qt.AlignCenter)

        self.verticalLayout_31.addWidget(self.label_43)

        self.logTE = QTextEdit(self.logPage)
        self.logTE.setObjectName(u"logTE")
        self.logTE.setStyleSheet(u"QTextEdit {\n"
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

        self.verticalLayout_31.addWidget(self.logTE)

        self.container.addWidget(self.logPage)
        self.toolPage = QWidget()
        self.toolPage.setObjectName(u"toolPage")
        self.verticalLayout_32 = QVBoxLayout(self.toolPage)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.frame_32 = QFrame(self.toolPage)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMinimumSize(QSize(0, 60))
        self.frame_32.setMaximumSize(QSize(16777215, 60))
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_44 = QLabel(self.frame_32)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(300, 0))
        self.label_44.setMaximumSize(QSize(300, 16777215))
        self.label_44.setStyleSheet(u"QLabel {\n"
"    background-color: #44cc88;  /* \u7eff\u8272\u80cc\u666f */\n"
"    color: white;  /* \u767d\u8272\u6587\u5b57 */\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.label_44.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_30.addWidget(self.label_44)


        self.verticalLayout_32.addWidget(self.frame_32)

        self.frame_31 = QFrame(self.toolPage)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_31)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.writeAggrHouseBtn_2 = QPushButton(self.frame_31)
        self.writeAggrHouseBtn_2.setObjectName(u"writeAggrHouseBtn_2")
        sizePolicy2.setHeightForWidth(self.writeAggrHouseBtn_2.sizePolicy().hasHeightForWidth())
        self.writeAggrHouseBtn_2.setSizePolicy(sizePolicy2)
        self.writeAggrHouseBtn_2.setMinimumSize(QSize(100, 100))
        self.writeAggrHouseBtn_2.setMaximumSize(QSize(100, 100))
        self.writeAggrHouseBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.writeAggrHouseBtn_2, 0, 0, 1, 1)

        self.redOltPortSiteBtn_2 = QPushButton(self.frame_31)
        self.redOltPortSiteBtn_2.setObjectName(u"redOltPortSiteBtn_2")
        sizePolicy2.setHeightForWidth(self.redOltPortSiteBtn_2.sizePolicy().hasHeightForWidth())
        self.redOltPortSiteBtn_2.setSizePolicy(sizePolicy2)
        self.redOltPortSiteBtn_2.setMinimumSize(QSize(100, 100))
        self.redOltPortSiteBtn_2.setMaximumSize(QSize(100, 100))
        self.redOltPortSiteBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.redOltPortSiteBtn_2, 0, 1, 1, 1)

        self.notOltAggrSiteBtn_2 = QPushButton(self.frame_31)
        self.notOltAggrSiteBtn_2.setObjectName(u"notOltAggrSiteBtn_2")
        sizePolicy2.setHeightForWidth(self.notOltAggrSiteBtn_2.sizePolicy().hasHeightForWidth())
        self.notOltAggrSiteBtn_2.setSizePolicy(sizePolicy2)
        self.notOltAggrSiteBtn_2.setMinimumSize(QSize(100, 100))
        self.notOltAggrSiteBtn_2.setMaximumSize(QSize(100, 100))
        self.notOltAggrSiteBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.notOltAggrSiteBtn_2, 0, 2, 1, 1)

        self.notXgOltBtn_2 = QPushButton(self.frame_31)
        self.notXgOltBtn_2.setObjectName(u"notXgOltBtn_2")
        sizePolicy2.setHeightForWidth(self.notXgOltBtn_2.sizePolicy().hasHeightForWidth())
        self.notXgOltBtn_2.setSizePolicy(sizePolicy2)
        self.notXgOltBtn_2.setMinimumSize(QSize(100, 100))
        self.notXgOltBtn_2.setMaximumSize(QSize(100, 100))
        self.notXgOltBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.notXgOltBtn_2, 0, 3, 1, 1)

        self.blueAggrSiteBtn_2 = QPushButton(self.frame_31)
        self.blueAggrSiteBtn_2.setObjectName(u"blueAggrSiteBtn_2")
        sizePolicy2.setHeightForWidth(self.blueAggrSiteBtn_2.sizePolicy().hasHeightForWidth())
        self.blueAggrSiteBtn_2.setSizePolicy(sizePolicy2)
        self.blueAggrSiteBtn_2.setMinimumSize(QSize(100, 100))
        self.blueAggrSiteBtn_2.setMaximumSize(QSize(100, 100))
        self.blueAggrSiteBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.blueAggrSiteBtn_2, 0, 4, 1, 1)

        self.boxUplinkBusyBtn_2 = QPushButton(self.frame_31)
        self.boxUplinkBusyBtn_2.setObjectName(u"boxUplinkBusyBtn_2")
        sizePolicy2.setHeightForWidth(self.boxUplinkBusyBtn_2.sizePolicy().hasHeightForWidth())
        self.boxUplinkBusyBtn_2.setSizePolicy(sizePolicy2)
        self.boxUplinkBusyBtn_2.setMinimumSize(QSize(100, 100))
        self.boxUplinkBusyBtn_2.setMaximumSize(QSize(100, 100))
        self.boxUplinkBusyBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.boxUplinkBusyBtn_2, 1, 0, 1, 1)

        self.onuBtn_2 = QPushButton(self.frame_31)
        self.onuBtn_2.setObjectName(u"onuBtn_2")
        sizePolicy2.setHeightForWidth(self.onuBtn_2.sizePolicy().hasHeightForWidth())
        self.onuBtn_2.setSizePolicy(sizePolicy2)
        self.onuBtn_2.setMinimumSize(QSize(100, 100))
        self.onuBtn_2.setMaximumSize(QSize(100, 100))
        self.onuBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.onuBtn_2, 1, 1, 1, 1)

        self.ponLineProjectBtn_2 = QPushButton(self.frame_31)
        self.ponLineProjectBtn_2.setObjectName(u"ponLineProjectBtn_2")
        sizePolicy2.setHeightForWidth(self.ponLineProjectBtn_2.sizePolicy().hasHeightForWidth())
        self.ponLineProjectBtn_2.setSizePolicy(sizePolicy2)
        self.ponLineProjectBtn_2.setMinimumSize(QSize(100, 100))
        self.ponLineProjectBtn_2.setMaximumSize(QSize(100, 100))
        self.ponLineProjectBtn_2.setStyleSheet(u"QPushButton {\n"
"        background-color: rgb(58, 65, 82);\n"
"        color: #44cc88;\n"
"        border-radius: 15px;\n"
"        border: 1px solid #44cc88;\n"
"        padding: 5px;\n"
"        font: 700 11pt;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgb(70, 77, 94);\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgb(46, 53, 70);\n"
"    }")

        self.gridLayout_2.addWidget(self.ponLineProjectBtn_2, 1, 2, 1, 1)


        self.verticalLayout_32.addWidget(self.frame_31)

        self.container.addWidget(self.toolPage)

        self.verticalLayout.addWidget(self.container)

        self.bottomBar = QFrame(self.root)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 40))
        self.bottomBar.setMaximumSize(QSize(1000, 40))
        self.bottomBar.setFrameShape(QFrame.StyledPanel)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, 0, -1, -1)
        self.statusLabel = QLabel(self.bottomBar)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setMinimumSize(QSize(0, 30))
        self.statusLabel.setMaximumSize(QSize(16777215, 30))
        self.statusLabel.setStyleSheet(u"QLabel {\n"
"    color: #44cc88;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"	font-weight:700;\n"
"}")

        self.horizontalLayout_28.addWidget(self.statusLabel)


        self.verticalLayout.addWidget(self.bottomBar)


        self.horizontalLayout.addWidget(self.root)

        self.sideBar = QFrame(self.centralwidget)
        self.sideBar.setObjectName(u"sideBar")
        self.sideBar.setEnabled(True)
        sizePolicy.setHeightForWidth(self.sideBar.sizePolicy().hasHeightForWidth())
        self.sideBar.setSizePolicy(sizePolicy)
        self.sideBar.setMinimumSize(QSize(0, 0))
        self.sideBar.setMaximumSize(QSize(0, 1000))
        self.sideBar.setStyleSheet(u"background-color: #00000000;")
        self.sideBar.setFrameShape(QFrame.NoFrame)
        self.sideBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.sideBar)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.sideContainer = QFrame(self.sideBar)
        self.sideContainer.setObjectName(u"sideContainer")
        self.sideContainer.setStyleSheet(u"background-color: rgb(43, 50, 63);")
        self.sideContainer.setFrameShape(QFrame.StyledPanel)
        self.sideContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.sideContainer)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.inforTab = QFrame(self.sideContainer)
        self.inforTab.setObjectName(u"inforTab")
        self.inforTab.setMinimumSize(QSize(0, 150))
        self.inforTab.setMaximumSize(QSize(16777215, 150))
        self.inforTab.setStyleSheet(u"")
        self.inforTab.setFrameShape(QFrame.StyledPanel)
        self.inforTab.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.inforTab)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(20, 10, 20, 10)
        self.frame_13 = QFrame(self.inforTab)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 30))
        self.frame_13.setMaximumSize(QSize(16777215, 30))
        self.frame_13.setStyleSheet(u"")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.sideClose = QPushButton(self.frame_13)
        self.sideClose.setObjectName(u"sideClose")
        self.sideClose.setMinimumSize(QSize(20, 20))
        self.sideClose.setMaximumSize(QSize(20, 20))
        self.sideClose.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	border-radius: 10;\n"
"	background-color: rgb(104, 117, 147);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(64, 71, 90);\n"
"}")
        icon22 = QIcon()
        icon22.addFile(u":/icons/assets/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.sideClose.setIcon(icon22)

        self.horizontalLayout_10.addWidget(self.sideClose)

        self.horizontalSpacer_11 = QSpacerItem(301, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)


        self.verticalLayout_14.addWidget(self.frame_13)

        self.label_16 = QLabel(self.inforTab)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_14.addWidget(self.label_16)


        self.verticalLayout_13.addWidget(self.inforTab)

        self.contentFrame = QFrame(self.sideContainer)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setStyleSheet(u"padding-left: 20;")
        self.contentFrame.setFrameShape(QFrame.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.contentFrame)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.settingBtn = QPushButton(self.contentFrame)
        self.settingBtn.setObjectName(u"settingBtn")
        self.settingBtn.setMinimumSize(QSize(320, 40))
        self.settingBtn.setMaximumSize(QSize(320, 40))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.settingBtn.setFont(font3)
        self.settingBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	border-radius: 5;\n"
"	color: rgb(188, 188, 188);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        icon23 = QIcon()
        icon23.addFile(u":/icons/assets/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingBtn.setIcon(icon23)
        self.settingBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.settingBtn)

        self.updateBtn = QPushButton(self.contentFrame)
        self.updateBtn.setObjectName(u"updateBtn")
        self.updateBtn.setMinimumSize(QSize(320, 40))
        self.updateBtn.setMaximumSize(QSize(320, 40))
        self.updateBtn.setFont(font3)
        self.updateBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	border-radius: 5;\n"
"	color: rgb(188, 188, 188);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        icon24 = QIcon()
        icon24.addFile(u":/icons/assets/document.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.updateBtn.setIcon(icon24)
        self.updateBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.updateBtn)

        self.kpiBtn = QPushButton(self.contentFrame)
        self.kpiBtn.setObjectName(u"kpiBtn")
        self.kpiBtn.setMinimumSize(QSize(320, 40))
        self.kpiBtn.setMaximumSize(QSize(320, 40))
        self.kpiBtn.setFont(font3)
        self.kpiBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	border-radius: 5;\n"
"	color: rgb(188, 188, 188);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        icon25 = QIcon()
        icon25.addFile(u":/icons/assets/graph.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.kpiBtn.setIcon(icon25)
        self.kpiBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.kpiBtn)

        self.logBtn = QPushButton(self.contentFrame)
        self.logBtn.setObjectName(u"logBtn")
        self.logBtn.setMinimumSize(QSize(320, 40))
        self.logBtn.setMaximumSize(QSize(320, 40))
        self.logBtn.setFont(font3)
        self.logBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	border-radius: 5;\n"
"	color: rgb(188, 188, 188);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        icon26 = QIcon()
        icon26.addFile(u":/icons/assets/help.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.logBtn.setIcon(icon26)
        self.logBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.logBtn)

        self.aboutBtn = QPushButton(self.contentFrame)
        self.aboutBtn.setObjectName(u"aboutBtn")
        self.aboutBtn.setMinimumSize(QSize(320, 40))
        self.aboutBtn.setMaximumSize(QSize(320, 40))
        self.aboutBtn.setFont(font3)
        self.aboutBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	border-radius: 5;\n"
"	color: rgb(188, 188, 188);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        icon27 = QIcon()
        icon27.addFile(u":/icons/assets/about.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.aboutBtn.setIcon(icon27)
        self.aboutBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.aboutBtn)

        self.toolBtn = QPushButton(self.contentFrame)
        self.toolBtn.setObjectName(u"toolBtn")
        self.toolBtn.setMinimumSize(QSize(400, 40))
        self.toolBtn.setMaximumSize(QSize(400, 40))
        self.toolBtn.setFont(font3)
        self.toolBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(43, 50, 63);\n"
"	color: rgb(188, 188, 188);\n"
"	border-top: 1px solid rgb(165, 165, 165);\n"
"	text-align: left;\n"
"	padding-left: 5;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(74, 80, 96);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(34, 40, 50);\n"
"}")
        self.toolBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_15.addWidget(self.toolBtn)


        self.verticalLayout_13.addWidget(self.contentFrame)


        self.horizontalLayout_9.addWidget(self.sideContainer)


        self.horizontalLayout.addWidget(self.sideBar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.container.setCurrentIndex(8)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4f20\u8f93\u7f51\u667a\u80fd\u8bca\u65ad\u5de5\u5177", None))
        self.pushButton.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:700; color:#ffffff;\">\u6e5b\u6c5f\u79fb\u52a8 </span><span style=\" font-size:12pt; color:#44cc88;\">\u4f20\u8f93\u7f51\u7edc\u7ef4\u62a4</span></p></body></html>", None))
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.menuBtn.setText(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
        self.miniBtn.setText("")
        self.closeBtn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">\u4f20\u8f93\u7f51     </span><span style=\" font-size:24pt; font-weight:700; color:#44cc88;\">\u667a\u80fd\u8bca\u65ad\u5de5\u5177 </span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; color:#ffffff;\">\u5feb\u901f\u67e5\u8be2</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; color:#ffffff;\">\u4e2a\u6027\u5316\u8bca\u65ad</span></p></body></html>", None))
        self.outsideBtn.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; color:#e8e8e8;\">\u5916\u7ebf</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; color:#43c485;\">\u7ba1\u7ebf\u8bbe\u65bd</span></p></body></html>", None))
        self.insideBtn.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; color:#e3e3e3;\">\u5185\u7ebf</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; color:#43c485;\">PON</span></p></body></html>", None))
        self.odevBtn.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; color:#cacaca;\">\u5149\u8bbe\u65bd</span></p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#c3c3c3;\">\u5149\u4ea4\u7bb1 \u5206\u7ea4\u7bb1</span></p></body></html>", None))
        self.oltBtn.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; color:#cacaca;\">OLT\u8bbe\u5907</span></p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#c3c3c3;\">\u7aef\u53e3 \u69fd\u4f4d</span></p></body></html>", None))
        self.linkBtn.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; color:#cacaca;\">\u4e3b\u5149\u8def</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; color:#c3c3c3;\">\u8d85\u957f \u8de8\u533a</span></p></body></html>", None))
        self.dbmsBtn.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93\u7ba1\u7406", None))
        self.choseFileBtn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.updateDataBaseBtn.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u6570\u636e", None))
        self.muti_file_cb.setText(QCoreApplication.translate("MainWindow", u"\u591a\u4e2a\u6587\u4ef6", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5217\u540d\u884c\u53f7\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.analysisLabel.setText(QCoreApplication.translate("MainWindow", u"\u3010\u6d4b\u8bd5\u3011", None))
        self.checkTableBtn.setText(QCoreApplication.translate("MainWindow", u"\u8868\u6821\u9a8c", None))
        self.runAnalysisBtn.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c\u5206\u6790", None))
        self.needTime.setText(QCoreApplication.translate("MainWindow", u"\u5269\u4f59\u65f6\u95f4\uff1a", None))
        self.dbTableBtn.setText(QCoreApplication.translate("MainWindow", u"\u8868\u67e5\u8be2", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u3010\u5feb\u901f\u62a5\u8868\u3011", None))
        self.writeAggrHouseBtn.setText(QCoreApplication.translate("MainWindow", u"\u6c47\u805a\u673a\u623f\n"
"\u8986\u76d6\u8bc4\u4f30", None))
        self.redOltPortSiteBtn.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3\u9884\u8b66\n"
"OLT\u7ad9\u70b9", None))
        self.notOltAggrSiteBtn.setText(QCoreApplication.translate("MainWindow", u"\u672a\u90e8\u7f72OLT\n"
"\u6c47\u805a\u7ad9\u70b9", None))
        self.notXgOltBtn.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u8986\u76d6\u5343\u5146\n"
"\u8d85\u5343\u6237\u7ad9\u70b9", None))
        self.blueAggrSiteBtn.setText(QCoreApplication.translate("MainWindow", u"\u4f4e\u7528\u6237\n"
"\u6c47\u805a\u7ad9\u70b9", None))
        self.boxUplinkBusyBtn.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u8054\u7ea4\u82af\n"
"\u7d27\u5f20\u7bb1\u4f53", None))
        self.onuBtn.setText(QCoreApplication.translate("MainWindow", u"ONU\u5f31\u5149\n"
"\u8c03\u4f18\u5206\u6790", None))
        self.ponLineProjectBtn.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u6709\u7ba1\u9053\n"
"\u6746\u8def\u5206\u6790", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"\u5149\u4ea4\u7bb1/\u5206\u7ea4\u7bb1:", None))
        self.searchDevUplinkBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u627e", None))
        self.highScoreBtn.setText(QCoreApplication.translate("MainWindow", u"\u8bc4\u5206\u6700\u9ad8", None))
        self.dbmMinBtn.setText(QCoreApplication.translate("MainWindow", u"\u8870\u8017\u6700\u5c0f", None))
        self.numMaxBtn.setText(QCoreApplication.translate("MainWindow", u"\u82af\u6570\u6700\u5927", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"\u6587\u672c\n"
"\u8def\u7531", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"\u8def\u7531\n"
"\u62d3\u6251", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.oDevPage), QCoreApplication.translate("MainWindow", u"\u5149\u4ea4\u8bbe\u65bd", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u591a\u5173\u952e\u5b57\uff08\u7a7a\u683c\u9694\u5f00\uff09\uff1a", None))
        self.searchLineBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u627e", None))
        self.aSiteBtn.setText(QCoreApplication.translate("MainWindow", u"A\u7aef", None))
        self.bSiteBtn.setText(QCoreApplication.translate("MainWindow", u"B\u7aef", None))
        self.mustDevBtn.setText(QCoreApplication.translate("MainWindow", u"\u5fc5\u7ecf", None))
        self.notDevBtn.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u7ecf", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"A\u7aef", None))
        self.aSiteLabel.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"B\u7aef", None))
        self.bSiteLabel.setText("")
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u6570", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"\u8870\u8017", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"\u5fc5\u7ecf\u673a\u623f/\u5149\u4ea4\u8bbe\u65bd", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u7ecf\u673a\u623f/\u5149\u4ea4\u8bbe\u65bd", None))
        self.delMustDevBtn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u5fc5\u7ecf", None))
        self.delNotDevBtn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u4e0d\u7ecf", None))
        self.devToLeftBtn.setText("")
        self.devToRightBtn.setText("")
        self.importABsBtn.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42\u6587\u4ef6", None))
        self.dispatchBtn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linePage), QCoreApplication.translate("MainWindow", u"\u4e2d\u7ee7\u6bb5", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"OLT\u7ad9\u70b9", None))
        self.searchOltBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u627e", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u5143\n"
"\n"
"\u6e05\u5355", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u65e5\u5fd7", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u5177\u7bb1", None))
        self.writeAggrHouseBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u5750\u6807\u7cfb\n"
"\u8f6c\u6362", None))
        self.redOltPortSiteBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u5c42\n"
"\u89e3\u6790", None))
        self.notOltAggrSiteBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u5c42\n"
"\u751f\u6210", None))
        self.notXgOltBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u70ed\u529b\u56fe\n"
"\u7ed8\u5236", None))
        self.blueAggrSiteBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u533a\u57df\n"
"\u5f52\u5c5e", None))
        self.boxUplinkBusyBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\n"
"\u63a2\u9488", None))
        self.onuBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u7cca\n"
"\u5339\u914d", None))
        self.ponLineProjectBtn_2.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u7eed", None))
        self.statusLabel.setText("")
        self.sideClose.setText("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700; color:#ffffff;\">\u4f7f\u7528\u8bf4\u660e</span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:700; color:#ffffff;\">\u9700\u5468\u671f\u66f4\u65b0\u6570\u636e </span></p></body></html>", None))
        self.settingBtn.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.updateBtn.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\u6570\u636e\u66f4\u65b0", None))
        self.kpiBtn.setText(QCoreApplication.translate("MainWindow", u"\u6307\u6807\u6570\u636e", None))
        self.logBtn.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.aboutBtn.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.toolBtn.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u5177\u7bb1", None))
    # retranslateUi

