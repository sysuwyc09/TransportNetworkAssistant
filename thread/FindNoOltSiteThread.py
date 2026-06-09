# 未部署OLT的汇聚站点
# 所属站点(TEXT), 机房类型(TEXT), 机房名称(TEXT), 业务级别(TEXT), 生命周期状态(TEXT)

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class FindNoOltSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','全量PON口数量','空闲PON口数量','PON口利用率','千兆PON口数量','空闲千兆PON口数量','千兆PON口利用率','是否有端口不足']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析未部署OLT的汇聚站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            house = readDataBase('机房')
            house = house[house['业务级别'].str.contains('汇聚')]
            house = house[house['机房类型'] == '传输机房']
            house = house[house['生命周期状态'] == '现网在用']
            site_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count'})
            site_table.columns = ['站点OLT网元数量']
            site_table = site_table.reset_index()
            house_table = pd.pivot_table(df,index=['所属机房'],aggfunc={'OLT网元':'count'})
            house_table = house_table.reset_index()
            house_table.columns = ['机房名称','机房OLT数量']
            house = house.merge(site_table,on='所属站点',how='left')
            house = house.merge(house_table,on='机房名称',how='left')
            house.fillna(0,inplace=True)
            house.sort_values(by=['站点OLT网元数量','机房OLT数量'],ascending=[True,True],inplace=True)
            self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            with pd.ExcelWriter(self.file_path) as writer:
                house.to_excel(writer,sheet_name='汇聚站点部署OLT分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析未部署OLT的汇聚站点失败:' + str(e))

