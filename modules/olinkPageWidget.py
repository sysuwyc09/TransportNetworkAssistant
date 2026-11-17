# -*- coding: utf-8 -*-
"""
光路查询页面（独立 QWidget 封装）

将 main.ui 中 stackedWidget 的 olink_page 页,以及 main.py 中该页所调用的
函数与查询线程,封装为一个可独立复用的 QWidget。

页面功能:
  1. 已关联拓扑连接光路查询:  A端关键字 -> A端网元 -> Z端网元 -> 查询链路
  2. 资源模糊搜索: 光纤光路 / 传输电路 的 模糊查询、精准查询

查询动作均放入 QThread 工作线程中执行,避免阻塞界面。
"""

import re
import sqlite3
from functools import partial
from pathlib import Path

import pandas as pd

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

from modules.olinkPageWidget_ui import Ui_OlinkPageWidget

# 资源数据库路径（相对项目根目录 data/transportNetwork.db）
DB_PATH = str(Path(__file__).resolve().parent.parent / "data" / "transportNetwork.db")


# ---------------------------------------------------------------------------
# 数据库工具函数
# ---------------------------------------------------------------------------
def readDataBase(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"select * from {table_name}", con=conn)
    conn.close()
    return df


def writeDataBase(df, table_name):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)
    conn.close()


def queryDataBase(sql):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(sql, con=conn)
    conn.close()
    return df


# ---------------------------------------------------------------------------
# 纯查询函数（供工作线程调用，不涉及任何 UI 弹窗）
# ---------------------------------------------------------------------------
def search(name, keys):
    """关键字匹配：name 中包含 keys 中的每一个关键字则返回 '是'，否则 '否'。"""
    for key in keys:
        if key not in name:
            return "否"
    return "是"


def searchAne(keys):
    """根据 A 端关键字查找网元名称，同时把 AZ 端映射写入 aneToZne 表。"""
    link_df = readDataBase("拓扑连接关联")
    link_df = link_df[["A端设备", "Z端设备"]].rename(columns={"A端设备":"源网元","Z端设备":"宿网元"})
    link2_df = link_df.copy()
    link2_df.rename(columns={"源网元": "宿网元", "宿网元": "源网元"}, inplace=True)
    link_df = pd.concat([link_df, link2_df])
    link_df = link_df.drop_duplicates()
    link_df["查找"] = link_df["源网元"].apply(search, args=(keys,))
    ane_zne_df = link_df[link_df["查找"] == "是"].copy()
    if ane_zne_df.shape[0] > 0:
        ane_names = list(dict.fromkeys(list(ane_zne_df["源网元"])))
        writeDataBase(ane_zne_df, "aneToZne")
        return ane_names
    return []


def searchZne(ane_name):
    """根据 A 端网元返回可选的 Z 端网元列表。"""
    ane_zne_df = readDataBase("aneToZne")
    temp_df = ane_zne_df[ane_zne_df["源网元"] == ane_name]
    return list(temp_df["宿网元"])


def searchOlink(ane_name, zne_name):
    """根据 AZ 端网元查询关联光路文本路由。"""
    keys = [ane_name, zne_name]
    olink_text_df = readDataBase("拓扑连接关联")
    olink_text_df = olink_text_df[["光电路名称", "拓扑连接名称", "文本路由"]].drop_duplicates()
    olink_text_df["筛选"] = olink_text_df["拓扑连接名称"].apply(search, args=(keys,))
    link_text_df = olink_text_df[olink_text_df["筛选"] == "是"].copy().reset_index()
    link_text_df = link_text_df.astype(str)
    link_text_df = link_text_df[(link_text_df["光电路名称"] != "nan")&(link_text_df["光电路名称"] != "")]
    link_text_df = link_text_df.drop_duplicates(subset=["光电路名称"], keep="first")
    if link_text_df.shape[0] > 0:
        olink_name = "、".join(list(link_text_df["光电路名称"]))
        olink_text = "\n***********************\n".join(list(link_text_df["文本路由"]))
        return olink_name, olink_text
    return "", ""


def searchAllOlink(keys):
    """光纤光路模糊查询。"""
    all_olink_df = readDataBase("全量光路")
    all_olink_df["筛选"] = all_olink_df["匹配项"].apply(search, args=(keys,))
    result_df = all_olink_df[all_olink_df["筛选"] == "是"].copy().reset_index()
    result_df = result_df[
        ["光路名称", "光路方案名称", "承载的业务", "传输系统",
         "A端站点", "Z端站点", "A端机房", "Z端机房", "光路文本路由"]
    ]
    return result_df


