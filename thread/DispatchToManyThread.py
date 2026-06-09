# 集中跳纤至OLT、CRAN机房的线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class DispatchToManyThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,jump_num=5,dbm_num=14,file_path='',b_type='CRAN'):
        super().__init__(parent)
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.file_path = file_path
        self.b_type = b_type
    
    def run(self):
        self.state_signal.emit('正在加载需求文件信息...')
        df = pd.read_excel(self.file_path)
        df = df.astype(str)
        if '需求名称' not in df.columns:
            self.error_signal.emit('需求文件格式错误，必须包含需求名称列')
            return;
        obds = df['需求名称'].tolist()
        if len(obds) == 0:
            self.error_signal.emit('需求行为空')
            return;
        self.state_signal.emit(f'共{len(obds)}个需求，将按500一组进行分析')
        # 按500一组进行分组，如果最后一组不足500则为剩余值
        obds_groups = [obds[i:i+500] for i in range(0, len(obds), 500)]

        self.state_signal.emit('正在加载中继段信息...')
        line2Df = loadLine2Df()
        self.state_signal.emit(f'正在加载{self.b_type}机房信息...')
        if self.b_type == 'CRAN':
            b_df = loadCranTypeDf()
        elif self.b_type == 'OLT':
            b_df = loadOltTypeDf()
        self.state_signal.emit('正在分析跳纤路由...')
        result_dfs = []
        start_time = time.time()
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToMany(obds_group,line2Df,b_df,self.b_type,self.jump_num,self.dbm_num)
            result_dfs.append(temp_df)
            # 计算预估剩余时间
            elapsed_time = time.time() - start_time
            avg_time_per_group = elapsed_time / (i+1)
            remaining_groups = len(obds_groups) - (i+1)
            estimated_time = avg_time_per_group * remaining_groups
            self.state_signal.emit(f'已完成{i+1}/{len(obds_groups)}组光设施跳纤分析,剩余约{int(estimated_time/60)}分{int(estimated_time%60)}秒')
        resultDf = pd.concat(result_dfs,ignore_index=True).drop_duplicates().reset_index(drop=True)
        if resultDf.shape[0] == 0:
            self.error_signal.emit(f'未找到符合条件的跳纤路径')
            return;
        resultDf['最小空闲芯数评分'] = resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
        # 评估方案得分，算法如下：
        resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
        resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
        resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
        resultDf = resultDf.sort_values(by=['A端','方案得分'],ascending=[False,False])
        best_df = resultDf.groupby(['A端']).first().reset_index(drop=False)
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        file_name = self.file_path.split('/')[-1].split('.')[0]
        out_file_name = f'结果\\{file_name}_需求至{self.b_type}的跳纤路径{dt}.xlsx'

        all_df = pd.DataFrame({'A端':obds})
        all_df = pd.merge(all_df,resultDf,on='A端',how='left')
        not_df = all_df[all_df['跳纤路径'].isnull()].copy()
        not_df['跳纤路径'] = '未找到符合条件的跳纤路径'
        self.state_signal.emit('分析完成，正在生成表格中')
        with pd.ExcelWriter(out_file_name) as writer:
            all_df.to_excel(writer,sheet_name='所有跳纤路径',index=False)
            best_df.to_excel(writer,sheet_name='最优跳纤路径',index=False)
            not_df.to_excel(writer,sheet_name='未找到跳纤路径',index=False)
        os.startfile(out_file_name)
        self.state_signal.emit(f'已将结果保存至{out_file_name}')


'''
通报弱光清单分析
1、分析C+光模块替换分析
2、分析可优化主光路清单,选取不能替换的光模块PON口
3、弱光ODB经纬度匹配,全量匹配
4、展开弱光匹配
''' 