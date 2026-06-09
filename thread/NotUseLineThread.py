# 分析零利用率的光缆段

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class NotUseLineThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
    
    def run(self):
        self.state_signal.emit('正在校验数据库表格')
        needs_files = ['中继段至光缆段','中继段','光缆段']
        # 查看data\transportNetwork.db是否存在这些表
        conn = sqlite3.connect('data/transportNetwork.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        for table in needs_files:
            if table not in tables:
                self.error_signal.emit(f'数据库表格中不存在{table}表')
                return;
        relay_to_line_df = pd.read_sql_query(f'SELECT * FROM {needs_files[0]}',conn)
        relay_df = pd.read_sql_query(f'SELECT * FROM {needs_files[1]}',conn)
        line_df = pd.read_sql_query(f'SELECT * FROM {needs_files[2]}',conn)
        # 筛选清单
        line_df = line_df[line_df['红线范围']=='红线外']
        line_df = line_df[line_df['资源状态']=='在网']

        conn.close()
        self.state_signal.emit('正在分析零利用率的光缆段')
        table,not_use_line_df,sub_df_1,sub_df_2,sub_df_3 = self.analyzeNotUseLine(relay_to_line_df,relay_df,line_df)
        self.state_signal.emit('正在生成零利用率光缆段分析结果')
        with pd.ExcelWriter(self.file_path) as writer:
            table.to_excel(writer,sheet_name='零利用率光缆段统计结果',index=False)
            not_use_line_df.to_excel(writer,sheet_name='零利用率光缆段清单',index=False)
            sub_df_1.to_excel(writer,sheet_name='无中继段疑似垃圾数据清单',index=False)
            sub_df_2.to_excel(writer,sheet_name='实际有占用清单',index=False)
            sub_df_3.to_excel(writer,sheet_name='实际无占用清单',index=False)
        self.state_signal.emit('零利用率光缆段分析结果已生成！')
    
    def analyzeNotUseLine(self,relay_to_line_df,relay_df,line_df):
        line_df['初验时间'] = pd.to_datetime(line_df['初验时间'],errors='coerce')
        line_df['时间类型'] = line_df['初验时间'].apply(self.timeType)
        relay_df = relay_df[['名称','中继纤芯数量','占用数量']].rename(columns={'名称':'中继段'})
        relay_to_line_df = relay_to_line_df.merge(relay_df,on='中继段',how='left')
        relay_to_line_df = relay_to_line_df.drop_duplicates()
        line_table = pd.pivot_table(relay_to_line_df,index=['光缆段'],aggfunc={'中继段':'count','中继纤芯数量':'sum','占用数量':'sum'})
        line_table = line_table.reset_index().rename(columns={'光缆段':'名称','中继段':'中继段数','中继纤芯数量':'成端纤芯数','占用数量':'纤芯占用数'})
        line_df = line_df.merge(line_table,on='名称',how='left')
        # 聚合中继段详细情况
        relay_to_line_df = relay_to_line_df.astype('str')
        relay_to_line_df['详细'] = relay_to_line_df['中继段'] + '(' + relay_to_line_df['占用数量'] + '/' + relay_to_line_df['中继纤芯数量'] + ')'
        line_detail_df = relay_to_line_df[['光缆段','详细']]
        line_detail_df = line_detail_df.groupby('光缆段')['详细'].agg(lambda x: ','.join(x)).reset_index().rename(columns={'光缆段':'名称'})
        line_df = line_df.merge(line_detail_df,on='名称',how='left')

        line_df['中继段数'] = line_df['中继段数'].fillna(0).astype('int')
        not_use_line_df = line_df[line_df['纤芯占用率']==0]
        # 统计表
        table = pd.pivot_table(not_use_line_df,index=['维护部门'],aggfunc={'名称':'count'})
        table = table.reset_index().rename(columns={'名称':'零利用率光缆段数'})

        # 子表1 纤芯占用率为0 且 中继段数为0
        sub_df_1 = not_use_line_df[not_use_line_df['中继段数']==0]
        table1 = pd.pivot_table(sub_df_1,index=['维护部门'],aggfunc={'名称':'count'})
        table1 = table1.reset_index().rename(columns={'名称':'零利用率光缆段数-无中继段'})
        table = table.merge(table1,on='维护部门',how='left')
        # 子表2 纤芯占用率为0 且 纤芯占用数不为0
        sub_df_2 = not_use_line_df[not_use_line_df['纤芯占用数']>0]
        table2 = pd.pivot_table(sub_df_2,index=['维护部门'],aggfunc={'名称':'count'})
        table2 = table2.reset_index().rename(columns={'名称':'零利用率光缆段数-实际有占用'})
        table = table.merge(table2,on='维护部门',how='left')
        # 子表3 纤芯占用率为0 且 纤芯占用数确实为0 且 中继段数不为0
        sub_df_3 = not_use_line_df[(not_use_line_df['纤芯占用数']==0) & (not_use_line_df['中继段数']>0)]
        table3 = pd.pivot_table(sub_df_3,index=['维护部门'],columns=['时间类型'],aggfunc={'名称':'count'})
        table3.columns = table3.columns.droplevel(0)
        table3 = table3.reset_index().rename(columns={
            '未满1年':'实际无占用-未满1年',
            '满1年未满2年':'实际无占用-满1年未满2年',
            '满2年未满3年':'实际无占用-满2年未满3年',
            '满3年以上':'实际无占用-满3年以上'
        })
        table = table.merge(table3,on='维护部门',how='left')
        table4 = pd.pivot_table(sub_df_3,index=['维护部门'],aggfunc={'名称':'count'})
        table4 = table4.reset_index().rename(columns={'名称':'零利用率光缆段数-实际无占用'})
        table = table.merge(table4,on='维护部门',how='left')
        table = table.fillna(0)
        table.set_index('维护部门',inplace=True)
        table.loc['合计'] = table.sum()
        table = table.reset_index()
        return table,not_use_line_df,sub_df_1,sub_df_2,sub_df_3


    def timeType(self,inSys_time):
        if pd.isna(inSys_time):
            return "满3年以上"
        # 根据时间判别未满一年，满一年未满两年，满两年未满三年，满三年以上
        now = pd.Timestamp.now()
        one_year_ago = now - pd.DateOffset(years=1)  # 1年前
        two_years_ago = now - pd.DateOffset(years=2)  # 2年前
        three_years_ago = now - pd.DateOffset(years=3)  # 3年前
        # 按区间判断
        if inSys_time >= one_year_ago:
            return "未满1年"
        elif inSys_time >= two_years_ago:
            return "满1年未满2年"
        elif inSys_time >= three_years_ago:
            return "满2年未满3年"
        else:
            return "满3年以上"


# 机房箱体分纤点级别定义业务逻辑
'''直连纤芯需要12芯以上，二级分纤点机房为本地接入；
1、OLT机房、汇聚机房：一级分纤点
2、直达一级机房：288以上【光交箱】：一级分纤点
3、直达一级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点
4、直达二级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点；循环次数4次
5、集群光交箱：就高的箱体级别
6、归属机房的光交箱、分纤箱：按照机房的分纤点级别
'''