def searchAllCircuit(keys):
    """传输电路模糊查询。"""
    circuit_df = readDataBase("全量电路")
    circuit_df["筛选"] = circuit_df["匹配项"].apply(search, args=(keys,))
    result_df = circuit_df[circuit_df["筛选"] == "是"].copy().reset_index()
    result_df = result_df[["电路名称", "A端业务", "Z端业务", "备注", "电路路由"]]
    return result_df


def queryOneOlink(name):
    """光纤光路精准查询。"""
    sql = f"SELECT * FROM 全量光路 WHERE 光路名称 = '{name}'"
    df = queryDataBase(sql)
    return df[
        ["光路名称", "光路方案名称", "承载的业务", "传输系统",
         "A端站点", "Z端站点", "A端机房", "Z端机房", "光路文本路由"]
    ]


def queryOneCircuit(name):
    """传输电路精准查询。"""
    sql = f"SELECT * FROM 全量电路 WHERE 电路名称 = '{name}'"
    df = queryDataBase(sql)
    return df[["电路名称", "A端业务", "Z端业务", "备注", "电路路由"]]


# ---------------------------------------------------------------------------
# 弹窗辅助
# ---------------------------------------------------------------------------
def customMessageBox(title, text, parent=None):
    box = QMessageBox(parent)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(QMessageBox.Warning)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec()


# ---------------------------------------------------------------------------
# 详情对话框
# ---------------------------------------------------------------------------
class AllSearchDialog(QDialog):
    """光纤光路 / 传输电路 模糊搜索结果表格，每行提供“查看”按钮。"""

    def __init__(self, df, dialog_type, parent=None):
        super().__init__(parent)
        self.dialog_type = dialog_type
        self.setWindowTitle(f"{dialog_type}查询情况")
        self.resize(1500, 600)
        self.initUI(df)

    def initUI(self, df):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(len(df))
        cols_len = len(df.columns)
        self.table.setColumnCount(cols_len)
        headers = list(df.columns)[:-1] + ["详细信息"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        if self.dialog_type == "光纤光路":
            fix_indexs = [2, 4, 5, 8]
            hidden_col_indexs = [1, 3, 6, 7]
        elif self.dialog_type == "传输电路":
            fix_indexs = [1, 2]
            hidden_col_indexs = [3]
        else:
            fix_indexs = []
            hidden_col_indexs = []

        for index in fix_indexs:
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.Fixed)
            self.table.setColumnWidth(index, 250)
        self.table.setColumnWidth(cols_len - 1, 100)

        for i in range(len(df)):
            for j in range(cols_len - 1):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
            btn = QPushButton("查看")
            btn.clicked.connect(partial(self.showDetails, df, i))
            self.table.setCellWidget(i, cols_len - 1, btn)

        for index in hidden_col_indexs:
            self.table.setColumnHidden(index, True)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def showDetails(self, df, row):
        if self.dialog_type == "光纤光路":
            detail_dialog = DetailsOlinkDialog(df, row, self)
            detail_dialog.exec()
        elif self.dialog_type == "传输电路":
            detail_dialog = DetailsCircuitDialog(df, row, self)
            detail_dialog.exec()


class DetailsOlinkDialog(QDialog):
    def __init__(self, df, row, parent=None):
        super().__init__(parent)
        self.setWindowTitle("光路详细信息")
        self.resize(800, 400)
        self.initUI(df, row)

    def initUI(self, df, row):
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("光路名称"), 0, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 0])), 0, 1)
        grid_layout.addWidget(QLabel("光路方案名称"), 0, 2)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 1])), 0, 3)

        grid_layout.addWidget(QLabel("承载的业务"), 1, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 2])), 1, 1)
        grid_layout.addWidget(QLabel("传输系统"), 1, 2)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 3])), 1, 3)

        grid_layout.addWidget(QLabel("A端站点"), 2, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 4])), 2, 1)
        grid_layout.addWidget(QLabel("Z端站点"), 2, 2)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 5])), 2, 3)

        grid_layout.addWidget(QLabel("A端机房"), 3, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 6])), 3, 1)
        grid_layout.addWidget(QLabel("Z端机房"), 3, 2)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 7])), 3, 3)

        path_label = QLabel("文本路由")
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(str(df.iloc[row, len(df.columns) - 1]))

        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(path_label)
        main_layout.addWidget(text_edit)
        main_layout.addWidget(close_button)
        self.setLayout(main_layout)


