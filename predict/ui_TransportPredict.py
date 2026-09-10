# -*- coding: utf-8 -*-
"""
UI Python 实现 - TransportPredict.ui 对应文件
由 Qt Designer .ui 文件手工转译而来（PySide6）。
"""
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_TransportPredict(object):
    """TransportPredict 主窗口 UI 类。"""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TransportPredict")
        MainWindow.resize(1100, 720)
        MainWindow.setWindowTitle("传输资源预测 - OLT PON 口需求预测")
        MainWindow.setWindowIcon(
            QtGui.QIcon(":/icons/assets/olt.svg")
        )

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutMain = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayoutMain.setObjectName("verticalLayoutMain")
        self.verticalLayoutMain.setContentsMargins(8, 8, 8, 8)

        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabsClosable(False)

        # ------------------------------------------------------------------
        # Tab 1 - 数据输入
        # ------------------------------------------------------------------
        self.tabDataInput = QtWidgets.QWidget()
        self.tabDataInput.setObjectName("tabDataInput")
        self.verticalLayoutDataInput = QtWidgets.QVBoxLayout(self.tabDataInput)
        self.verticalLayoutDataInput.setObjectName("verticalLayoutDataInput")

        self.labelDataInputTitle = QtWidgets.QLabel(parent=self.tabDataInput)
        self.labelDataInputTitle.setObjectName("labelDataInputTitle")
        self.labelDataInputTitle.setTextFormat(QtCore.Qt.RichText)
        self.labelDataInputTitle.setText(
            "<h2>数据输入 - 加载 OBD / OLT 数据</h2>"
        )
        self.verticalLayoutDataInput.addWidget(self.labelDataInputTitle)

        self.labelConnStatus = QtWidgets.QLabel(parent=self.tabDataInput)
        self.labelConnStatus.setObjectName("labelConnStatus")
        self.verticalLayoutDataInput.addWidget(self.labelConnStatus)

        self.horizontalLayoutConn = QtWidgets.QHBoxLayout()
        self.horizontalLayoutConn.setObjectName("horizontalLayoutConn")
        self.btnTestConn = QtWidgets.QPushButton(parent=self.tabDataInput)
        self.btnTestConn.setObjectName("btnTestConn")
        self.btnTestConn.setIcon(QtGui.QIcon(":/icons/assets/link.svg"))
        self.horizontalLayoutConn.addWidget(self.btnTestConn)
        self.btnLoadOBD = QtWidgets.QPushButton(parent=self.tabDataInput)
        self.btnLoadOBD.setObjectName("btnLoadOBD")
        self.btnLoadOBD.setIcon(QtGui.QIcon(":/icons/assets/box.svg"))
        self.horizontalLayoutConn.addWidget(self.btnLoadOBD)
        self.btnLoadOLT = QtWidgets.QPushButton(parent=self.tabDataInput)
        self.btnLoadOLT.setObjectName("btnLoadOLT")
        self.btnLoadOLT.setIcon(QtGui.QIcon(":/icons/assets/olt.svg"))
        self.horizontalLayoutConn.addWidget(self.btnLoadOLT)
        self.horizontalSpacerConn = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutConn.addItem(self.horizontalSpacerConn)
        self.verticalLayoutDataInput.addLayout(self.horizontalLayoutConn)

        self.labelDataSummary = QtWidgets.QLabel(parent=self.tabDataInput)
        self.labelDataSummary.setObjectName("labelDataSummary")
        self.verticalLayoutDataInput.addWidget(self.labelDataSummary)

        self.labelTableTitle = QtWidgets.QLabel(parent=self.tabDataInput)
        self.labelTableTitle.setObjectName("labelTableTitle")
        self.verticalLayoutDataInput.addWidget(self.labelTableTitle)

        self.tableViewData = QtWidgets.QTableView(parent=self.tabDataInput)
        self.tableViewData.setObjectName("tableViewData")
        self.tableViewData.setAlternatingRowColors(True)
        self.tableViewData.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableViewData.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.verticalLayoutDataInput.addWidget(self.tableViewData)

        self.tabWidget.addTab(self.tabDataInput, "")
        self.tabWidget.setTabIcon(
            self.tabWidget.indexOf(self.tabDataInput),
            QtGui.QIcon(":/icons/assets/database.svg")
        )

        # ------------------------------------------------------------------
        # Tab 2 - 数据处理
        # ------------------------------------------------------------------
        self.tabDataProcess = QtWidgets.QWidget()
        self.tabDataProcess.setObjectName("tabDataProcess")
        self.verticalLayoutDataProcess = QtWidgets.QVBoxLayout(self.tabDataProcess)
        self.verticalLayoutDataProcess.setObjectName("verticalLayoutDataProcess")

        self.labelDataProcessTitle = QtWidgets.QLabel(parent=self.tabDataProcess)
        self.labelDataProcessTitle.setObjectName("labelDataProcessTitle")
        self.labelDataProcessTitle.setTextFormat(QtCore.Qt.RichText)
        self.labelDataProcessTitle.setText(
            "<h2>数据处理 - OBD 分类与 PON 口聚合</h2>"
        )
        self.verticalLayoutDataProcess.addWidget(self.labelDataProcessTitle)

        self.horizontalLayoutProcess = QtWidgets.QHBoxLayout()
        self.horizontalLayoutProcess.setObjectName("horizontalLayoutProcess")
        self.btnProcessData = QtWidgets.QPushButton(parent=self.tabDataProcess)
        self.btnProcessData.setObjectName("btnProcessData")
        self.btnProcessData.setIcon(QtGui.QIcon(":/icons/assets/run.svg"))
        self.horizontalLayoutProcess.addWidget(self.btnProcessData)
        self.labelObdSummary = QtWidgets.QLabel(parent=self.tabDataProcess)
        self.labelObdSummary.setObjectName("labelObdSummary")
        self.horizontalLayoutProcess.addWidget(self.labelObdSummary)
        self.horizontalSpacerProcess = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutProcess.addItem(self.horizontalSpacerProcess)
        self.verticalLayoutDataProcess.addLayout(self.horizontalLayoutProcess)

        self.labelPonStatsTitle = QtWidgets.QLabel(parent=self.tabDataProcess)
        self.labelPonStatsTitle.setObjectName("labelPonStatsTitle")
        self.verticalLayoutDataProcess.addWidget(self.labelPonStatsTitle)

        self.tableViewPonStats = QtWidgets.QTableView(parent=self.tabDataProcess)
        self.tableViewPonStats.setObjectName("tableViewPonStats")
        self.tableViewPonStats.setAlternatingRowColors(True)
        self.tableViewPonStats.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableViewPonStats.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.verticalLayoutDataProcess.addWidget(self.tableViewPonStats)

        self.labelChartUtil = QtWidgets.QLabel(parent=self.tabDataProcess)
        self.labelChartUtil.setObjectName("labelChartUtil")
        self.verticalLayoutDataProcess.addWidget(self.labelChartUtil)

        self.widgetChartUtil = QtWidgets.QWidget(parent=self.tabDataProcess)
        self.widgetChartUtil.setObjectName("widgetChartUtil")
        self.verticalLayoutDataProcess.addWidget(self.widgetChartUtil)

        self.tabWidget.addTab(self.tabDataProcess, "")
        self.tabWidget.setTabIcon(
            self.tabWidget.indexOf(self.tabDataProcess),
            QtGui.QIcon(":/icons/assets/fiber.svg")
        )

        # ------------------------------------------------------------------
        # Tab 3 - 模型训练
        # ------------------------------------------------------------------
        self.tabModelTrain = QtWidgets.QWidget()
        self.tabModelTrain.setObjectName("tabModelTrain")
        self.verticalLayoutModelTrain = QtWidgets.QVBoxLayout(self.tabModelTrain)
        self.verticalLayoutModelTrain.setObjectName("verticalLayoutModelTrain")

        self.labelModelTrainTitle = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelModelTrainTitle.setObjectName("labelModelTrainTitle")
        self.labelModelTrainTitle.setTextFormat(QtCore.Qt.RichText)
        self.labelModelTrainTitle.setText(
            "<h2>模型训练 - 随机森林回归</h2>"
        )
        self.verticalLayoutModelTrain.addWidget(self.labelModelTrainTitle)

        self.formLayoutParams = QtWidgets.QFormLayout()
        self.formLayoutParams.setObjectName("formLayoutParams")

        self.labelNEstimators = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelNEstimators.setObjectName("labelNEstimators")
        self.spinNEstimators = QtWidgets.QSpinBox(parent=self.tabModelTrain)
        self.spinNEstimators.setObjectName("spinNEstimators")
        self.spinNEstimators.setMinimum(10)
        self.spinNEstimators.setMaximum(1000)
        self.spinNEstimators.setValue(100)
        self.formLayoutParams.addRow(self.labelNEstimators, self.spinNEstimators)

        self.labelMaxDepth = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelMaxDepth.setObjectName("labelMaxDepth")
        self.spinMaxDepth = QtWidgets.QSpinBox(parent=self.tabModelTrain)
        self.spinMaxDepth.setObjectName("spinMaxDepth")
        self.spinMaxDepth.setMinimum(0)
        self.spinMaxDepth.setMaximum(50)
        self.spinMaxDepth.setValue(0)
        self.spinMaxDepth.setSpecialValueText("不限")
        self.formLayoutParams.addRow(self.labelMaxDepth, self.spinMaxDepth)

        self.labelRandomState = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelRandomState.setObjectName("labelRandomState")
        self.spinRandomState = QtWidgets.QSpinBox(parent=self.tabModelTrain)
        self.spinRandomState.setObjectName("spinRandomState")
        self.spinRandomState.setMinimum(0)
        self.spinRandomState.setMaximum(99999)
        self.spinRandomState.setValue(42)
        self.formLayoutParams.addRow(self.labelRandomState, self.spinRandomState)

        self.verticalLayoutModelTrain.addLayout(self.formLayoutParams)

        self.horizontalLayoutTrain = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTrain.setObjectName("horizontalLayoutTrain")
        self.btnTrainModel = QtWidgets.QPushButton(parent=self.tabModelTrain)
        self.btnTrainModel.setObjectName("btnTrainModel")
        self.btnTrainModel.setIcon(QtGui.QIcon(":/icons/assets/run.svg"))
        self.horizontalLayoutTrain.addWidget(self.btnTrainModel)
        self.progressBarTrain = QtWidgets.QProgressBar(parent=self.tabModelTrain)
        self.progressBarTrain.setObjectName("progressBarTrain")
        self.progressBarTrain.setValue(0)
        self.horizontalLayoutTrain.addWidget(self.progressBarTrain)
        self.horizontalSpacerTrain = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutTrain.addItem(self.horizontalSpacerTrain)
        self.verticalLayoutModelTrain.addLayout(self.horizontalLayoutTrain)

        self.labelMetrics = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelMetrics.setObjectName("labelMetrics")
        self.verticalLayoutModelTrain.addWidget(self.labelMetrics)

        self.labelFeatureImpTitle = QtWidgets.QLabel(parent=self.tabModelTrain)
        self.labelFeatureImpTitle.setObjectName("labelFeatureImpTitle")
        self.verticalLayoutModelTrain.addWidget(self.labelFeatureImpTitle)

        self.widgetChartFeatureImp = QtWidgets.QWidget(parent=self.tabModelTrain)
        self.widgetChartFeatureImp.setObjectName("widgetChartFeatureImp")
        self.verticalLayoutModelTrain.addWidget(self.widgetChartFeatureImp)

        self.tabWidget.addTab(self.tabModelTrain, "")
        self.tabWidget.setTabIcon(
            self.tabWidget.indexOf(self.tabModelTrain),
            QtGui.QIcon(":/icons/assets/computer.svg")
        )

        # ------------------------------------------------------------------
        # Tab 4 - 结果预测
        # ------------------------------------------------------------------
        self.tabResultPredict = QtWidgets.QWidget()
        self.tabResultPredict.setObjectName("tabResultPredict")
        self.verticalLayoutResultPredict = QtWidgets.QVBoxLayout(self.tabResultPredict)
        self.verticalLayoutResultPredict.setObjectName("verticalLayoutResultPredict")

        self.labelResultTitle = QtWidgets.QLabel(parent=self.tabResultPredict)
        self.labelResultTitle.setObjectName("labelResultTitle")
        self.labelResultTitle.setTextFormat(QtCore.Qt.RichText)
        self.labelResultTitle.setText(
            "<h2>结果预测 - OLT 站点 PON 口扩容建议</h2>"
        )
        self.verticalLayoutResultPredict.addWidget(self.labelResultTitle)

        self.horizontalLayoutPredict = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPredict.setObjectName("horizontalLayoutPredict")
        self.btnPredict = QtWidgets.QPushButton(parent=self.tabResultPredict)
        self.btnPredict.setObjectName("btnPredict")
        self.btnPredict.setIcon(QtGui.QIcon(":/icons/assets/checkmark.svg"))
        self.horizontalLayoutPredict.addWidget(self.btnPredict)
        self.btnExportCSV = QtWidgets.QPushButton(parent=self.tabResultPredict)
        self.btnExportCSV.setObjectName("btnExportCSV")
        self.btnExportCSV.setIcon(QtGui.QIcon(":/icons/assets/file.svg"))
        self.horizontalLayoutPredict.addWidget(self.btnExportCSV)
        self.horizontalSpacerPredict = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutPredict.addItem(self.horizontalSpacerPredict)
        self.verticalLayoutResultPredict.addLayout(self.horizontalLayoutPredict)

        self.labelResultTableTitle = QtWidgets.QLabel(parent=self.tabResultPredict)
        self.labelResultTableTitle.setObjectName("labelResultTableTitle")
        self.verticalLayoutResultPredict.addWidget(self.labelResultTableTitle)

        self.tableViewResult = QtWidgets.QTableView(parent=self.tabResultPredict)
        self.tableViewResult.setObjectName("tableViewResult")
        self.tableViewResult.setAlternatingRowColors(True)
        self.tableViewResult.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableViewResult.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.verticalLayoutResultPredict.addWidget(self.tableViewResult)

        self.labelAdviceTitle = QtWidgets.QLabel(parent=self.tabResultPredict)
        self.labelAdviceTitle.setObjectName("labelAdviceTitle")
        self.verticalLayoutResultPredict.addWidget(self.labelAdviceTitle)

        self.textEditAdvice = QtWidgets.QTextEdit(parent=self.tabResultPredict)
        self.textEditAdvice.setObjectName("textEditAdvice")
        self.textEditAdvice.setReadOnly(True)
        self.textEditAdvice.setHtml(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
            "\"http://www.w3.org/TR/REC-html40/strict.dtd\">"
            "<html><head/><body><p>尚未执行预测。</p></body></html>"
        )
        self.verticalLayoutResultPredict.addWidget(self.textEditAdvice)

        self.tabWidget.addTab(self.tabResultPredict, "")
        self.tabWidget.setTabIcon(
            self.tabWidget.indexOf(self.tabResultPredict),
            QtGui.QIcon(":/icons/assets/graph.svg")
        )

        self.verticalLayoutMain.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _t = QtCore.QCoreApplication.translate
        # 数据输入 Tab
        self.labelConnStatus.setText(_t("TransportPredict", "数据库连接状态：未连接"))
        self.btnTestConn.setText(_t("TransportPredict", "测试连接"))
        self.btnLoadOBD.setText(_t("TransportPredict", "加载 OBD 数据"))
        self.btnLoadOLT.setText(_t("TransportPredict", "加载 OLT 数据"))
        self.labelDataSummary.setText(_t("TransportPredict", "数据摘要：未加载"))
        self.labelTableTitle.setText(_t("TransportPredict", "数据预览："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDataInput),
                                  _t("TransportPredict", "数据输入"))
        # 数据处理 Tab
        self.btnProcessData.setText(_t("TransportPredict", "执行数据处理"))
        self.labelObdSummary.setText(_t("TransportPredict", "OBD 摘要：未处理"))
        self.labelPonStatsTitle.setText(_t("TransportPredict", "PON 口利用率统计："))
        self.labelChartUtil.setText(_t("TransportPredict", "端子利用率分布图："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDataProcess),
                                  _t("TransportPredict", "数据处理"))
        # 模型训练 Tab
        self.labelNEstimators.setText(_t("TransportPredict", "n_estimators (树数量)："))
        self.labelMaxDepth.setText(_t("TransportPredict", "max_depth (最大深度, 0=不限)："))
        self.labelRandomState.setText(_t("TransportPredict", "random_state (随机种子)："))
        self.btnTrainModel.setText(_t("TransportPredict", "开始训练"))
        self.labelMetrics.setText(_t("TransportPredict", "评估指标：未训练"))
        self.labelFeatureImpTitle.setText(_t("TransportPredict", "特征重要性："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabModelTrain),
                                  _t("TransportPredict", "模型训练"))
        # 结果预测 Tab
        self.btnPredict.setText(_t("TransportPredict", "执行预测"))
        self.btnExportCSV.setText(_t("TransportPredict", "导出 CSV"))
        self.labelResultTableTitle.setText(_t("TransportPredict", "OLT 站点扩容建议汇总："))
        self.labelAdviceTitle.setText(_t("TransportPredict", "详细建议："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultPredict),
                                  _t("TransportPredict", "结果预测"))
        # 状态栏默认文本
        self.statusbar.showMessage(_t("TransportPredict", "就绪"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # 注册资源
    try:
        import resources_rc  # noqa: F401
    except Exception:
        pass
    window = QtWidgets.QMainWindow()
    ui = Ui_TransportPredict()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
