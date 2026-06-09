'''
分析未部署千兆OLT的超1000户站点
分析超1000户站点的OLT网元数量、用户数、全量PON口数量、空闲PON口数量、PON口利用率
生成Excel表格
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class FindNoXgOltSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','千兆OLT数','用户数','全量PON口数量','空闲PON口数量','PON口利用率']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析未部署千兆OLT的超1000户站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            # site_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count','用户数':'sum'})
            # site_table.columns = ['OLT网元数量','用户数']
            # site_table = site_table.reset_index()
            # site_table = site_table[site_table['用户数'] >= 1000]
            # self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            # with pd.ExcelWriter(self.file_path) as writer:
            #     site_table.to_excel(writer,sheet_name='超1000户站点部署OLT分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析未部署千兆OLT的超1000户站点失败:' + str(e))

# 超长主光路调优分析