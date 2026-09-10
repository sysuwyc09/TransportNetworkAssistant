# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TransportPredict.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFormLayout, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTableView, QTextEdit, QVBoxLayout,
    QWidget)
import resources_rc.py_rc

class Ui_TransportPredict(object):
    def setupUi(self, TransportPredict):
        if not TransportPredict.objectName():
            TransportPredict.setObjectName(u"TransportPredict")
        TransportPredict.resize(1100, 720)
        icon = QIcon()
        icon.addFile(u":/icons/assets/olt.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TransportPredict.setWindowIcon(icon)
        self.centralwidget = QWidget(TransportPredict)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutMain = QVBoxLayout(self.centralwidget)
        self.verticalLayoutMain.setObjectName(u"verticalLayoutMain")
        self.verticalLayoutMain.setContentsMargins(8, 8, 8, 8)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(False)
        self.tabDataInput = QWidget()
        self.tabDataInput.setObjectName(u"tabDataInput")
        self.verticalLayoutDataInput = QVBoxLayout(self.tabDataInput)
        self.verticalLayoutDataInput.setObjectName(u"verticalLayoutDataInput")
        self.labelDataInputTitle = QLabel(self.tabDataInput)
        self.labelDataInputTitle.setObjectName(u"labelDataInputTitle")
        self.labelDataInputTitle.setTextFormat(Qt.RichText)

        self.verticalLayoutDataInput.addWidget(self.labelDataInputTitle)

        self.labelConnStatus = QLabel(self.tabDataInput)
        self.labelConnStatus.setObjectName(u"labelConnStatus")

        self.verticalLayoutDataInput.addWidget(self.labelConnStatus)

        self.horizontalLayoutConn = QHBoxLayout()
        self.horizontalLayoutConn.setObjectName(u"horizontalLayoutConn")
        self.btnTestConn = QPushButton(self.tabDataInput)
        self.btnTestConn.setObjectName(u"btnTestConn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/assets/link.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnTestConn.setIcon(icon1)

        self.horizontalLayoutConn.addWidget(self.btnTestConn)

        self.btnLoadOBD = QPushButton(self.tabDataInput)
        self.btnLoadOBD.setObjectName(u"btnLoadOBD")
        icon2 = QIcon()
        icon2.addFile(u":/icons/assets/box.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnLoadOBD.setIcon(icon2)

        self.horizontalLayoutConn.addWidget(self.btnLoadOBD)

        self.btnLoadOLT = QPushButton(self.tabDataInput)
        self.btnLoadOLT.setObjectName(u"btnLoadOLT")
        self.btnLoadOLT.setIcon(icon)

        self.horizontalLayoutConn.addWidget(self.btnLoadOLT)

        self.horizontalSpacerConn = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutConn.addItem(self.horizontalSpacerConn)


        self.verticalLayoutDataInput.addLayout(self.horizontalLayoutConn)

        self.labelDataSummary = QLabel(self.tabDataInput)
        self.labelDataSummary.setObjectName(u"labelDataSummary")

        self.verticalLayoutDataInput.addWidget(self.labelDataSummary)

        self.labelTableTitle = QLabel(self.tabDataInput)
        self.labelTableTitle.setObjectName(u"labelTableTitle")

        self.verticalLayoutDataInput.addWidget(self.labelTableTitle)

        self.tableViewData = QTableView(self.tabDataInput)
        self.tableViewData.setObjectName(u"tableViewData")
        self.tableViewData.setAlternatingRowColors(True)
        self.tableViewData.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableViewData.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayoutDataInput.addWidget(self.tableViewData)

        icon3 = QIcon()
        icon3.addFile(u":/icons/assets/database.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tabDataInput, icon3, "")
        self.tabDataProcess = QWidget()
        self.tabDataProcess.setObjectName(u"tabDataProcess")
        self.verticalLayoutDataProcess = QVBoxLayout(self.tabDataProcess)
        self.verticalLayoutDataProcess.setObjectName(u"verticalLayoutDataProcess")
        self.labelDataProcessTitle = QLabel(self.tabDataProcess)
        self.labelDataProcessTitle.setObjectName(u"labelDataProcessTitle")
        self.labelDataProcessTitle.setTextFormat(Qt.RichText)

        self.verticalLayoutDataProcess.addWidget(self.labelDataProcessTitle)

        self.horizontalLayoutProcess = QHBoxLayout()
        self.horizontalLayoutProcess.setObjectName(u"horizontalLayoutProcess")
        self.btnProcessData = QPushButton(self.tabDataProcess)
        self.btnProcessData.setObjectName(u"btnProcessData")
        icon4 = QIcon()
        icon4.addFile(u":/icons/assets/run.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnProcessData.setIcon(icon4)

        self.horizontalLayoutProcess.addWidget(self.btnProcessData)

        self.labelObdSummary = QLabel(self.tabDataProcess)
        self.labelObdSummary.setObjectName(u"labelObdSummary")

        self.horizontalLayoutProcess.addWidget(self.labelObdSummary)

        self.horizontalSpacerProcess = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutProcess.addItem(self.horizontalSpacerProcess)


        self.verticalLayoutDataProcess.addLayout(self.horizontalLayoutProcess)

        self.labelPonStatsTitle = QLabel(self.tabDataProcess)
        self.labelPonStatsTitle.setObjectName(u"labelPonStatsTitle")

        self.verticalLayoutDataProcess.addWidget(self.labelPonStatsTitle)

        self.tableViewPonStats = QTableView(self.tabDataProcess)
        self.tableViewPonStats.setObjectName(u"tableViewPonStats")
        self.tableViewPonStats.setAlternatingRowColors(True)
        self.tableViewPonStats.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableViewPonStats.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayoutDataProcess.addWidget(self.tableViewPonStats)

        self.labelChartUtil = QLabel(self.tabDataProcess)
        self.labelChartUtil.setObjectName(u"labelChartUtil")

        self.verticalLayoutDataProcess.addWidget(self.labelChartUtil)

        self.widgetChartUtil = QWidget(self.tabDataProcess)
        self.widgetChartUtil.setObjectName(u"widgetChartUtil")

        self.verticalLayoutDataProcess.addWidget(self.widgetChartUtil)

        icon5 = QIcon()
        icon5.addFile(u":/icons/assets/fiber.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tabDataProcess, icon5, "")
        self.tabModelTrain = QWidget()
        self.tabModelTrain.setObjectName(u"tabModelTrain")
        self.verticalLayoutModelTrain = QVBoxLayout(self.tabModelTrain)
        self.verticalLayoutModelTrain.setObjectName(u"verticalLayoutModelTrain")
        self.labelModelTrainTitle = QLabel(self.tabModelTrain)
        self.labelModelTrainTitle.setObjectName(u"labelModelTrainTitle")
        self.labelModelTrainTitle.setTextFormat(Qt.RichText)

        self.verticalLayoutModelTrain.addWidget(self.labelModelTrainTitle)

        self.formLayoutParams = QFormLayout()
        self.formLayoutParams.setObjectName(u"formLayoutParams")
        self.labelNEstimators = QLabel(self.tabModelTrain)
        self.labelNEstimators.setObjectName(u"labelNEstimators")

        self.formLayoutParams.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelNEstimators)

        self.spinNEstimators = QSpinBox(self.tabModelTrain)
        self.spinNEstimators.setObjectName(u"spinNEstimators")
        self.spinNEstimators.setMinimum(10)
        self.spinNEstimators.setMaximum(1000)
        self.spinNEstimators.setValue(100)

        self.formLayoutParams.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spinNEstimators)

        self.labelMaxDepth = QLabel(self.tabModelTrain)
        self.labelMaxDepth.setObjectName(u"labelMaxDepth")

        self.formLayoutParams.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelMaxDepth)

        self.spinMaxDepth = QSpinBox(self.tabModelTrain)
        self.spinMaxDepth.setObjectName(u"spinMaxDepth")
        self.spinMaxDepth.setMinimum(0)
        self.spinMaxDepth.setMaximum(50)
        self.spinMaxDepth.setValue(0)

        self.formLayoutParams.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spinMaxDepth)

        self.labelRandomState = QLabel(self.tabModelTrain)
        self.labelRandomState.setObjectName(u"labelRandomState")

        self.formLayoutParams.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelRandomState)

        self.spinRandomState = QSpinBox(self.tabModelTrain)
        self.spinRandomState.setObjectName(u"spinRandomState")
        self.spinRandomState.setMinimum(0)
        self.spinRandomState.setMaximum(99999)
        self.spinRandomState.setValue(42)

        self.formLayoutParams.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spinRandomState)


        self.verticalLayoutModelTrain.addLayout(self.formLayoutParams)

        self.horizontalLayoutTrain = QHBoxLayout()
        self.horizontalLayoutTrain.setObjectName(u"horizontalLayoutTrain")
        self.btnTrainModel = QPushButton(self.tabModelTrain)
        self.btnTrainModel.setObjectName(u"btnTrainModel")
        self.btnTrainModel.setIcon(icon4)

        self.horizontalLayoutTrain.addWidget(self.btnTrainModel)

        self.progressBarTrain = QProgressBar(self.tabModelTrain)
        self.progressBarTrain.setObjectName(u"progressBarTrain")
        self.progressBarTrain.setValue(0)

        self.horizontalLayoutTrain.addWidget(self.progressBarTrain)

        self.horizontalSpacerTrain = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutTrain.addItem(self.horizontalSpacerTrain)


        self.verticalLayoutModelTrain.addLayout(self.horizontalLayoutTrain)

        self.labelMetrics = QLabel(self.tabModelTrain)
        self.labelMetrics.setObjectName(u"labelMetrics")

        self.verticalLayoutModelTrain.addWidget(self.labelMetrics)

        self.labelFeatureImpTitle = QLabel(self.tabModelTrain)
        self.labelFeatureImpTitle.setObjectName(u"labelFeatureImpTitle")

        self.verticalLayoutModelTrain.addWidget(self.labelFeatureImpTitle)

        self.widgetChartFeatureImp = QWidget(self.tabModelTrain)
        self.widgetChartFeatureImp.setObjectName(u"widgetChartFeatureImp")

        self.verticalLayoutModelTrain.addWidget(self.widgetChartFeatureImp)

        icon6 = QIcon()
        icon6.addFile(u":/icons/assets/computer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tabModelTrain, icon6, "")
        self.tabResultPredict = QWidget()
        self.tabResultPredict.setObjectName(u"tabResultPredict")
        self.verticalLayoutResultPredict = QVBoxLayout(self.tabResultPredict)
        self.verticalLayoutResultPredict.setObjectName(u"verticalLayoutResultPredict")
        self.labelResultTitle = QLabel(self.tabResultPredict)
        self.labelResultTitle.setObjectName(u"labelResultTitle")
        self.labelResultTitle.setTextFormat(Qt.RichText)

        self.verticalLayoutResultPredict.addWidget(self.labelResultTitle)

        self.horizontalLayoutPredict = QHBoxLayout()
        self.horizontalLayoutPredict.setObjectName(u"horizontalLayoutPredict")
        self.btnPredict = QPushButton(self.tabResultPredict)
        self.btnPredict.setObjectName(u"btnPredict")
        icon7 = QIcon()
        icon7.addFile(u":/icons/assets/checkmark.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnPredict.setIcon(icon7)

        self.horizontalLayoutPredict.addWidget(self.btnPredict)

        self.btnExportCSV = QPushButton(self.tabResultPredict)
        self.btnExportCSV.setObjectName(u"btnExportCSV")
        icon8 = QIcon()
        icon8.addFile(u":/icons/assets/file.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnExportCSV.setIcon(icon8)

        self.horizontalLayoutPredict.addWidget(self.btnExportCSV)

        self.horizontalSpacerPredict = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutPredict.addItem(self.horizontalSpacerPredict)


        self.verticalLayoutResultPredict.addLayout(self.horizontalLayoutPredict)

        self.labelResultTableTitle = QLabel(self.tabResultPredict)
        self.labelResultTableTitle.setObjectName(u"labelResultTableTitle")

        self.verticalLayoutResultPredict.addWidget(self.labelResultTableTitle)

        self.tableViewResult = QTableView(self.tabResultPredict)
        self.tableViewResult.setObjectName(u"tableViewResult")
        self.tableViewResult.setAlternatingRowColors(True)
        self.tableViewResult.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableViewResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayoutResultPredict.addWidget(self.tableViewResult)

        self.labelAdviceTitle = QLabel(self.tabResultPredict)
        self.labelAdviceTitle.setObjectName(u"labelAdviceTitle")

        self.verticalLayoutResultPredict.addWidget(self.labelAdviceTitle)

        self.textEditAdvice = QTextEdit(self.tabResultPredict)
        self.textEditAdvice.setObjectName(u"textEditAdvice")
        self.textEditAdvice.setReadOnly(True)

        self.verticalLayoutResultPredict.addWidget(self.textEditAdvice)

        icon9 = QIcon()
        icon9.addFile(u":/icons/assets/graph.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tabResultPredict, icon9, "")

        self.verticalLayoutMain.addWidget(self.tabWidget)

        TransportPredict.setCentralWidget(self.centralwidget)

        self.retranslateUi(TransportPredict)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TransportPredict)
    # setupUi

    def retranslateUi(self, TransportPredict):
        TransportPredict.setWindowTitle(QCoreApplication.translate("TransportPredict", u"\u4f20\u8f93\u8d44\u6e90\u9884\u6d4b - OLT PON \u53e3\u9700\u6c42\u9884\u6d4b", None))
        self.labelDataInputTitle.setText(QCoreApplication.translate("TransportPredict", u"<h2>\u6570\u636e\u8f93\u5165 - \u52a0\u8f7d OBD / OLT \u6570\u636e</h2>", None))
        self.labelConnStatus.setText(QCoreApplication.translate("TransportPredict", u"\u6570\u636e\u5e93\u8fde\u63a5\u72b6\u6001\uff1a\u672a\u8fde\u63a5", None))
        self.btnTestConn.setText(QCoreApplication.translate("TransportPredict", u"\u6d4b\u8bd5\u8fde\u63a5", None))
        self.btnLoadOBD.setText(QCoreApplication.translate("TransportPredict", u"\u52a0\u8f7d OBD \u6570\u636e", None))
        self.btnLoadOLT.setText(QCoreApplication.translate("TransportPredict", u"\u52a0\u8f7d OLT \u6570\u636e", None))
        self.labelDataSummary.setText(QCoreApplication.translate("TransportPredict", u"\u6570\u636e\u6458\u8981\uff1a\u672a\u52a0\u8f7d", None))
        self.labelTableTitle.setText(QCoreApplication.translate("TransportPredict", u"\u6570\u636e\u9884\u89c8\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDataInput), QCoreApplication.translate("TransportPredict", u"\u6570\u636e\u8f93\u5165", None))
        self.labelDataProcessTitle.setText(QCoreApplication.translate("TransportPredict", u"<h2>\u6570\u636e\u5904\u7406 - OBD \u5206\u7c7b\u4e0e PON \u53e3\u805a\u5408</h2>", None))
        self.btnProcessData.setText(QCoreApplication.translate("TransportPredict", u"\u6267\u884c\u6570\u636e\u5904\u7406", None))
        self.labelObdSummary.setText(QCoreApplication.translate("TransportPredict", u"OBD \u6458\u8981\uff1a\u672a\u5904\u7406", None))
        self.labelPonStatsTitle.setText(QCoreApplication.translate("TransportPredict", u"PON \u53e3\u5229\u7528\u7387\u7edf\u8ba1\uff1a", None))
        self.labelChartUtil.setText(QCoreApplication.translate("TransportPredict", u"\u7aef\u5b50\u5229\u7528\u7387\u5206\u5e03\u56fe\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDataProcess), QCoreApplication.translate("TransportPredict", u"\u6570\u636e\u5904\u7406", None))
        self.labelModelTrainTitle.setText(QCoreApplication.translate("TransportPredict", u"<h2>\u6a21\u578b\u8bad\u7ec3 - \u968f\u673a\u68ee\u6797\u56de\u5f52</h2>", None))
        self.labelNEstimators.setText(QCoreApplication.translate("TransportPredict", u"n_estimators (\u6811\u6570\u91cf)\uff1a", None))
        self.labelMaxDepth.setText(QCoreApplication.translate("TransportPredict", u"max_depth (\u6700\u5927\u6df1\u5ea6, 0=\u4e0d\u9650)\uff1a", None))
        self.spinMaxDepth.setSpecialValueText(QCoreApplication.translate("TransportPredict", u"\u4e0d\u9650", None))
        self.labelRandomState.setText(QCoreApplication.translate("TransportPredict", u"random_state (\u968f\u673a\u79cd\u5b50)\uff1a", None))
        self.btnTrainModel.setText(QCoreApplication.translate("TransportPredict", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.labelMetrics.setText(QCoreApplication.translate("TransportPredict", u"\u8bc4\u4f30\u6307\u6807\uff1a\u672a\u8bad\u7ec3", None))
        self.labelFeatureImpTitle.setText(QCoreApplication.translate("TransportPredict", u"\u7279\u5f81\u91cd\u8981\u6027\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabModelTrain), QCoreApplication.translate("TransportPredict", u"\u6a21\u578b\u8bad\u7ec3", None))
        self.labelResultTitle.setText(QCoreApplication.translate("TransportPredict", u"<h2>\u7ed3\u679c\u9884\u6d4b - OLT \u7ad9\u70b9 PON \u53e3\u6269\u5bb9\u5efa\u8bae</h2>", None))
        self.btnPredict.setText(QCoreApplication.translate("TransportPredict", u"\u6267\u884c\u9884\u6d4b", None))
        self.btnExportCSV.setText(QCoreApplication.translate("TransportPredict", u"\u5bfc\u51fa CSV", None))
        self.labelResultTableTitle.setText(QCoreApplication.translate("TransportPredict", u"OLT \u7ad9\u70b9\u6269\u5bb9\u5efa\u8bae\u6c47\u603b\uff1a", None))
        self.labelAdviceTitle.setText(QCoreApplication.translate("TransportPredict", u"\u8be6\u7ec6\u5efa\u8bae\uff1a", None))
        self.textEditAdvice.setHtml(QCoreApplication.translate("TransportPredict", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\"><html><head/><body><p>\u5c1a\u672a\u6267\u884c\u9884\u6d4b\u3002</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultPredict), QCoreApplication.translate("TransportPredict", u"\u7ed3\u679c\u9884\u6d4b", None))
    # retranslateUi

