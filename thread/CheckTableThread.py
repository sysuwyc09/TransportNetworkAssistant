# 检查数据库表格是否存在线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class CheckTableThread(QThread):
    tableReady = Signal(str)  # 信号：表名和查询结果
    resultReady = Signal(bool)  # 信号：表名和查询结果
    
    def __init__(self, analysis_type, parent=None):
        super().__init__(parent)
        self.analysis_type = analysis_type
    
    def run(self):
        # 根据分析类型确定需要检查的表格
        tables_to_check = self.get_tables_for_analysis()
        is_check = True
        try:
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            # 检查每个表格是否存在并查询数据
            for table in tables_to_check:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    # 表格存在，查询数据表的列数，行数
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    # 表格存在，查询数据表的行数
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    row_count = cursor.fetchone()[0]
                    self.tableReady.emit(table + f': 表格校验通过, 列数: {len(columns)}, 行数: {row_count}')
                else:
                    if table == '箱体上联OLT跳纤路径表':
                        self.tableReady.emit(table + ': 不存在这个表格,请先执行光设施分析')
                    else:
                        self.tableReady.emit(table + '：不存在这个表格，请先在资源数据中导入表格')
                    self.resultReady.emit(False)
                    is_check = False
            if is_check:
                self.resultReady.emit(True)
        except Exception as e:
            self.tableReady.emit(f'数据库操作错误: {e}')
            self.resultReady.emit(False)
        finally:
            conn.close()
    
    def get_tables_for_analysis(self):
        """根据分析类型返回需要检查的表格列表"""
        if self.analysis_type == "光设施":
            return ["OLT网元","机房", "中继段",'光交箱','分纤箱','主光路']
        elif self.analysis_type == "OLT端口":
            return ['OLT网元', 'PON端口', '机房', '华为PON单板','中兴PON单板']
        elif self.analysis_type == "主光路":
            return ['主光路', '箱体上联OLT跳纤路径表','光交箱','分纤箱','ODF']

# 导入文件线程