class DetailsCircuitDialog(QDialog):
    def __init__(self, df, row, parent=None):
        super().__init__(parent)
        self.setWindowTitle("电路详细信息")
        self.resize(800, 600)
        self.initUI(df, row)

    def initUI(self, df, row):
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("电路名称"), 0, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 0])), 0, 1)

        grid_layout.addWidget(QLabel("A端业务"), 1, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 1])), 1, 1)

        grid_layout.addWidget(QLabel("Z端业务"), 2, 0)
        grid_layout.addWidget(QLineEdit(str(df.iloc[row, 2])), 2, 1)

        remark_label = QLabel("备注")
        remark_text = QTextEdit()
        remark_text.setReadOnly(True)
        remark_text.setText(str(df.iloc[row, 3]))

        route_label = QLabel("电路路由")
        route_text = QTextEdit()
        route_text.setReadOnly(True)
        route_text.setText(str(df.iloc[row, 4]))

        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(remark_label)
        main_layout.addWidget(remark_text)
        main_layout.addWidget(route_label)
        main_layout.addWidget(route_text)
        main_layout.addWidget(close_button)
        self.setLayout(main_layout)


# ---------------------------------------------------------------------------
# 查询工作线程
# ---------------------------------------------------------------------------
class QueryThread(QThread):
    """在后台线程中执行一个纯查询函数，并通过信号回传结果。"""

    result_signal = Signal(object)
    error_signal = Signal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._func(*self._args, **self._kwargs)
            self.result_signal.emit(result)
        except Exception as exc:  # noqa: BLE001
            self.error_signal.emit(str(exc))


