# 箱体上联纤芯紧张状态分析

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class BusyBoxUplinkThread(QThread):
    state_signal = Signal(str)
    def __init__(self,dir_path):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super().__init__()
        self.dir_path = dir_path
    
    def run(self):
        try:
            self.state_signal.emit('正在加载全量箱体上联OLT机房...')
            box_uplink_df = readDataBase('箱体上联OLT跳纤路径表')
            if box_uplink_df.shape[0] == 0:
                self.state_signal.emit('查询不到箱体上联方案,请先运行箱体上联方案分析...')
                return
            self.busyBoxUplink(box_uplink_df)
            self.state_signal.emit('已完成...')
        except Exception as e:
            self.state_signal.emit('分析箱体上联纤芯紧张状态失败:' + str(e))

    def busyBoxUplink(self,box_uplink_df):
        # 根据评分选取最优方案
        box_uplink_df.sort_values(by=['设施名称','方案得分'],ascending=[True,False],inplace=True)
        best_box_uplink_df = box_uplink_df.groupby('设施名称').first().reset_index()
        all_red_uplink_df = best_box_uplink_df[best_box_uplink_df['最小空闲芯数'] <=6]
        box_df = readDataBase('光交箱')[['设施名称','容量']]
        box_red_uplink_df = all_red_uplink_df.merge(box_df,on='设施名称')
        box_red_uplink_df = box_red_uplink_df[box_red_uplink_df['容量'] >= 288]
        self.state_signal.emit(f'已查询到{box_red_uplink_df.shape[0]}个288及以上光交箱上联纤芯紧张状态...')
        dfs = []
        for i in range(len(box_red_uplink_df)):
            row = box_red_uplink_df.iloc[i]
            lines = re.findall(r'{(.*?)}\((\d+)\/(\d+)\)', row['跳纤路径'])
            temp_df = pd.DataFrame(lines,columns=['中继段','空闲芯数','芯数'])
            temp_df['设施名称'] = row['设施名称']
            dfs.append(temp_df)
        line_df = pd.concat(dfs)
        line_df['空闲芯数'] = line_df['空闲芯数'].astype(int)
        line_df['芯数'] = line_df['芯数'].astype(int)
        line_df = line_df[line_df['空闲芯数'] <= 6]
        line_table = pd.pivot_table(line_df,index=['中继段'],aggfunc={'设施名称':'count'})
        line_table.rename(columns={'设施名称':'影响288以上光交箱数'},inplace=True)
        # 将设施名称按中继段分组，并合并
        temp_grp = line_df.groupby('中继段')['设施名称'].apply(lambda x: ','.join(x)).reset_index()
        result_df = line_df[['中继段','空闲芯数','芯数']].drop_duplicates().copy()
        result_df = result_df.merge(line_table,on='中继段',how='left')
        result_df = result_df.merge(temp_grp,on='中继段',how='left')

        lines = readDataBase('中继段')
        temp_df = lines[['名称','长度']].copy().rename(columns={'名称':'中继段'})
        result_df = result_df.merge(temp_df,on='中继段',how='left')

        # 读取中继段-光缆段对应关系
        line_to_fiber = readDataBase('中继段至光缆段')
        fiber_df = line_to_fiber.merge(result_df,on='中继段').drop_duplicates()
        all_fiber = readDataBase('光缆段')
        all_fiber = all_fiber[['名称','光纤数目']].rename(columns={'名称':'光缆段','光纤数目':'光缆芯数'})
        fiber_df = fiber_df.merge(all_fiber,on='光缆段',how='left')
        temp_df = fiber_df[['光缆段']].copy().drop_duplicates()
        temp_df = temp_df.merge(line_to_fiber,on='光缆段',how='left')
        temp_df = temp_df.merge(lines,left_on='中继段',right_on='名称')
        temp_table = pd.pivot_table(temp_df,index=['光缆段'],aggfunc={'中继纤芯数量':'sum'})
        temp_table.rename(columns={'中继纤芯数量':'光缆成端数'},inplace=True)
        temp_table = temp_table.reset_index()
        fiber_df = fiber_df.merge(temp_table,on='光缆段',how='left')
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].fillna(0)
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].astype(int)
        fiber_df['光缆成端数'] = fiber_df['光缆成端数'].astype(int)
        fiber_df['是否有预留纤芯'] = '否'
        for i in range(fiber_df.shape[0]):
            row = fiber_df.iloc[i]
            if row['光缆芯数'] > row['光缆成端数']:
                fiber_df.loc[i,'是否有预留纤芯'] = '是'
        fiber_table = pd.pivot_table(fiber_df,index=['中继段'],columns=['是否有预留纤芯'],aggfunc={'中继段':'count'})
        fiber_table.columns = fiber_table.columns.droplevel(0)
        fiber_table['是否有预留纤芯'] = fiber_table['否'].apply(lambda x: '否' if x > 0 else '是')
        fiber_table = fiber_table.reset_index()[['中继段','是否有预留纤芯']]
        fiber_df['光缆成端数'] = fiber_df['光缆成端数'].astype(str)
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].astype(str)
        fiber_df['光缆段情况'] = fiber_df['光缆段'] + '(是否有预留：' + fiber_df['是否有预留纤芯'] + '【' + fiber_df['光缆成端数'] + '/' + fiber_df['光缆芯数'] + '】)'
        temp_df = fiber_df[['中继段','光缆段情况']].copy().drop_duplicates()
        temp_grp = temp_df.groupby('中继段')['光缆段情况'].apply(lambda x: ','.join(x)).reset_index()
        result_df = result_df.merge(fiber_table,on='中继段',how='left')
        result_df = result_df.merge(temp_grp,on='中继段',how='left')
        self.state_signal.emit('分析完成，正在生成表格，请稍后...')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with pd.ExcelWriter(f'{self.dir_path}/箱体上联纤芯紧张分析{dt}.xlsx') as writer:
            best_box_uplink_df.to_excel(writer,sheet_name='所有箱体上联最优方案',index=False)
            box_red_uplink_df.to_excel(writer,sheet_name='288以上光交箱上联纤芯紧张状态',index=False)
            result_df.to_excel(writer,sheet_name='288以上光交箱紧张中继段详细',index=False)
            fiber_df.to_excel(writer,sheet_name='288以上光交箱紧张光缆段详细',index=False)


