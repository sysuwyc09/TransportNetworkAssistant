'''
临界弱光+弱光，主光路调优分析
1、分析弱光+临界弱光ONU的清单，分析主光路可调优数量
2、根据分析结果，生成主光路调优建议
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class WeekOnuPortAnalyzeThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        self.state_signal.emit('正在加载弱光ONU清单清单...')
        week_onu_df = pd.read_excel(self.file_path,engine='openpyxl')
        self.state_signal.emit('正在分析弱光清单U')

        week_onu_df,week_port_table = self.analyzeWeekPort(week_onu_df)

        self.state_signal.emit('正在分析弱光清单U的可优化主光路清单,分析结构主光路问题')
        week_port_table,long_pon_up_link,adjust_port_df,dev_df = self.analyzeLongPonLine(week_port_table)


        self.state_signal.emit('正在生成分析结果。')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        out_file_path = '结果/'+self.file_path.split('/')[-1].split('.')[0]+'_分析结果'+dt+'.xlsx'

        with pd.ExcelWriter(out_file_path) as writer:
            week_onu_df.to_excel(writer,sheet_name='弱光ONU清单',index=False)
            week_port_table.to_excel(writer,sheet_name='弱光PON口清单',index=False)
            long_pon_up_link.to_excel(writer,sheet_name='超长主光路可调优方案',index=False)
            adjust_port_df.to_excel(writer,sheet_name='超长待调整结构的清单',index=False)
            dev_df.to_excel(writer,sheet_name='弱光聚合情况',index=False)
        self.state_signal.emit('分析完成')

    def analyzeWeekPort(self,week_onu_df):
        '''
        分析弱光清单U的弱光类型
        '''
        week_onu_df['接收光功率(dBm)'] = pd.to_numeric(week_onu_df['接收光功率(dBm)'],errors='coerce')
        week_onu_df['弱光类型'] = week_onu_df['接收光功率(dBm)'].apply(lambda x: '弱光' if x <= -27 else ('临界弱光' if x <= -25 else '正常'))
        week_onu_df['弱光类型'] = week_onu_df['弱光类型'].fillna('正常') 
        anaylyzeArea_vec = np.vectorize(self.anaylyzeArea)
        week_onu_df['区域'] = anaylyzeArea_vec(week_onu_df['区域'],week_onu_df['PON'])
        week_port_table = pd.pivot_table(week_onu_df,index=['PON'],columns=['弱光类型'],aggfunc='size',fill_value=0)
        week_port_table = week_port_table.reset_index()
        week_port_table = week_port_table.rename(columns={'弱光':'弱光ONU数','临界弱光':'临界弱光ONU数'})
        week_port_table['待整治数'] = week_port_table['弱光ONU数'] + week_port_table['临界弱光ONU数']
        port_area = week_onu_df[['PON','区域','网格']].drop_duplicates(subset=['PON'],keep='first')
        week_port_table = week_port_table.merge(port_area,on='PON',how='left')
        return week_onu_df,week_port_table

    def anaylyzeArea(self,company,olt_name):
        if pd.isnull(company):
            company = fixCompany(olt_name)
        elif company == '':
            company = fixCompany(olt_name)    
        return company

    def analyzeLongPonLine(self,week_port_table):
        # 分析可调优清单
        long_pon_port = readDataBase('超长主光路清单')
        long_pon_port['PON'] = long_pon_port['PON口'].apply(self.fixLongPonPort)

        temp_df = long_pon_port[['PON','PON口']].copy()
        temp_df['是否超长主光路'] = '是'
        week_port_table = week_port_table.merge(temp_df,on='PON',how='left')
        week_port_table['是否超长主光路'] = week_port_table['是否超长主光路'].fillna('否')

        long_pon_up_link = readDataBase('超长主光路调优方案')
        long_pon_up_link = long_pon_up_link[long_pon_up_link['割接可用芯数']>0]
        long_pon_up_link = long_pon_up_link.merge(week_port_table,on='PON口')


        temp_df = long_pon_up_link[['PON口']].copy()
        temp_df['是否可主光路调整'] = '是'
        week_port_table = week_port_table.merge(temp_df,on='PON口',how='left')
        week_port_table['是否可主光路调整'] = week_port_table['是否可主光路调整'].fillna('否')

        # 分析待调整结构的清单
        adjust_port_df = week_port_table[week_port_table['是否可主光路调整']=='否'].merge(long_pon_port,on=['PON','PON口'])
        all_dev_df = readDevsWithCoord()[['设施名称','经度','纬度']]
        all_dev_df.rename(columns={'设施名称':'OBD所属对象'},inplace=True)
        adjust_port_df = adjust_port_df.merge(all_dev_df,on='OBD所属对象',how='left')

        # 分析弱光聚合情况
        dfs = adjust_port_df['光路文本路由'].apply(self.fixPathPoint)
        pon_path_df = pd.concat(dfs.tolist(),ignore_index=True)
        pon_path_df = pon_path_df.drop_duplicates()
        dev_df = pd.pivot_table(pon_path_df,index='光交设施',aggfunc={'光路文本路由':'count'},fill_value=0)
        dev_df = dev_df.reset_index()
        dev_df.columns = ['光交设施','光路数']
        adjust_port_unique = adjust_port_df[['光路文本路由','PON口']].drop_duplicates(subset=['光路文本路由'], keep='first')
        pon_path_df = pon_path_df.merge(adjust_port_unique,on='光路文本路由',how='left')
        temp_df = pon_path_df[['光交设施','PON口']]
        temp_grp = temp_df.groupby('光交设施').agg('、'.join)
        temp_grp = temp_grp.reset_index().rename(columns={'PON口':'弱光PON口清单'})
        dev_df = dev_df.merge(temp_grp,on='光交设施',how='left')
        dev_df.sort_values(by='光路数',ascending=False,inplace=True)

        return week_port_table,long_pon_up_link,adjust_port_df,dev_df

    def fixLongPonPort(self,pon_port):
        parts = pon_port.split('-')
        olt_name = '-'.join(parts[:-5])
        return olt_name + '-' + parts[-5] + '/' + parts[-4] + '/' + parts[-2]

    def fixPathPoint(self,pon_path):
        sites = re.findall('>(.*?)\([AB正反/面ODM0-9]+-\d+-\d+',pon_path)
        items = []
        # 倒序查询割接路径上的割接点,排除空字符串和NA值
        for site in sites:
            if site not in items:
                items.append(site)
        items = items[1:]
        df = pd.DataFrame(items,columns=['光交设施'])
        df['光路文本路由'] = pon_path
        return df


# 分析零利用率的光缆段