# 更新数据库线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class UpdateDBThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号

    
    def __init__(self, table_name,df):
        super().__init__()
        self.df = df
        self.table_name = table_name
    
    def run(self):
        try:
            self.state_signal.emit('正在清洗数据')
            self.selectData()
            self.state_signal.emit('正在更新数据库数据')
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            self.df.to_sql(self.table_name, conn, if_exists='replace', index=False)
            # 更新 表格更新时间 表 table_name的更新时间 为当前时间
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M')
            # 判断表格是否存在并执行更新或插入操作
            cursor.execute("SELECT COUNT(*) FROM 表格更新时间 WHERE 表名=?", (self.table_name,))
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE 表格更新时间 SET 更新时间=? WHERE 表名=?", (now, self.table_name))
            else:
                cursor.execute("INSERT INTO 表格更新时间 (表名, 更新时间) VALUES (?, ?)", (self.table_name, now))
            conn.commit()
            conn.close()
            self.state_signal.emit("更新成功")
        except Exception as e:
            self.state_signal.emit(f"更新失败: {str(e)}")

    def selectData(self):
        if self.table_name == 'OLT网元':
            self.selectOLT()

    def selectOLT(self):
        self.df = self.df.astype(str)
        # 删除 生命周期状态列 包含 退网 的行
        self.df = self.df[~self.df['生命周期状态'].str.contains('退网')]
        # 删除 生命周期状态列 为 工程无业务 的行
        self.df = self.df[self.df['生命周期状态']!='工程无业务']
        # 删除 生命周期状态列 为 工程在建 的行
        self.df = self.df[self.df['生命周期状态']!='工程在建']

# 下载文件线程