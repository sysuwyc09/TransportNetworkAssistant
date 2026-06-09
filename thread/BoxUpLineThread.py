# 箱体上联方案分析

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class BoxUpLineThread(QThread):
    state_signal = Signal(str,int,str)
    def __init__(self):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(BoxUpLineThread, self).__init__()

    def run(self):
        self.state_signal.emit('正在加载中继段信息，请稍后...',0,'')
        line2Df = loadLine2Df()
        oltDf = loadOltTypeDf()
        self.state_signal.emit(f'已查询到{len(line2Df)}个跳纤中继段...',0,'')
        self.state_signal.emit('正在加载全量光交设施(超72芯分纤箱、光交箱、ODF) ...',0,'')
        self.all_dev = readDevs()
        self.state_signal.emit('已加载全量光交设施...',0,'')
        self.all_dev.rename(columns={'机房名称':'设施所属机房','业务区':'设施所属业务区'},inplace=True)
        self.all_dev['设施所属位置'] = fixSite(self.all_dev['设施所属机房'],self.all_dev['设施名称'])
        obds = list(set(list(self.all_dev['设施所属位置'])))
        self.state_signal.emit(f'已查询到{len(obds)}个光交设施...',0,'')
        # 按300一组进行分组，如果最后一组不足300则为剩余值
        obds_groups = [obds[i:i+300] for i in range(0, len(obds), 300)]
        result_dfs = []
        start_time = time.time()
        self.state_signal.emit(f'按300个为一组，共{len(obds_groups)}组光交设施进行跳纤路径分析，正在进行第1组...',0,'')
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToMany(obds_group,line2Df,oltDf,'OLT',7,15)
            if temp_df.shape[0] > 0:
                temp_df = selectBestPath(temp_df)
            result_dfs.append(temp_df)
            # 计算预估剩余时间
            elapsed_time = time.time() - start_time
            avg_time_per_group = elapsed_time / (i+1)
            remaining_groups = len(obds_groups) - (i+1)
            estimated_time = avg_time_per_group * remaining_groups
            self.state_signal.emit(f'已完成{i+1}/{len(obds_groups)}组光设施跳纤分析,',90/len(obds_groups)*(i+1),f'剩余约{int(estimated_time/60)}分{int(estimated_time%60)}秒')
        result_df = pd.concat(result_dfs)
        self.state_signal.emit(f'已完成调度方案输出',90,'')
        if result_df.shape[0] == 0:
            self.state_signal.emit('查询不到上联方案')
            return
        odevs = self.all_dev[['设施名称','设施所属位置']]
        result_df = result_df.rename(columns={'A端':'设施所属位置','B端':'目标OLT机房'})
        result_df.drop(['B端类型'],axis=1,inplace=True)
        odevs = odevs.merge(result_df,on='设施所属位置',how='left')
        odevs2 = odevs.copy().drop(['设施名称'],axis=1).rename(columns={'设施所属位置':'设施名称'})
        odevs = odevs.drop(['设施所属位置'],axis=1)
        odevs = pd.concat([odevs,odevs2],axis=0).drop_duplicates()
        writeDataBase('箱体上联OLT跳纤路径表', odevs)
        self.state_signal.emit('已完成...',100,'')


# 箱体上联纤芯紧张状态分析