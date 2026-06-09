# 更新OLT管理一张表

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class UpdateOltOneTableThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    result_signal = Signal(str)

    def __init__(self, old_file_path):
        super().__init__()
        self.old_file_path = old_file_path

    def run(self):
        # try:
        self.state_signal.emit('正在读取OLT网元数据集...')
        olt_df = readDataBase('OLT网元数据集')
        if olt_df.empty:
            self.error_signal.emit('OLT网元数据集为空，请先分析OLT端口')
            return

        self.state_signal.emit('正在读取OLT上联链路表...')
        link_df = readDataBase('OLT上联链路')
        if not link_df.empty:
            link_df = self.process_link_data(link_df)
            self.state_signal.emit('正在匹配上联链路数据...')
            olt_df = olt_df.merge(link_df, on='OLT网元', how='left')

        self.state_signal.emit('正在读取旧的OLT管理一张表...')
        old_df = pd.read_excel(self.old_file_path)

        # 需要从旧表匹配的列
        match_cols = ['分公司', '区域归属', '网格',
                        '是否同路由', '同路由长度', '>300或者>800m', '是否整改',
                        '（跳纤整改）现有资源满足', '问题', '汇聚机房比例提升策略',
                        '附近汇聚距离', '目标搬迁机房']

        # 检查旧表是否包含设备IP列
        if '设备IP' not in old_df.columns:
            self.error_signal.emit('旧的OLT管理一张表缺少"设备IP"列')
            return

        # 提取旧表的匹配列（只保留存在的列）
        existing_cols = [col for col in match_cols if col in old_df.columns]
        old_match_df = old_df[['设备IP'] + existing_cols].copy()

        self.state_signal.emit('正在匹配数据...')
        # 根据设备IP列进行匹配
        olt_df = olt_df.merge(old_match_df, on='设备IP', how='left')

        # 计算站点总用户数
        if '所属站点' in olt_df.columns and '用户数' in olt_df.columns:
            site_user_df = olt_df.groupby('所属站点')['用户数'].sum().reset_index()
            site_user_df.rename(columns={'用户数': '站点总用户数'}, inplace=True)
            olt_df = olt_df.merge(site_user_df, on='所属站点', how='left')
            
            # 按站点总用户数、所属站点、用户数倒序排序
            olt_df = olt_df.sort_values(by=['站点总用户数', '所属站点', '用户数'], ascending=[False, False, False])

        # 按指定列顺序输出
        output_cols = ['分公司', '区域归属', '网格', '设备IP', 'OLT网元', '生命周期状态',
                        '所属站点', '所属机房', '机房类型', '产权单位', '机房状态', '设备型号',
                        '是否千兆', '站点总用户数', '用户数', '闲置OLT', 'PON口总数', 'PON口空闲数',
                        'XGPON口总数', 'XGPON口空闲数', '空闲业务槽数量', '上联链路数',
                        '综资关联链路', '关联BNG数', '是否同路由',
                        '同路由长度', '>300或者>800m', '是否整改', '（跳纤整改）现有资源满足',
                        '问题', '汇聚机房比例提升策略', '附近汇聚距离', '目标搬迁机房']

        # 只保留存在的列
        final_cols = [col for col in output_cols if col in olt_df.columns]
        result_df = olt_df[final_cols].copy()

        self.state_signal.emit('正在获取更新时间...')
        # 获取OLT网元数据集的更新时间
        conn = sqlite3.connect('data/transportNetwork.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 更新时间 FROM 表格更新时间 WHERE 表名='OLT网元数据集'")
        update_time = cursor.fetchone()
        conn.close()

        if update_time:
            time_suffix = update_time[0].replace(':', '-').replace(' ', '_')
        else:
            time_suffix = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

        # 生成输出文件名
        output_path = os.path.join(os.path.dirname(self.old_file_path), f'【OLT管理一张表】_{time_suffix}.xlsx')

        self.state_signal.emit('正在写入文件...')
        result_df.to_excel(output_path, index=False)

        self.state_signal.emit(f'OLT管理一张表已更新完成，共{len(result_df)}条记录')

        # except Exception as e:
        #     self.error_signal.emit(f'更新OLT管理一张表失败: {str(e)}')
    
    def process_link_data(self, link_df):
        '''
        处理OLT上联链路数据，生成上联链路数、综资关联链路、关联BNG数
        '''
        # 重命名列
        link_df.rename(columns={'OLT设备': 'OLT网元'}, inplace=True)
        
        # 生成电路名称 - 使用 apply 逐行处理
        link_df['电路名称'] = link_df.apply(lambda row: self.fixPonPath(row['连接方式'], row['传输电路名称'], row['光纤光路名称']), axis=1)
        link_df['OLTPort'] = link_df['OLT端口'].apply(self.fixOltPort)
        link_df['电路名称'] = link_df['电路名称'] + '{' + link_df['A端设备名称'] + ':' + link_df['A端端口名称'] + '<=>' + link_df['OLTPort'] + '}'
        
        # 统计上联链路数
        link_count_df = link_df.groupby('OLT网元').size().reset_index(name='上联链路数')
        
        # 统计关联BNG数（去重）
        bng_count_df = link_df.groupby('OLT网元')['A端设备名称'].nunique().reset_index(name='关联BNG数')
        
        # 生成综资关联链路字符串
        link_df = link_df.astype(str)
        link_str_df = link_df.groupby('OLT网元')['电路名称'].apply(lambda x: '//'.join(x)).reset_index()
        link_str_df.rename(columns={'电路名称': '综资关联链路'}, inplace=True)
        
        # 合并结果
        result_df = link_count_df.merge(bng_count_df, on='OLT网元', how='left')
        result_df = result_df.merge(link_str_df, on='OLT网元', how='left')
        
        return result_df
    
    def fixPonPath(self, ptype, eName, oName):
        '''
        根据连接方式、传输电路名称、光纤光路名称生成电路名称前缀
        '''
        if pd.isnull(eName) and pd.isnull(oName):
            if ptype == '尾纤直连':
                return '尾纤直连'
            else:
                return '录入缺失'
        else:
            if pd.isnull(eName):
                return str(oName) + '(光路)'
            elif pd.isnull(oName):
                return str(eName) + '(电路)'
            else:
                return '录入缺失'
    
    def fixOltPort(self, portName):
        '''
        处理OLT端口名称，提取最后4个部分的前3个
        '''
        if pd.isnull(portName):
            return "OLT端口缺失"
        else:
            parts = str(portName).split("-")
            if len(parts) >= 4:
                return "-".join(parts[-4:-1])
            else:
                return "OLT端口缺失"