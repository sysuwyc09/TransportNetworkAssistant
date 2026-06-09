# 导入文件线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class ImportFileThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号
    result_signal = Signal(pd.DataFrame)  # 列名和数据信号
    
    def __init__(self, file_paths, table_name, header_line):
        super().__init__()
        self.file_paths = file_paths
        self.table_name = table_name
        self.header_line = header_line
    
    def run(self):
        try:
            self.state_signal.emit("正在读取文件,请稍后...")
            # 读取文件到DataFrame
            dfs = []
            for file in self.file_paths:
                if file.endswith('.xlsx') or file.endswith('.XLSX'):
                    df = pd.read_excel(file,header=self.header_line-1)
                    dfs.append(df)
                if file.endswith('.csv') or file.endswith('.CSV'):
                    df = readCsvFile(file,header=self.header_line-1)
                    dfs.append(df)
            df = pd.concat(dfs, ignore_index=True)
            if self.table_name == '中继段':
                self.convertLine(df)
            # 发送状态信号
            self.state_signal.emit("导入成功,请选择对应文件列")
            # 发送结果信号
            self.result_signal.emit(df)
        except Exception as e:
            self.state_signal.emit(f"导入失败: {str(e)}")
            self.result_signal.emit(pd.DataFrame)

    def convertLine(self,df):
        value_vars = df.columns.tolist()[16:]
        result = df.melt(id_vars=['名称'], value_vars=value_vars,value_name='光缆段').drop(columns=['variable'])  # 移除不需要的variable列
        # 重置索引
        result = result.reset_index(drop=True)
        result = result[result['光缆段'].notnull()]
        result.rename(columns={'名称':'中继段'},inplace=True)
        writeDataBase('中继段至光缆段',result)

# 更新数据库线程