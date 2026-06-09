# 批量A-B跳纤方案线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class DispatchABSThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,jump_num=5,dbm_num=14,file_path=''):
        super().__init__(parent)
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.file_path = file_path
    
    def run(self):
        self.state_signal.emit('正在加载需求文件信息...')
        df = pd.read_excel(self.file_path)
        df = df.astype(str)
        if 'A端' not in df.columns or 'B端' not in df.columns:
            self.error_signal.emit('需求文件格式错误，必须包含A端和B端列')
            return;
        self.state_signal.emit('正在加载中继段信息...')
        line2Df = loadLine2Df()
        self.state_signal.emit('正在分析跳纤路由...')
        results = []
        for i in range(df.shape[0]):
            a_name = df.loc[i,'A端']
            b_name = df.loc[i,'B端']
            if a_name == b_name:
                temp_df = pd.DataFrame({'A端':[a_name],'B端':[b_name],'跳纤路径':'A端等于B端'})
            else:
                temp_df = dispatchOneToOne(line2Df,a_name,b_name,self.jump_num,self.dbm_num,[])
            if temp_df.shape[0] == 0:
                temp_df = pd.DataFrame({'A端':[a_name],'B端':[b_name],'跳纤路径':'未找到符合条件的跳纤路径'})
            results.append(temp_df)
            self.state_signal.emit(f'处理进度：{i+1}/{df.shape[0]}')
        resultDf = pd.concat(results,ignore_index=True).drop_duplicates().reset_index(drop=True)
        if resultDf.shape[0] == 0:
            self.error_signal.emit('未找到符合条件的跳纤路径')
        else:
            # 评估方案得分，算法如下：
            resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
            resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
            resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
            resultDf = resultDf.sort_values(by=['A端','B端','方案得分'],ascending=[False,False,False])
            best_df = resultDf.groupby(['A端','B端']).first().reset_index(drop=False)
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
            file_name = self.file_path.split('/')[-1].split('.')[0]
            out_file_name = f'结果\\{file_name}_批量需求跳纤路径{dt}.xlsx'
            with pd.ExcelWriter(out_file_name) as writer:
                resultDf.to_excel(writer,sheet_name='所有跳纤路径',index=False)
                best_df.to_excel(writer,sheet_name='最优跳纤路径',index=False)
            os.startfile(out_file_name)
            self.state_signal.emit(f'已将结果保存至{out_file_name}')

# 集中跳纤至OLT、CRAN机房的线程