# ---------------------------------------------------------------------------
# 光路查询页面
# ---------------------------------------------------------------------------
class OlinkPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_OlinkPageWidget()
        self.ui.setupUi(self)

        # 状态栏标签（原 main 窗口通过 status_label 显示状态，这里在页面底部补充一个）
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #c94f6d;")
        self.ui.verticalLayout_18.addWidget(self.status_label)

        # 保存工作线程引用，防止被垃圾回收
        self._threads = []

        self._connectSignals()

    def _connectSignals(self):
        self.ui.a_ne_le.returnPressed.connect(self.olinkReturnPress)
        self.ui.a_ne_cb.currentIndexChanged.connect(self.mergeZne)
        self.ui.search_link_bt.clicked.connect(self.olinkButtonClick)
        self.ui.search_all_olink_bt.clicked.connect(self.olinkButtonClick)
        self.ui.search_one_olink_bt.clicked.connect(self.olinkButtonClick)
        self.ui.search_all_circuit_bt.clicked.connect(self.olinkButtonClick)
        self.ui.search_one_circuit_bt.clicked.connect(self.olinkButtonClick)

    # ------------------------------------------------------------------
    # 通用状态显示与线程启动
    # ------------------------------------------------------------------
    def showStatus(self, text):
        self.status_label.setText(text)

    def _startQuery(self, func, result_slot, *args, status="查询中..."):
        self.showStatus(status)
        thread = QueryThread(func, *args)
        thread.result_signal.connect(result_slot)
        thread.error_signal.connect(self._onQueryError)
        thread.finished.connect(thread.deleteLater)
        self._threads.append(thread)
        thread.start()

    def _onQueryError(self, msg):
        self.showStatus(f"查询出错：{msg}")
        customMessageBox("错误提示", f"查询出错：{msg}", self)

    # ------------------------------------------------------------------
    # 按钮 / 输入框事件
    # ------------------------------------------------------------------
    def olinkButtonClick(self):
        btn = self.sender()
        btn_name = btn.objectName()

        if btn_name == "search_link_bt":
            self.queryOlinkText()
        elif btn_name == "search_all_olink_bt":
            self.queryAllOlink()
        elif btn_name == "search_one_olink_bt":
            self.queryOneOlink()
        elif btn_name == "search_all_circuit_bt":
            self.queryAllCircuit()
        elif btn_name == "search_one_circuit_bt":
            self.queryOneCircuit()

    def olinkReturnPress(self):
        line_edit = self.sender()
        if line_edit.objectName() == "a_ne_le":
            self.queryAneName()

    def mergeZne(self):
        ane_name = self.ui.a_ne_cb.currentText()
        if not ane_name:
            return
        self._startQuery(searchZne, self._onZneResult, ane_name, status="正在加载Z端网元...")

    # ------------------------------------------------------------------
    # 查询动作（校验输入 -> 启动工作线程）
    # ------------------------------------------------------------------
    def queryAneName(self):
        keys = self.ui.a_ne_le.text().split(" ")
        if not keys or all(not k for k in keys):
            return
        self._startQuery(searchAne, self._onAneResult, keys, status="正在查找A端网元...")

    def queryOlinkText(self):
        ane_name = self.ui.a_ne_cb.currentText()
        zne_name = self.ui.z_ne_cb.currentText()
        if not ane_name:
            self.showStatus("请先选择A，Z端网元")
            return
        self._startQuery(searchOlink, self._onOlinkTextResult, ane_name, zne_name,
                         status="正在查询链路...")

    def queryAllOlink(self):
        text = self.ui.olink_key_le.text().strip()
        if text == "":
            self.showStatus("请输入查询关键字")
            return
        keys = text.split(" ")
        self._startQuery(searchAllOlink, self._onAllOlinkResult, keys, status="正在模糊查询光路...")

    def queryOneOlink(self):
        olink_name = self.ui.olink_key_le.text().strip()
        if len(olink_name) == 0:
            self.showStatus("请输入光路名称")
            return
        self._startQuery(queryOneOlink, self._onOneOlinkResult, olink_name,
                         status="正在精准查询光路...")

    def queryAllCircuit(self):
        text = self.ui.circuit_keys_le.text().strip()
        if text == "":
            self.showStatus("请输入查询关键字")
            return
        keys = text.split(" ")
        self._startQuery(searchAllCircuit, self._onAllCircuitResult, keys,
                         status="正在模糊查询电路...")

    def queryOneCircuit(self):
        circuit_name = self.ui.circuit_keys_le.text().strip()
        if len(circuit_name) == 0:
            self.showStatus("请输入电路名称")
            return
        self._startQuery(queryOneCircuit, self._onOneCircuitResult, circuit_name,
                         status="正在精准查询电路...")

    # ------------------------------------------------------------------
    # 线程结果回调（主线程中刷新界面）
    # ------------------------------------------------------------------
    def _onAneResult(self, ane_names):
        self.ui.a_ne_cb.clear()
        self.ui.a_ne_cb.addItems(ane_names)
        if not ane_names:
            self.showStatus("查无此网元！")
            customMessageBox("错误提示", "查无此网元！", self)
        else:
            self.showStatus(f"找到 {len(ane_names)} 个A端网元")

    def _onZneResult(self, zne_names):
        self.ui.z_ne_cb.clear()
        self.ui.z_ne_cb.addItems(zne_names)

    def _onOlinkTextResult(self, result):
        olink_name, olink_text = result
        if olink_name == "" or olink_name == "nan":
            self.showStatus("AZ端网元之间拓扑连接未关联光路，请手工查询")
            customMessageBox("错误提示", "AZ端网元之间拓扑连接未关联光路，请手工查询", self)
            self.ui.olink_name_le.setText("")
            self.ui.olink_text_te.setPlainText("")
            return
        self.ui.olink_name_le.setText(olink_name)
        self.ui.olink_text_te.setPlainText(olink_text)
        self.showStatus("链路查询完成")

    def _onAllOlinkResult(self, result_df):
        if result_df.shape[0] == 0:
            self.showStatus("找不到这些关键字的光路")
            customMessageBox("错误提示", "找不到这些关键字的光路", self)
            return
        dialog = AllSearchDialog(result_df, "光纤光路", self)
        dialog.exec()

    def _onOneOlinkResult(self, result_df):
        if result_df.shape[0] == 0:
            name = self.ui.olink_key_le.text().strip()
            self.showStatus(f"找不到光路:{name}!")
            customMessageBox("错误提示", f"找不到光路:{name}!", self)
            return
        dialog = DetailsOlinkDialog(result_df, 0, self)
        dialog.exec()

    def _onAllCircuitResult(self, result_df):
        if result_df.shape[0] == 0:
            self.showStatus("找不到这些关键字的电路")
            customMessageBox("错误提示", "找不到这些关键字的电路", self)
            return
        dialog = AllSearchDialog(result_df, "传输电路", self)
        dialog.exec()

    def _onOneCircuitResult(self, result_df):
        if result_df.shape[0] == 0:
            name = self.ui.circuit_keys_le.text().strip()
            self.showStatus(f"找不到电路:{name}!")
            customMessageBox("错误提示", f"找不到电路:{name}!", self)
            return
        dialog = DetailsCircuitDialog(result_df, 0, self)
        dialog.exec()
