# 查找端口不足的OLT站点

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class FindRedOltPortSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','全量PON口数量','空闲PON口数量','PON口利用率','千兆PON口数量','空闲千兆PON口数量','千兆PON口利用率','是否有端口不足']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析存在端口不足的OLT站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            olt_count = pd.pivot_table(df,index=['所属站点','设备型号'],aggfunc={'OLT网元':'count'})
            olt_count.columns = ['OLT网元数量']
            olt_count = olt_count.reset_index()
            olt_count = olt_count.astype(str)
            olt_count['OLT情况'] = olt_count['设备型号'] + '(' + olt_count['OLT网元数量'] + ')'
            olt_grp = olt_count.groupby('所属站点')['OLT情况'].apply(lambda x: ','.join(x)).reset_index()
            
            port_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count','PON口总数':'sum','PON口空闲数':'sum','XGPON口总数':'sum','XGPON口空闲数':'sum'})
            port_table = port_table.reset_index()
            port_table.columns = ['所属站点','OLT网元数量','全量PON口数量','空闲PON口数量','千兆PON口数量','空闲千兆PON口数量']
            port_table = port_table.merge(olt_grp,on='所属站点',how='left')
            port_table['PON口利用率'] = round((1-port_table['空闲PON口数量']/port_table['全量PON口数量'])*100,2)
            port_table['千兆PON口利用率'] = round((1-port_table['空闲千兆PON口数量']/port_table['千兆PON口数量'])*100,2)
            isRedOltPortSite_vec = np.vectorize(self.isRedOltPortSite)
            port_table['是否有端口不足'] = isRedOltPortSite_vec(port_table['空闲PON口数量'],port_table['PON口利用率'])
            port_table = port_table[self.cols]
            port_table.sort_values(by=['是否有端口不足','全量PON口数量'],ascending=[False,False],inplace=True)
            self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            with pd.ExcelWriter(self.file_path) as writer:
                port_table.to_excel(writer,sheet_name='端口资源分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析存在端口不足的OLT站点失败:' + str(e))

    def isRedOltPortSite(self,left_port_num,percent):
        if left_port_num < 5 and percent >= 90:
            return '是'
        else:
            return '否'

# 未部署OLT的汇聚站点
# 所属站点(TEXT), 机房类型(TEXT), 机房名称(TEXT), 业务级别(TEXT), 生命周期状态(TEXT)