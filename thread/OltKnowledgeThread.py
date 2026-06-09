'''
OLT知识库线程，调用数据库data\transportNetwork.db中的'OLT网元'表格，读取指定数据后，调用PublicFunc.py中的dfToMarkdownKnowledge函数，输出到指定目录
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class OltKnowledgeThread(QThread):
    error_signal = Signal(str)
    state_signal = Signal(str)
    def __init__(self, parent=None,output_path=None):
        super().__init__(parent)
        self.output_path = output_path
    
    def run(self):
        '''
        运程函数，读取OLT表格，然后获取OLT的markdown格式文档
        '''
        if self.tableNotRequired():
            error_str =  '数据库不存在这些表格：' + '、'.join(self.tableNotRequired())
            self.error_signal.emit(f'OLT网元数据集表格{error_str}')
            return;
        
        olt_df = readDataBase('OLT网元数据集')
        pon_df = readDataBase('PON口数据集')
        
        port_info_df = self.process_port_info(pon_df)
        
        detail_cols = ['用户数','PON口总数','PON口空闲数','XGPON口总数','XGPON口空闲数']
        for col in detail_cols:
            olt_df[col] = olt_df[col].astype(int).astype(str)
        olt_df['详细信息'] = '网元:' + olt_df['OLT网元'] + ' 设备型号:'+ olt_df['设备型号'] + ' '
        for col in detail_cols:
            olt_df['详细信息'] += col + ':' + olt_df[col] + ' '
        
        olt_df = olt_df.merge(port_info_df, on='OLT网元', how='left')
        olt_df['端口情况'] = olt_df['端口情况'].fillna('')
        olt_df['详细信息'] += olt_df['端口情况']
        
        olt_df = olt_df[['所属站点','详细信息']]
        
        result = dfToMarkdownKnowledge(olt_df,self.output_path)
        if result[0]:
            self.state_signal.emit(f'OLT网元知识库已生成，路径：{self.output_path}')
        else:
            self.error_signal.emit(result[1])
    
    def process_port_info(self, pon_df):
        '''
        处理PON口数据集，按OLT网元、PON口类型、槽位号、端口状态聚合
        返回：OLT网元，端口情况
        '''
        pon_df['端口号'] = pon_df['端口号'].astype(str)
        pon_df['槽位号'] = pon_df['槽位号'].astype(str)
        
        def format_port_group(group):
            slots = sorted(group['槽位号'].unique(), key=lambda x: int(x))
            result = []
            for slot in slots:
                slot_group = group[group['槽位号'] == slot]
                occupied = sorted(slot_group[slot_group['端口状态'] == '占用']['端口号'].tolist(), key=lambda x: int(x))
                idle = sorted(slot_group[slot_group['端口状态'] == '空闲']['端口号'].tolist(), key=lambda x: int(x))
                if occupied:
                    result.append(f"{slot}槽{','.join(occupied)}口 占用")
                if idle:
                    result.append(f"{slot}槽{','.join(idle)}口 空闲")
            return '，'.join(result)
        
        port_info_df = pon_df.groupby(['OLT网元', 'PON口类型']).apply(format_port_group).reset_index()
        port_info_df.columns = ['OLT网元', 'PON口类型', '端口明细']
        
        port_info_df = port_info_df.pivot(index='OLT网元', columns='PON口类型', values='端口明细').reset_index()
        
        port_info_df['端口情况'] = ''
        if '千兆' in port_info_df.columns:
            port_info_df['端口情况'] += '千兆口：' + port_info_df['千兆'].fillna('无') + '；'
        if '普通' in port_info_df.columns:
            port_info_df['端口情况'] += '普通口：' + port_info_df['普通'].fillna('无')
        
        port_info_df['端口情况'] = port_info_df['端口情况'].str.rstrip('；')
        
        return port_info_df[['OLT网元', '端口情况']]

    def tableNotRequired(self):
        '''
        校验数据库表格是否存在满足，一次返回不满足的表格清单
        '''
        check_tales = ['OLT网元数据集', 'PON口数据集']
        conn = sqlite3.connect('data/TransportNetwork.db')
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]
        not_required_tables = [table for table in check_tales if table not in tables]
        return not_required_tables

'''
箱体及箱体上联方案的进程，读取箱体表、上联方案表，然后分别输出箱体及上联方案markdown知识库文档
'''