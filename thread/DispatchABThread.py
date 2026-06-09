# 单点A-B跳纤方案线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class DispatchABThread(QThread):
    state_signal = Signal(str) 
    def __init__(self,parent=None,a_name='',b_name='',jump_num=5,dbm_num=14,must_devs=[],not_devs=[]):
        super().__init__(parent)
        self.a_name = a_name
        self.b_name = b_name
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.must_devs = must_devs
        self.not_devs = not_devs
    
    def run(self):
        try:
            self.state_signal.emit('正在加载中继段信息...')
            line2Df = loadLine2Df()
            resultDf = dispatchOneToOne(line2Df,self.a_name,self.b_name,self.jump_num,self.dbm_num,self.not_devs)
            if resultDf.shape[0] == 0:
                self.state_signal.emit('未找到符合条件的跳纤路径')
            else:
                if self.must_devs:
                    for dev in self.must_devs:
                        resultDf = resultDf[resultDf['跳纤路径'].str.contains(dev)]
                if resultDf.shape[0] == 0:
                    self.state_signal.emit('未找到符合条件的跳纤路径')
                else:
                    self.state_signal.emit(f'已找到{resultDf.shape[0]}条符合条件的跳纤路径')
                    # 评估方案得分，算法如下：
                    resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
                    resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
                    resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
                    resultDf = resultDf.sort_values(by='方案得分',ascending=False)
                    dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
                    # 清除a_name和b_name不符合文件命名的字符
                    temp_a_name = re.sub(r'[^\w]','',self.a_name)
                    temp_b_name = re.sub(r'[^\w]','',self.b_name)
                    out_file_name = f'结果\\{temp_a_name}_{temp_b_name}_跳纤路径{dt}.xlsx'
                    resultDf.to_excel(out_file_name,index=False)
                    os.startfile(out_file_name)
                    self.state_signal.emit(f'已将结果保存至{out_file_name}')
        except Exception as e:
            self.state_signal.emit(f'发生错误：{e}')


# 批量A-B跳纤方案线程