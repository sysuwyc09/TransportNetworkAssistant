'''
箱体及箱体上联方案的进程，读取箱体表、上联方案表，然后分别输出箱体及上联方案markdown知识库文档
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class BoxKnowledgeThread(QThread):
    error_signal = Signal(str)
    state_signal = Signal(str)
    def __init__(self, parent=None,output_dir=None):
        super().__init__(parent)
        self.output_dir = output_dir
    
    def run(self):
        '''
        运程函数，读取箱体表、上联方案表，然后分别输出箱体及上联方案markdown知识库文档
        '''
        if self.tableNotRequired():
            self.error_signal.emit('数据库不存在这些表格：' + '、'.join(self.tableNotRequired()))
            return;
        self.state_signal.emit('开始读取箱体清单...')
        all_dev = readBoxKnowledge()
        # 测试只取200数据测试，正式版全选
        # all_dev = all_dev.head(200)
        all_dev = self.getAllDev(all_dev)
        self.state_signal.emit('箱体清单读取完成')
        self.state_signal.emit('开始读取箱体上联方案...')
        grped = all_dev.groupby('所属区县')
        self.state_signal.emit('正在生成箱体知识库...')
        for area,group in grped:
            all_dev, uplink_df = self.getDevUplink(group)
            now = datetime.datetime.now().strftime('%Y%m%d%H%M')
            self.devToKnowledge(all_dev,now,area)
            self.uplinkToKnowledge(uplink_df,now,area)
        self.state_signal.emit('已完成')


    def uplinkToKnowledge(self,uplink_df,now,area):
        '''
        将箱体上联方案表转换为Dify知识库格式的Markdown文档
        '''
        uplink_df['跳纤路径'] = uplink_df['跳纤路径'].apply(self.fixPonLine)
        uplink_df['详细信息'] = '设施名称:' + uplink_df['设施名称'] + ' '
        uplink_df['最小空闲芯数'] = uplink_df['最小空闲芯数'].astype(int)

        uplink_df = uplink_df.astype(str)
        uplink_df['详细信息'] = uplink_df['详细信息'] + '上联机房:' + uplink_df['目标OLT机房'] + '【' + uplink_df['机房详细信息'] + '】 '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '上联路由:' + uplink_df['跳纤路径'] + ' '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '【空闲芯数:' + uplink_df['最小空闲芯数'] + '芯 | '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '跳纤距离:' + uplink_df['跳纤距离'] + 'km | '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '光衰预算:' + uplink_df['光衰预算'] + 'dB】'

        uplink_df = uplink_df[['设施名称','详细信息']]
        uplink_df = uplink_df.drop_duplicates()
        flag,result = dfToMarkdownKnowledge(uplink_df,self.output_dir+'/箱体上联方案_'+area+'_'+now+'.md')
        if flag:
            self.state_signal.emit(result)
        else:
            self.error_signal.emit(result)

    def fixPonLine(self,path):
        '''
        修正跳纤路径，只保留跳纤信息
        '''
        path = '=>' + path + '<='
        points = re.findall('=>(.*?)<=',path)
        path = '《=》'.join(points)
        return path



    def devToKnowledge(self,all_dev,now,area):
        '''
        将箱体清单和上联方案表转换为Dify知识库格式的Markdown文档
        '''
        all_dev = all_dev[['设施名称','所属区县','所属镇街','经度','纬度','容量']]
        all_dev = all_dev.reset_index(drop=True)
        all_dev = all_dev.fillna('').astype(str)
        all_dev['详细信息'] = (
            '设施名称:' + all_dev['设施名称'] + ' ' +
            all_dev['所属区县'] + ' ' +
            all_dev['所属镇街'] + ' ' +
            '容量:' + all_dev['容量']
        )
        all_dev = all_dev[['设施名称','详细信息']]
        all_dev = all_dev.drop_duplicates()
        flag,result = dfToMarkdownKnowledge(all_dev,self.output_dir+'/箱体清单_'+area+'_'+now+'.md')
        if flag:
            self.state_signal.emit(result)
        else:
            self.error_signal.emit(result)


    def loadOltHouseCount(self):
        '''
        读取OLT网元数据集，统计每个OLT机房的情况
        '''
        df = readDataBase('OLT网元数据集')
        df_model_count = df.groupby(['所属机房', '设备型号']).size().reset_index(name='设备台数')
        # 把每个机房下的【型号: 台数】拼成字符串
        model_str = df_model_count.groupby('所属机房').apply(
            lambda x: '、'.join([f"{row['设备型号']}({row['设备台数']}台)" for _, row in x.iterrows()])
        ).reset_index(name='设备型号统计')
        # 2. 按机房汇总所有端口总数
        df_port = df.groupby('所属机房').agg(
            PON口总数汇总=('PON口总数', 'sum'),
            PON口空闲数汇总=('PON口空闲数', 'sum'),
            XGPON口总数汇总=('XGPON口总数', 'sum'),
            XGPON口空闲数汇总=('XGPON口空闲数', 'sum')
        ).reset_index()
        # 3. 合并统计结果
        result_df = pd.merge(model_str, df_port, on='所属机房')

        # 4. 拼接成【详细信息】列
        result_df['机房详细信息'] = (
            '设备情况：' + result_df['设备型号统计'] +
            ' | PON口数：' + result_df['PON口总数汇总'].astype(int).astype(str) +
            ' | PON口空闲数：' + result_df['PON口空闲数汇总'].astype(int).astype(str) +
            ' | XGPON口数：' + result_df['XGPON口总数汇总'].astype(int).astype(str) +
            ' | XGPON口空闲数：' + result_df['XGPON口空闲数汇总'].astype(int).astype(str)
        )
        # 5. 最终只保留 2 列
        house_df = result_df[['所属机房', '机房详细信息']].drop_duplicates().rename(columns={'所属机房':'目标OLT机房'})
        return house_df

    def getAllDev(self,all_dev):
        # 只提取72个PON口以上的箱体和已开主光路的箱体
        pon_line = readDataBase('主光路')[['OBD所属对象']].drop_duplicates().rename(columns={'OBD所属对象':'设施名称'})
        pon_line = pd.merge(all_dev,pon_line,on='设施名称')
        all_dev = all_dev[all_dev['容量']>=72]
        all_dev = pd.concat([all_dev,pon_line],ignore_index=True)
        all_dev = all_dev.drop_duplicates()
        return all_dev

    def getDevUplink(self,all_dev):
        # 读取箱体上联OLT跳纤路径表
        uplink_df = readDataBase('箱体上联OLT跳纤路径表')
        temp_df = all_dev[['设施名称']].copy().drop_duplicates()
        uplink_df = uplink_df[uplink_df['目标OLT机房']!='']
        uplink_df = uplink_df.groupby(['设施名称','目标OLT机房']).first().reset_index()
        uplink_df = uplink_df.merge(temp_df,on='设施名称')
        uplink_df = uplink_df.drop_duplicates()
        house_df = self.loadOltHouseCount()
        uplink_df = uplink_df.merge(house_df,on='目标OLT机房')
        uplink_df = uplink_df.drop_duplicates()
        temp_df = uplink_df[['设施名称']].copy().drop_duplicates()
        all_dev = all_dev.merge(temp_df,on='设施名称')
        all_dev = all_dev.drop_duplicates()
        return all_dev,uplink_df

    def tableNotRequired(self):
        '''
        校验数据库表格是否存在满足，一次返回不满足的表格清单
        '''
        check_tales = ['分纤箱','光交箱','ODF','箱体上联OLT跳纤路径表','OLT网元数据集']
        conn = sqlite3.connect('data/TransportNetwork.db')
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]
        not_required_tables = [table for table in check_tales if table not in tables]
        return not_required_tables


'''
调用数据库data\transportNetwork.db中的'机房','光交箱', '分纤箱', 'ODF'表格，按类型生成箱体图层，分区域输出文件；
数据库表格数据结构：
所属站点(TEXT), 机房类型(TEXT), 机房名称(TEXT), 业务级别(TEXT), 生命周期状态(TEXT)
(['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
(['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
(['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
处理过程：
1、ODF表格 取 机房名称、所属区县、经度、纬度 四列去重，形成机房清单，设置类型为机房
2、光交箱表格 取 设施名称、所属区县、经度、纬度、分纤点级别 五列去重，形成光交箱清单，设置类型为分纤点级别-光交箱
3、分纤箱表格 取 设施名称、所属区县、经度、纬度、容量 五列去重，筛选容量大于等于72的箱体，形成分纤箱清单，设置类型为分纤箱
合并三个清单，根据类型分文件夹，按所属区县逐个输出文件；调用PublicFunc.py中的writeDoc\writeFolder\writePoint函数，生成KML文件；不同类型的icon不同；
'''