# 加载中继段资源的类

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class LoadRelayLineThread(QThread):
    state_signal = Signal(str)
    result_signal = Signal(pd.DataFrame)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.cols = ['名称','始端机房','终端机房','长度','纤芯数量','空闲数量','占用数量','查找项']
    
    def run(self):
        try:
            self.state_signal.emit('正在加载中继段资源，请稍后...')
            lines = readDataBase('中继段')
            lines = lines[lines['中继纤芯数量'] > 0]
            lines['长度'] = round(lines['长度']/1000,2)
            lines = lines.astype({'名称':str,'始端机房':str,'终端机房':str,'中继纤芯数量':int,'占用数量':int,'空闲数量':int})
            lines['查找项'] = lines['名称'] + lines['始端机房'] + lines['终端机房']
            lines = lines.rename(columns={'中继纤芯数量':'纤芯数量'})
            lines = lines[self.cols]
            lines.sort_values(by=['纤芯数量'],ascending=[False],inplace=True)
            lines =lines.reset_index(drop=True)
            self.result_signal.emit(lines)
        except Exception as e:
            self.state_signal.emit('加载中继段资源失败:' + str(e))



# 查找端口不足的OLT站点