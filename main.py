# pyside6-rcc resources.qrc -o resources_rc.py
import sys
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import (QMainWindow, QApplication, QGraphicsDropShadowEffect, QWidget, QFileDialog, QMessageBox,
                               QTableWidgetItem,QHBoxLayout,QPushButton,QHeaderView)
from PySide6.QtUiTools import loadUiType
from main_ui import Ui_MainWindow
from publicFunc import *
from publicThread import *
from datetime import datetime
from customnWidget import *

class TNAIWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(TNAIWindow, self).__init__()
        # Remove default title bar
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))
        self.setupUi(self)
        self.closeBtn.clicked.connect(self.closeWindow)
        self.miniBtn.clicked.connect(self.minimizeWindow)
        self.sideClose.clicked.connect(self.toggleSideBar)
        self.menuBtn.clicked.connect(self.toggleSideBar)
        self.homeBtn.clicked.connect(self.selectPage)
        self.updateBtn.clicked.connect(self.selectPage)
        self.cardShadow(self.card1)
        self.cardShadow(self.card2)
        self.cardShadow(self.card3)
        self.cardShadow(self.card4)
        self.cardShadow(self.card5)

        # 数据库更新页面
        self.file_type_cols = [
            'OLT网元', '主光路', 'PON端口', '中继段', '光缆段', '站点', '机房', '光交箱', '分纤箱', 'ODF', '华为PON单板','中兴PON单板'
        ]
        # 数据库更新页面 列名
        self.file_cols = [
            (['网元名称', '所属机房', '设备型号', '设备IP','生命周期状态'],['str','str','str','str','str']),
            (['OLT名称', 'PON口', 'PON下挂ONU数量', 'OBD所属对象', '光路名称', '光路长度','光路文本路由'],['str','str','int','str','str','float','str']),
            (['所属传输网元', '端口名称', 'PONID', '端口状态', 'PON口下挂用户数', '端口子类型'],['str','str','str','str','int','str']),
            (['名称', '长度', '空闲数量', '占用数量', '中继纤芯数量', '始端站点', '终端站点', '始端机房','终端机房', '始端设施', '终端设施'],['str','float','int','int','int','str','str','str','str','str','str']),
            (['名称','所属光缆','实际长度','纤芯占用率','光纤数目','业务级别','敷设方式'],['str','str','float','float','int','str','str']),
            (['站点名称', '所属区县', '乡镇街道'],['str','str','str']),
            (['所属站点', '机房类型', '机房名称', '业务级别', '生命周期状态'],['str','str','str','str','str']),
            (['设施名称', '机房名称', '所属综合业务区', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','int','float','float']),
            (['所属网元','槽位号','单板类型','单板状态'],['str','str','str','str']),
            (['网元名称','板卡槽位','板卡类型','板卡状态'],['str','str','str','str'])
        ]

        self.fileTypeCB.currentIndexChanged.connect(self.updateFileCols)
        self.fileTypeCB.addItems(self.file_type_cols)
        self.current_cols = []
        self.importFileDf = pd.DataFrame()
        self.choseFileBtn.clicked.connect(self.choseFile)
        
        self.settingBtn.clicked.connect(self.initDataBase)
        self.analysis_types = ['光设施', 'OLT端口', '主光路']
        self.current_analysis_type = 0
        self.odevBtn.clicked.connect(self.selectAnalysisType)
        self.oltBtn.clicked.connect(self.selectAnalysisType)
        self.linkBtn.clicked.connect(self.selectAnalysisType)
        self.runAnalysisBtn.clicked.connect(self.runAnalysis)
        self.checkTableBtn.clicked.connect(self.checkTable)
        self.updateDataBaseBtn.clicked.connect(self.updateDataBase)
        self.dbmsBtn.clicked.connect(self.selectPage)
        self.dbTableBtn.clicked.connect(self.searchDBTableInfo)
        self.kpiBtn.clicked.connect(self.selectPage)
        self.outsideBtn.clicked.connect(self.selectPage)
        self.insideBtn.clicked.connect(self.selectPage)
        self.oltKeywordLE.returnPressed.connect(self.searchOltSite)
        self.searchOltBtn.clicked.connect(self.searchOltNe)
        self.oltNeTw.cellClicked.connect(self.onOltNeTwCellClicked)
        self.writeAggrHouseBtn.clicked.connect(self.writeAggrHouseKml)
        self.odevNameKeysLe.returnPressed.connect(self.searchoDevs)
        self.searchDevUplinkBtn.clicked.connect(self.searchDevUplink)
        self.upLinkTW.cellClicked.connect(self.onUpLinkTwCellClicked)
        self.highScoreBtn.clicked.connect(self.selectupLink)
        self.dbmMinBtn.clicked.connect(self.selectupLink)
        self.numMaxBtn.clicked.connect(self.selectupLink)
        # 查找中继段资源
        self.searchLineBtn.clicked.connect(self.findRelayLine)
        self.lineKeysLE.returnPressed.connect(self.findRelayLine)
        self.relay_line_result_dialogs = []
        # 设置首页
        page_widget = self.container.findChild(QWidget, "homePage")
        self.container.setCurrentWidget(page_widget)

        # kpi页面的按钮
        self.redOltPortSiteBtn.clicked.connect(self.searchRedOltPortSite)
        self.notOltAggrSiteBtn.clicked.connect(self.findNoOltSite)
        self.boxUplinkBusyBtn.clicked.connect(self.busyBoxUplink)
        self.notXgOltBtn.clicked.connect(self.findNoXgOltSite)
        self.onuBtn.clicked.connect(self.findWeekOnu)


        self.log_str = ''
        # 提速 中继段查找效能
        self.all_line_df = pd.DataFrame()
        self.load_relay_line_thread = LoadRelayLineThread()
        self.load_relay_line_thread.state_signal.connect(self.showStatus)
        self.load_relay_line_thread.result_signal.connect(self.loadRelayLineResult)
        self.load_relay_line_thread.start()

    def loadRelayLineResult(self,df):
        self.all_line_df = df
        self.showStatus('中继段加载完成')
    
    def findWeekOnu(self):
        # 选择PON口光功率数据文件夹
        folder_path = QFileDialog.getExistingDirectory(self, "选择PON口光功率数据文件夹")
        if not folder_path:
            return
        self.find_weak_onu_thread = FindWeakONUThread(folder_path=folder_path)
        self.find_weak_onu_thread.state_signal.connect(self.showStatus)
        self.find_weak_onu_thread.start()
        

    # 分析未部署千兆OLT的超1000户站点
    def findNoXgOltSite(self):
        # 选择保存文件路径
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "未部署千兆OLT的超1000户站点.xlsx", "Excel 文件 (*.xlsx)")
        if not file_path:
            return
        self.find_no_xg_olt_site_thread = FindNoXgOltSiteThread(file_path=file_path)
        self.find_no_xg_olt_site_thread.state_signal.connect(self.showStatus)
        self.find_no_xg_olt_site_thread.start()

    # 分析未部署OLT的汇聚站点          
    def findNoOltSite(self):
        # 选择保存文件路径
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "未部署OLT的汇聚站点.xlsx", "Excel 文件 (*.xlsx)")
        if not file_path:
            return
        self.find_no_olt_site_thread = FindNoOltSiteThread(file_path=file_path)
        self.find_no_olt_site_thread.state_signal.connect(self.showStatus)
        self.find_no_olt_site_thread.start()
    
    def searchRedOltPortSite(self):
        # 选择保存文件路径
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "端口预警OLT站点.xlsx", "Excel 文件 (*.xlsx)")
        if not file_path:
            return
        self.find_red_olt_port_site_thread = FindRedOltPortSiteThread(file_path=file_path)
        self.find_red_olt_port_site_thread.state_signal.connect(self.showStatus)
        self.find_red_olt_port_site_thread.start()

    # 中继段查找
    def search(self,text,keywords=[]):
        for keyword in keywords:
            if keyword not in text:
                return False
        return True

    def findRelayLine(self):
        keyword_text = self.lineKeysLE.text().strip()
        if not keyword_text:
            QMessageBox.warning(self, '警告', '请输入查找关键词')
            return;
        if self.all_line_df.empty:
            QMessageBox.warning(self, '警告', '请先加载中继段资源')
            return;
        keywords = keyword_text.split(' ')
        temp_df = self.all_line_df[self.all_line_df['查找项'].apply(lambda x: self.search(x,keywords))].copy()
        temp_df = temp_df.drop(['查找项'],axis=1)
        temp_df = temp_df.reset_index(drop=True)
        self.showRelayLineResult(temp_df,keyword_text)

    def showRelayLineResult(self,df,keyword_text):
        if df.empty:
            QMessageBox.warning(self, '警告', '未查询到结果')
            return;
        # 创建新的结果窗口
        dialog = RelayLineResultDialog(df)
        # 设置窗口标题包含序号，便于区分
        dialog.setWindowTitle(f"中继段资源查询结果：({keyword_text})")
        # 添加到窗口列表
        self.relay_line_result_dialogs.append(dialog)
        # 使用closeEvent回调替代destroyed信号
        dialog.setCloseCallback(self.removeClosedDialog)
        # 显示窗口
        dialog.show()


    def removeClosedDialog(self, dialog):
        """从列表中移除已关闭的窗口，释放内存"""
        if dialog in self.relay_line_result_dialogs:
            self.relay_line_result_dialogs.remove(dialog)
        
    def busyBoxUplink(self):
        # 选择输出文件目录
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出文件目录")
        if not dir_path:
            return
        self.busy_box_thread = BusyBoxUplinkThread(dir_path)
        self.busy_box_thread.state_signal.connect(self.showStatus)
        self.busy_box_thread.start()

    def selectupLink(self):
        if self.sender() == self.highScoreBtn:
            # 查找upLinkTW中第8列中值最大的行
            max_value = float('-inf')
            max_row_index = -1
            for row in range(self.upLinkTW.rowCount()):
                value = float(self.upLinkTW.item(row, 7).text())
                if value > max_value:
                    max_value = value
                    max_row_index = row
            if max_row_index != -1:
                self.upLinkTW.selectRow(max_row_index)
            up_link_text = self.upLinkTW.item(max_row_index,6).text()
        elif self.sender() == self.dbmMinBtn:
            # 查找upLinkTW中第6列中值最小的行
            min_value = float('100000')
            min_row_index = -1
            for row in range(self.upLinkTW.rowCount()):
                value = float(self.upLinkTW.item(row, 5).text())
                if value < min_value:
                    min_value = value
                    min_row_index = row
            if min_row_index != -1:
                self.upLinkTW.selectRow(min_row_index)
            up_link_text = self.upLinkTW.item(min_row_index,6).text()
        elif self.sender() == self.numMaxBtn:
            # 查找upLinkTW中第3列中值最大的行
            max_value = float('-inf')
            max_row_index = -1
            for row in range(self.upLinkTW.rowCount()):
                value = float(self.upLinkTW.item(row, 2).text())
                if value > max_value:
                    max_value = value
                    max_row_index = row
            if max_row_index != -1:
                self.upLinkTW.selectRow(max_row_index)
            up_link_text = self.upLinkTW.item(max_row_index,6).text()
        self.uplink_text.setText(up_link_text)
        self.uplink_topo.setData(up_link_text)

    def onUpLinkTwCellClicked(self,row,column):
        # 行号从0开始（第一行为0），可根据需要加1转为自然行号
        clicked_row = row
        up_link_text = self.upLinkTW.item(clicked_row,6).text()
        self.uplink_text.setText(up_link_text)
        self.uplink_topo.setData(up_link_text)

    # 查找光交设施上联路径
    def searchDevUplink(self):
        dev_name = self.odevNamesCB.currentText()
        if dev_name == '':
            QMessageBox.warning(self, '警告', '请选择光交设施')
            return;
        uplink_path_df = searchOdevUplinkFunc(dev_name)
        if len(uplink_path_df) == 0:
            QMessageBox.warning(self, '警告', '未查询到光交设施上联路径')
            return;
        self.upLinkTW.setRowCount(len(uplink_path_df))
        self.upLinkTW.setColumnCount(len(uplink_path_df.columns))
        self.upLinkTW.setHorizontalHeaderLabels(uplink_path_df.columns)
        # 设置第1,7列隐藏
        self.upLinkTW.setColumnHidden(0, True)
        self.upLinkTW.setColumnHidden(6, True)
        # 设置第二列自动扩展
        self.upLinkTW.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i in range(uplink_path_df.shape[0]):
            for j in range(uplink_path_df.shape[1]):
                self.upLinkTW.setItem(i, j, QTableWidgetItem(str(uplink_path_df.iloc[i, j])))
        

    # 查找光交设施名称
    def searchoDevs(self):
        dev_name_keyword = self.odevNameKeysLe.text().strip()
        if dev_name_keyword == '':
            QMessageBox.warning(self, '警告', '请输入光交设施名称')
            return;
        odev_names = searchOdevNameFunc(dev_name_keyword)
        if len(odev_names) == 0:
            QMessageBox.warning(self, '警告', '未查询到光交设施')
            return;
        self.odevNamesCB.clear()
        self.odevNamesCB.addItems(odev_names)



    # 写入汇聚机房覆盖情况kml文件
    def writeAggrHouseKml(self):
        file_path = QFileDialog.getSaveFileName(self, '保存文件', '汇聚机房覆盖情况.kml', 'KML Files (*.kml)')
        if file_path[0] == '':
            return;
        self.statusLabel.setText('正在生成机房覆盖图层...')
        writeAggrHouseKml(file_path[0])
        self.statusLabel.setText('已生成机房覆盖图层！')
    
    def onOltNeTwCellClicked(self,row,column):
        # 行号从0开始（第一行为0），可根据需要加1转为自然行号
        clicked_row = row
        olt_name = self.oltNeTw.item(clicked_row,0).text()
        pon_dict = {'使用数':int(self.oltNeTw.item(clicked_row,2).text()),'空闲数':int(self.oltNeTw.item(clicked_row,3).text())}
        xgpon_dict = {'使用数':int(self.oltNeTw.item(clicked_row,4).text()),'空闲数':int(self.oltNeTw.item(clicked_row,5).text())}
        self.portUsePie.setData(pon_dict,'普通PON口占用情况')
        self.xgPortUsePie.setData(xgpon_dict,'千兆PON口占用情况')
        dict = drawOltBoard(olt_name)
        self.oltBoardView.drawBoard(dict)
               
    
    def selectOltNe(self):
        # 选中OLT网元
        selected_rows = self.oltNeTw.selectedRows()
        if len(selected_rows) == 0:
            QMessageBox.warning(self, '警告', '请选择OLT网元')
            return;
        olt_name = self.oltNeTw.item(selected_rows[0],0).text()
        self.oltSiteNamesCB.setCurrentText(olt_name)
    
    def searchOltNe(self):
        olt_name = self.oltSiteNamesCB.currentText()
        if olt_name == '':
            QMessageBox.warning(self, '警告', '请选择OLT站点')
            return;
        df,pon_dict,xgpon_dict = searchOltNeFunc(olt_name)
        self.portUsePie.setData(pon_dict,'普通PON口占用情况')
        self.xgPortUsePie.setData(xgpon_dict,'千兆PON口占用情况')
        self.oltNeTw.setRowCount(df.shape[0])
        self.oltNeTw.setColumnCount(df.shape[1])
        self.oltNeTw.setHorizontalHeaderLabels(df.columns)
        # 第一行自动扩展
        self.oltNeTw.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.oltNeTw.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def searchOltSite(self):
        # 搜索OLT站点
        keyword = self.oltKeywordLE.text().strip()
        if keyword == '':
            QMessageBox.warning(self, '警告', '请输入搜索关键词')
            self.oltSiteNamesCB.clear()
            return;
        sites,msg = searchOltSiteFunc(keyword)
        if msg != '搜索成功':
            QMessageBox.warning(self, '警告', msg)
            return;
        self.oltSiteNamesCB.clear()
        self.oltSiteNamesCB.addItems(sites)
        self.oltSiteNamesCB.setCurrentIndex(0)
        
            
    
    def searchDBTableInfo(self):
        # 查询数据库的表信息，返回dataframe ,显示在dbTableTw，最后一列加上 操作 列
        self.db_info_thread = DatabaseInfoThread()
        self.db_info_thread.resultReady.connect(self.showDBTableInfo)
        self.db_info_thread.state_signal.connect(self.showStatus)
        self.db_info_thread.start()


    def showDBTableInfo(self,df):
        self.dbTableTw.setRowCount(len(df))
        self.dbTableTw.setColumnCount(5)  # 表名 + 操作列
        self.dbTableTw.setHorizontalHeaderLabels(['表名', '列名及类型', '行数', '最后更新时间', '操作'])
        # 列名及类型 列自动扩展
        self.dbTableTw.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i, row in df.iterrows():
            # 添加表名
            self.dbTableTw.setItem(i, 0, QTableWidgetItem(row['表名']))
            self.dbTableTw.setItem(i, 1, QTableWidgetItem(row['列名及类型']))
            self.dbTableTw.setItem(i, 2, QTableWidgetItem(str(row['行数'])))
            self.dbTableTw.setItem(i, 3, QTableWidgetItem(row['最后更新时间']))
            # 添加操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            download_btn = QPushButton('下载')
            download_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 33, 44, 255);
                    color: #44cc88;
                    border: 1px solid #44cc88;
                }
                QPushButton:hover {
                    background-color: rgba(40, 45, 56, 255);
                }
                QPushButton:pressed {
                    background-color: rgba(20, 25, 36, 255);
                }
            """)
            download_btn.clicked.connect((lambda checked=None, r=i: self.download_table(df.iloc[r, 0])))
            clear_btn = QPushButton('清空')
            clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 33, 44, 255);
                    color: #ff9999;
                    border: 1px solid #ff9999;
                }
                QPushButton:hover {
                    background-color: rgba(40, 45, 56, 255);
                }
                QPushButton:pressed {
                    background-color: rgba(20, 25, 36, 255);
                }""")
            clear_btn.clicked.connect((lambda checked=None, r=i: self.clear_table(df.iloc[r, 0])))
            btn_layout.addWidget(download_btn)
            btn_layout.addWidget(clear_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_widget.setLayout(btn_layout)
            self.dbTableTw.setCellWidget(i, 4, btn_widget)

    def download_table(self, table_name):
        # 下载表格数据实现
        data_df = readDataBase(table_name)
        file_path = QFileDialog.getSaveFileName(self, "保存文件", f"{table_name}.xlsx", "Excel 文件 (*.xlsx)")[0]
        self.download_file_thread = downloadThread([table_name], [data_df],file_path)
        self.download_file_thread.state_signal.connect(self.showStatus)
        self.download_file_thread.start()

    def clear_table(self, table_name):
        # 弹窗确认是否清空
        reply = QMessageBox.question(self, '确认清空', f'确认清空 {table_name} 表吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return;
        # 清空表格实现
        self.showStatus(clearDataBase(table_name))

    # 运行分析
    def runAnalysis(self):
        self.runProgressBar.show()
        self.needTime.show()
        if self.current_analysis_type == 0:
            self.analysis_thread = BoxUpLineThread()
        elif self.current_analysis_type == 1:
            self.analysis_thread = AnalysisOltPortThread()
        elif self.current_analysis_type == 2:
            self.analysis_thread = FindLongPonLineThread()
        self.analysis_thread.state_signal.connect(self.showAnalysisStatus)
        self.analysis_thread.start()

    def showAnalysisStatus(self,msg,percent,time):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.needTalbeTE.append(f"{current_time} 当前进度：{msg}")
        self.runProgressBar.setValue(percent)
        if percent == 100:
            self.runProgressBar.hide()
            self.needTime.hide()
        else:
            self.needTime.setText(time)

    # 检查分析需求表格是否存在
    def checkTable(self):
        self.needTalbeTE.clear()
        self.check_table_thread = CheckTableThread(self.analysis_types[self.current_analysis_type])
        self.check_table_thread.tableReady.connect(self.showCheckResult)
        self.check_table_thread.resultReady.connect(self.enableCheck)
        self.check_table_thread.start()

    def showCheckResult(self, result):
        # 将result结果加入到 needTalbeTE
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.needTalbeTE.append(f"{current_time} {result}")
    
    def enableCheck(self, result):
        if result:
            self.runAnalysisBtn.setEnabled(True)
        else:
            self.runAnalysisBtn.setEnabled(False)

    # 选择分析类型
    def selectAnalysisType(self):
        if self.sender() == self.odevBtn:
            self.current_analysis_type = 0
            self.analysisLabel.setText('【光交设施上联OLT机房分析】')
        elif self.sender() == self.oltBtn:
            self.current_analysis_type = 1
            self.analysisLabel.setText('【OLT设备端口分析】')
        elif self.sender() == self.linkBtn:
            self.current_analysis_type = 2
            self.analysisLabel.setText('【超长PON主光路分析】')
        page_widget = self.container.findChild(QWidget, "analysisPage")
        self.container.setCurrentWidget(page_widget)
        # 设置 runProgressBar、needTime隐藏
        self.runAnalysisBtn.setEnabled(False)
        self.runProgressBar.hide()
        self.needTime.hide()

    def initDataBase(self):
        initDB()
        # 弹窗显示已完成
        QMessageBox.information(self, "提示", "数据库初始化完成")

    # 更新数据库
    def updateDataBase(self):
        if len(self.current_cols) == 0:
            QMessageBox.information(self, "提示", "未选择导入文件！", QMessageBox.Yes)
            return
        tempDf = self.importFileDf.copy()
        cols = self.file_cols[self.fileTypeCB.currentIndex()][0]
        col_types = self.file_cols[self.fileTypeCB.currentIndex()][1]
        for i in range(len(cols)):
            row = 2 * int(i / 5) + 1
            col = i % 5
            oldCol = self.colsGridLayout.itemAtPosition(row, col).widget().currentText()
            if oldCol != cols[i]:
                tempDf.rename(columns={oldCol: cols[i]}, inplace=True)
            if col_types[i] == 'int':
                tempDf[cols[i]] = pd.to_numeric(tempDf[cols[i]], errors='coerce').fillna(0).astype(int)
            elif col_types[i] == 'float':
                tempDf[cols[i]] = pd.to_numeric(tempDf[cols[i]], errors='coerce')
        tempDf = tempDf[cols]
        tempFileType = self.fileTypeCB.currentText()
        tempDf = tempDf.drop_duplicates()
        self.update_db_thread = UpdateDBThread(tempFileType, tempDf)
        self.update_db_thread.state_signal.connect(self.showStatus)
        self.update_db_thread.start()

    def choseFile(self):
        if self.muti_file_cb.isChecked():
            file_paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "Excel 文件 (*.xlsx);;CSV 文件 (*.csv)")
            if len(file_paths) == 0:
                return
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel 文件 (*.xlsx);;CSV 文件 (*.csv)")
            if len(file_path) == 0:
                return
            file_paths = [file_path]
        self.filePathLE.setText(', '.join(file_paths))
        header_line = self.header_sb.value()
        table_name = self.fileTypeCB.currentText()
        self.import_file_thread = ImportFileThread(file_paths, table_name, header_line)
        self.import_file_thread.state_signal.connect(self.showStatus)
        self.import_file_thread.result_signal.connect(self.showResult)
        self.import_file_thread.start()

    def showResult(self, df):
        self.importFileDf = df
        self.current_cols = df.columns.tolist()
        cols = self.file_cols[self.fileTypeCB.currentIndex()][0]
        for i in range(len(cols)):
            row = 2 * int(i / 5) + 1
            col = i % 5
            self.colsGridLayout.itemAtPosition(row, col).widget().clear()
            self.colsGridLayout.itemAtPosition(row, col).widget().addItems(self.current_cols)
            tempCol = self.colsGridLayout.itemAtPosition(row - 1,col).widget().text()
            if tempCol in self.current_cols:
                self.colsGridLayout.itemAtPosition(row, col).widget().setCurrentIndex(self.current_cols.index(tempCol))
            else:
                tempMark = mostLike(tempCol, self.current_cols)
                self.colsGridLayout.itemAtPosition(row, col).widget().setCurrentIndex(self.current_cols.index(tempMark))
        self.statusLabel.setText('自动匹配对应列如上，请核对，确认无问题后更新缓存按钮！')


    def showStatus(self, state):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.statusLabel.setText(f"{current_time} {state}")
        self.log_str += f"{current_time} {state}\n"


    def updateFileCols(self):
        # 初始化：
        self.current_cols = []
        for row in range(0, 6, 2):
            for col in range(5):
                self.colsGridLayout.itemAtPosition(row,col).widget().setText("- - - -")
                self.colsGridLayout.itemAtPosition(row + 1, col).widget().clear()
        cols = self.file_cols[self.fileTypeCB.currentIndex()][0]
        for i in range(len(cols)):
            row = 2 * int(i / 5)
            col = i % 5
            self.colsGridLayout.itemAtPosition(row, col).widget().setText(cols[i])

    def selectPage(self):
        if self.sender() == self.updateBtn:
            page_widget = self.container.findChild(QWidget, "updatePage")
            self.container.setCurrentWidget(page_widget)
            self.toggleSideBar()
        elif self.sender() == self.homeBtn:
            page_widget = self.container.findChild(QWidget, "homePage")
            self.container.setCurrentWidget(page_widget)
        elif self.sender() == self.dbmsBtn:
            page_widget = self.container.findChild(QWidget, "dbTablePage")
            self.container.setCurrentWidget(page_widget)
        elif self.sender() == self.kpiBtn:
            page_widget = self.container.findChild(QWidget, "kpiPage")
            self.container.setCurrentWidget(page_widget)
            self.toggleSideBar()
        elif self.sender() == self.outsideBtn:
            page_widget = self.container.findChild(QWidget, "outsidePage")
            self.container.setCurrentWidget(page_widget)
        elif self.sender() == self.insideBtn:
            page_widget = self.container.findChild(QWidget, "insidePage")
            self.container.setCurrentWidget(page_widget)

    def closeWindow(self):
        self.close()

    def minimizeWindow(self):
        self.showMinimized()

    def toggleSideBar(self):
        if self.sideBar.maximumWidth() == 0:
            self.sideBar.setMaximumWidth(400)
        else:
            self.sideBar.setMaximumWidth(0)
        
    # def cardShadow(self, widget):
    #     shadow = QGraphicsDropShadowEffect(self)
    #     shadow.setBlurRadius(20)
    #     shadow.setXOffset(0)
    #     shadow.setYOffset(0)
    #     shadow.setColor(QColor(0, 0, 0, 200))
    #     widget.setGraphicsEffect(shadow)
    def cardShadow(self, widget):
        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        
        # 设置悬停事件
        widget.setGraphicsEffect(shadow)
        widget.setAttribute(Qt.WA_Hover)
        widget.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            shadow = QGraphicsDropShadowEffect(obj)
            shadow.setBlurRadius(20)
            shadow.setXOffset(5)
            shadow.setYOffset(5)
            shadow.setColor(QColor(0, 0, 0, 120))
            obj.setGraphicsEffect(shadow)
        elif event.type() == QEvent.HoverLeave:
            shadow = QGraphicsDropShadowEffect(obj)
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(0, 0, 0, 80))
            obj.setGraphicsEffect(shadow)
        return super().eventFilter(obj, event)
    # Move Window with mouse
    def mousePressEvent(self, event):
        self.dragPos = self.pos()
        self.mouse_original_pos = self.mapToGlobal(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            if event.buttons() == Qt.LeftButton:
                last_pos = self.dragPos + self.mapToGlobal(event.position().toPoint()) - self.mouse_original_pos
                self.move(last_pos)
                event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置图标
    app.setWindowIcon(QIcon('assets/main.png'))
    win = TNAIWindow()
    win.show()
    sys.exit(app.exec())

