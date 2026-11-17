# 更新OLT管理一张表

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re



# 更新拓扑连接关联文本路由的线程
class UpdateOlinkThread(QThread):
    state_signal = Signal(str)
    # 新增信号，用于请求主线程显示缺少必备列的提示框，文件名，缺失列名，文件列名
    show_dialog_signal = Signal(str, list, list)

    # 通过初始化赋值的方式实现UI主线程传递值给子线程
    def __init__(self, folder_path):  
        super(UpdateOlinkThread, self).__init__()
        self.folder_path = folder_path
        # 文件夹必须文件
        self.required_files = {
            '传输电路': [],
            '光纤光路': [], 
            '拓扑连接': []
        }
        self.circuit_cols = ['电路名称','电路路由','A端业务设备','Z端业务设备','备注']
        self.olink_cols = ['光路名称','光路方案名称','光路长度','光路文本路由','承载的业务','传输系统','A端站点', 'A端机房', 'A端设施', 'Z端站点', 'Z端机房','Z端设施']
        self.topo_cols = ['关联光路/电路/微波段名称','关联类型','A端设备','Z端设备']

    def run(self):
        try:
            files = os.listdir(self.folder_path)
            # 遍历文件，将匹配的文件名存入对应列表
            for file in files:
                if '传输电路' in file and '$' not in file and 'xlsx' in file:
                    self.required_files['传输电路'].append(file)
                elif '光纤光路' in file and '$' not in file and 'CSV' in file:
                    self.required_files['光纤光路'].append(file)
                elif '拓扑连接' in file and '$' not in file and 'xlsx' in file:
                    self.required_files['拓扑连接'].append(file)
            # 检查是否有空列表
            for file_type, file_list in self.required_files.items():
                if not file_list:
                    self.state_signal.emit(f'文件夹中缺少{file_type}文件')
                    return
            # 更新电路
            self.updateCircuit()
            # 更新光纤光路
            self.updateOlink()
            # 更新拓扑连接
            self.updateTopologyLink()
            self.state_signal.emit('更新光路、电路数据完成！')
        except Exception as e:
            self.state_signal.emit(f'更新失败：{e}')

    def compareCloumns(self, file_name, df, required_columns):
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.show_dialog_signal.emit(file_name, missing_columns, df.columns.tolist())
            raise ValueError(f'文件「{file_name}」缺少必备列：{", ".join(missing_columns)}')
        return df
    
    # 更新电路数据
    def updateCircuit(self):
        self.state_signal.emit('正在读取电路清单...')
        circuit_df = pd.DataFrame()
        for file in self.required_files['传输电路']:
            self.state_signal.emit(f'正在读取电路清单：{file}...')
            temp_df = pd.read_excel(self.folder_path + '/' + file)
            circuit_df = pd.concat([circuit_df,temp_df])
        circuit_df = self.compareCloumns('传输电路表格',circuit_df,self.circuit_cols)
        self.state_signal.emit('正在清洗电路')
        fixUser_vec = np.vectorize(self.fixUser)
        if 'A端业务设备(电路)' in circuit_df.columns and 'Z端业务设备(电路)' in circuit_df.columns:
            circuit_df['A端业务'], circuit_df['Z端业务'] = fixUser_vec(circuit_df['A端业务设备'],circuit_df['Z端业务设备'],
                                                            circuit_df['A端业务设备(电路)'],circuit_df['Z端业务设备(电路)'])
        else:
            circuit_df['A端业务'] = circuit_df['A端业务设备']
            circuit_df['Z端业务'] = circuit_df['Z端业务设备']
        circuit_df = circuit_df.fillna('-')
        circuit_df['匹配项'] = circuit_df['电路名称'] + circuit_df['电路路由'] + circuit_df['A端业务'] + circuit_df['Z端业务'] + circuit_df['备注']
        circuit_df = circuit_df[['电路名称','电路路由','A端业务','Z端业务','备注', '匹配项']]
        writeDataBase('全量电路',circuit_df)
        self.state_signal.emit('更新电路数据完成！')

    def fixUser(self,a_user,z_user,a_user_circuit,z_user_circuit):
        
        if pd.isnull(a_user):
            if pd.isnull(a_user_circuit):
                a_user = '-'
            else:
                a_user = a_user_circuit
        if pd.isnull(z_user):
            if pd.isnull(z_user_circuit):
                z_user = '-'
            else:
                z_user = z_user_circuit
        return a_user,z_user

    # 更新光纤光路数据
    def updateOlink(self):
        dfs = []
        for file in self.required_files['光纤光路']:
            self.state_signal.emit(f'正在读取光纤光路清单：{file}...')
            temp_df  = readCsvFile(self.folder_path + '/' + file)
            dfs.append(temp_df)
        olink_df = pd.concat(dfs,ignore_index=True)
        olink_df = self.compareCloumns('光纤光路表格',olink_df,self.olink_cols)
        olink_df = olink_df[self.olink_cols]
        self.state_signal.emit('正在清洗光纤光路')
        # 清除子光路,特征 子光路无文本路由
        olink_df = olink_df.astype(str)
        olink_df = olink_df[olink_df['光路文本路由'] != '']
        olink_df = olink_df[olink_df['A端设施'] != '']
        olink_df = olink_df[olink_df['Z端设施'] != '']
        olink_df['匹配项'] = olink_df['光路名称'] + olink_df['A端站点'] + olink_df['Z端站点']
        writeDataBase('全量光路',olink_df)
        self.state_signal.emit('光纤光路数据更新完成！')

    # 更新拓扑连接数据
    def updateTopologyLink(self):
        self.state_signal.emit('正在读取拓扑连接清单...')
        dfs = []
        for file in self.required_files['拓扑连接']:
            self.state_signal.emit(f'正在读取拓扑连接清单：{file}...')
            temp_df = pd.read_excel(self.folder_path + '/' + file)
            dfs.append(temp_df)
        topo_df = pd.concat(dfs,ignore_index=True)
        topo_df = self.compareCloumns('拓扑连接表格',topo_df,self.topo_cols)
        topo_df = topo_df[self.topo_cols]
        self.state_signal.emit('正在清洗拓扑连接数据...')
        topo_df = topo_df.astype(str)
        # topo_df = topo_df[topo_df['关联类型'].isin(['电路', '光路'])]
        # 剔除A端设备为空，Z端设备为空的记录，且A端设备=Z端设备的记录
        topo_df = topo_df[topo_df['A端设备'] != '']
        topo_df = topo_df[topo_df['Z端设备'] != '']
        topo_df = topo_df[topo_df['A端设备'] != topo_df['Z端设备']]
        topo_df['拓扑连接名称'] = topo_df['A端设备'] + "<==>" + topo_df['Z端设备']
        # topo_df = topo_df[['关联光路/电路/微波段名称','拓扑连接名称']]
        topo_df = topo_df.rename(columns={'关联光路/电路/微波段名称':'光电路名称'})
        sql = '''
            select 光路名称 as 光电路名称, 光路文本路由 as 文本路由
            from 全量光路
        '''
        temp_olink = queryDataBase(sql)
        sql = '''
            select 电路名称 as 光电路名称, 电路路由 as 文本路由
            from 全量电路
        '''
        temp_circuit = queryDataBase(sql)
        temp_df = pd.concat([temp_olink,temp_circuit])
        temp_df = temp_df.drop_duplicates()
        topo_df = pd.merge(topo_df, temp_df, on='光电路名称', how='left')
        writeDataBase('拓扑连接关联',topo_df)
        self.state_signal.emit('拓扑连接关联数据更新完成！')