# 查找中继段资源的类
#名称(TEXT), 长度(REAL), 空闲数量(REAL), 占用数量(REAL), 中继纤芯数量(REAL), 始端站点(TEXT), 终端站点(TEXT), 始端机房(TEXT), 终端机房(TEXT), 始端设施(TEXT), 终端设施(TEXT)
# class FindRelayLineThread(QThread):
#     state_signal = Signal(str)
#     result_signal = Signal(pd.DataFrame)
#     def __init__(self,parent=None,keywords=[]):
#         super().__init__(parent)
#         self.keywords = keywords
#         self.cols = ['名称','长度','中继纤芯数量','占用数量','空闲数量','始端机房','终端机房']
    
#     def run(self):
#         try:
#             self.state_signal.emit('正在查找中继段资源，请稍后...')
#             lines = readDataBase('中继段')
#             lines = lines[lines['中继纤芯数量'] > 0]
#             lines['长度'] = round(lines['长度']/1000,2)
#             lines = lines.astype({'名称':str,'始端机房':str,'终端机房':str,'中继纤芯数量':int,'占用数量':int,'空闲数量':int})
#             lines['查找项'] = lines['名称'] + lines['始端机房'] + lines['终端机房']
#             result_df = lines[lines['查找项'].apply(lambda x: self.search(x,self.keywords))]
#             result_df = result_df[self.cols]
#             result_df.sort_values(by=['中继纤芯数量'],ascending=[False],inplace=True)
#             result_df =result_df.reset_index(drop=True)
#             self.result_signal.emit(result_df)
#             self.state_signal.emit('查找完成')
#         except Exception as e:
#             self.state_signal.emit('查找中继段资源失败:' + str(e))
    
#     def search(self,text,keywords=[]):
#         for keyword in keywords:
#             if keyword not in text:
#                 return False
#         return True

# 加载中继段资源的类