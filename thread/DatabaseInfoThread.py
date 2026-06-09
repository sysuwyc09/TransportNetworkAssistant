# 查询数据库 存在的表格清单 ，匹配最后更新时间， 列名及类型，行数

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class DatabaseInfoThread(QThread):
    resultReady = Signal(pd.DataFrame)
    state_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            self.state_signal.emit("正在查询数据库,请稍后...")
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            # 获取所有表格名称
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            data = []
            for table in tables:
                # 获取表格最后更新时间
                cursor.execute(f"SELECT 更新时间 FROM 表格更新时间 WHERE 表名='{table}'")
                update_time = cursor.fetchone()
                update_time = update_time[0] if update_time else '未知'
                # 获取列名和类型
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                columns_info = ', '.join([f"{col[1]}({col[2]})" for col in columns])
                # 获取行数
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                data.append({
                    '表名': table,
                    '列名及类型': columns_info,
                    '行数': row_count,
                    '最后更新时间': update_time,
                })
            conn.close()
            df = pd.DataFrame(data)
            self.resultReady.emit(df)
            self.state_signal.emit("查询完成")
        except Exception as e:
            self.state_signal.emit(f"查询失败: {str(e)}")

# 分析OLT网元端口情况