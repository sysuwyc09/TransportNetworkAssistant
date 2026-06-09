# 下载文件线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class downloadThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号
    
    def __init__(self, table_names, dfs,file_path):
        super().__init__()
        self.table_names = table_names
        self.dfs = dfs
        self.file_path = file_path
    
    def run(self):
        try:
            self.state_signal.emit("正在导出文件,请稍后...")
            # 下载表格数据实现
            with pd.ExcelWriter(self.file_path) as writer:
                for table_name, df in zip(self.table_names, self.dfs):
                    df.to_excel(writer, sheet_name=table_name, index=False)
            self.state_signal.emit("导出成功！")
        except Exception as e:
            self.state_signal.emit(f"导出失败: {str(e)}")

# 查询数据库 存在的表格清单 ，匹配最后更新时间， 列名及类型，行数