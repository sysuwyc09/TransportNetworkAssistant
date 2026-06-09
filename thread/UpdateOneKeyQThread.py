'''
更新一键数据线程
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class UpdateOneKeyQThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    
    def __init__(self, folder_path=''):
        super().__init__()
        self.folder_path = folder_path
        self.file_type_cols = [
            'OLT网元', '主光路', 'PON端口', '中继段', '光缆段', '站点', '机房', '光交箱', '分纤箱', 'ODF', '集群管理', '华为PON单板','中兴PON单板','OLT上联链路'
        ]
        self.file_cols = [
            (['网元名称', '所属机房', '设备型号', '设备IP','生命周期状态'],['str','str','str','str','str']),
            (['OLT名称', 'PON口', 'PON下挂ONU数量', 'OBD所属对象', '光路名称', '光路长度','光路文本路由'],['str','str','int','str','str','float','str']),
            (['所属传输网元', '端口名称', 'PONID', '端口状态', 'PON口下挂用户数', '端口子类型'],['str','str','str','str','int','str']),
            (['名称', '长度', '空闲数量', '占用数量', '中继纤芯数量', '始端站点', '终端站点', '始端机房','终端机房', '始端设施', '终端设施'],['str','float','int','int','int','str','str','str','str','str','str']),
            (['名称','所属光缆','实际长度','纤芯占用率','光纤数目','业务级别','敷设方式','维护部门','红线范围','初验时间','资源状态'],['str','str','float','float','int','str','str','str','str','str','str']),
            (['站点名称', '所属区县', '乡镇街道'],['str','str','str']),
            (['所属站点', '机房类型', '机房名称', '业务级别', '生命周期状态','产权单位'],['str','str','str','str','str','str']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设备名称','集群列表'],['str','str']),
            (['所属网元','槽位号','单板类型','单板状态'],['str','str','str','str']),
            (['网元名称','板卡槽位','板卡类型','板卡状态'],['str','str','str','str']),
            (['传输电路名称','光纤光路名称','A端设备名称','A端端口名称','OLT设备','OLT端口','连接方式'],['str','str','str','str','str','str','str']),
        ]
        self.file_rules = [
            {'keyword': 'OLT设备', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {'所属位置点/机房': '所属机房', '设备IP地址（省内系统：网管IP）': '设备IP'}},
            {'keyword': '主光路', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {'PON口名称':'PON口'}},
            {'keyword': 'PON端口', 'file_type': 'xlsx', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '中继段', 'file_type': 'CSV', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '光缆段', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '站点管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '机房管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '光交接箱', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '光分纤箱', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': 'ODF', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '集群管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '单板报表', 'file_type': 'xlsx', 'single': True, 'header': 3, 'rename_cols': {}},
            {'keyword': 'card_query', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': 'OLT上联链路', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
        ]
    
    def run(self):
        try:
            self.state_signal.emit('开始检查需求文件...')
            missing_files = self.check_required_files()
            if missing_files:
                self.error_signal.emit('缺失以下必需文件：\n' + '\n'.join(missing_files))
                return
            
            self.state_signal.emit('文件检查通过，开始导入数据...')
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            
            for i, table_name in enumerate(self.file_type_cols):
                self.state_signal.emit(f'正在导入 {table_name}...')
                df = self.read_table_data(i)
                if df.empty:
                    self.state_signal.emit(f'{table_name} 数据为空，跳过')
                    continue
                if table_name == '中继段':
                    self.convertLine(df, cursor)
                if table_name == 'OLT网元':
                    df = self.selectOLT(df)
                # 筛选数据    
                df = self.process_data(df, i)

                df.to_sql(table_name, conn, if_exists='replace', index=False)
                self.update_table_time(cursor, table_name)
                

                
                conn.commit()
                self.state_signal.emit(f'{table_name} 导入完成，共 {len(df)} 条记录')
            
            conn.close()
            self.state_signal.emit('一键更新数据库完成！')
        
        except Exception as e:
            self.error_signal.emit(f'一键更新数据库失败: {str(e)}')
    
    def update_table_time(self, cursor, table_name):
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M')
        cursor.execute("SELECT COUNT(*) FROM 表格更新时间 WHERE 表名=?", (table_name,))
        if cursor.fetchone()[0] > 0:
            cursor.execute("UPDATE 表格更新时间 SET 更新时间=? WHERE 表名=?", (now, table_name))
        else:
            cursor.execute("INSERT INTO 表格更新时间 (表名, 更新时间) VALUES (?, ?)", (table_name, now))
    
    def selectOLT(self, df):
        df = df.astype(str)
        df = df[~df['生命周期状态'].str.contains('退网')]
        df = df[df['生命周期状态']!='工程无业务']
        df = df[df['生命周期状态']!='工程在建']
        return df
    
    def convertLine(self, df, cursor):
        value_vars = df.columns.tolist()[16:]
        result = df.melt(id_vars=['名称'], value_vars=value_vars, value_name='光缆段').drop(columns=['variable'])
        result = result.reset_index(drop=True)
        result = result[result['光缆段'].notnull()]
        result.rename(columns={'名称': '中继段'}, inplace=True)
        result.to_sql('中继段至光缆段', cursor.connection, if_exists='replace', index=False)
        self.update_table_time(cursor, '中继段至光缆段')
        cursor.connection.commit()
        self.state_signal.emit('中继段至光缆段 导入完成')
    
    def check_required_files(self):
        missing_files = []
        files = os.listdir(self.folder_path)
        
        for i, rule in enumerate(self.file_rules):
            found = False
            for file in files:
                if rule['keyword'] in file and file.endswith('.' + rule['file_type']):
                    found = True
                    break
            if not found:
                missing_files.append(f"{self.file_type_cols[i]}: 需要包含'{rule['keyword']}'的{rule['file_type']}文件")
        
        return missing_files
    
    def read_table_data(self, index):
        rule = self.file_rules[index]
        files = os.listdir(self.folder_path)
        matched_files = [f for f in files if rule['keyword'] in f and f.endswith('.' + rule['file_type'])]
        
        dfs = []
        for file in matched_files:
            file_path = os.path.join(self.folder_path, file)
            if rule['file_type'] == 'xlsx':
                df = pd.read_excel(file_path, header=rule['header'])
            else:
                df = readCsvFile(file_path, header=rule['header'])
            dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        return pd.concat(dfs, ignore_index=True)
    
    def process_data(self, df, index):
        table_cols = self.file_cols[index][0]
        col_types = self.file_cols[index][1]
        rename_cols = self.file_rules[index]['rename_cols']
        
        df = df.rename(columns=rename_cols)
        
        df = df[[col for col in table_cols if col in df.columns]]
        
        for i, col in enumerate(table_cols):
            if col in df.columns:
                if col_types[i] == 'int':
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                elif col_types[i] == 'float':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.drop_duplicates()
        
        return df


# 更新OLT管理一张表