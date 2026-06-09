'''
通报弱光清单分析
1、分析C+光模块替换分析
2、分析可优化主光路清单,选取不能替换的光模块PON口
3、弱光ODB经纬度匹配,全量匹配
4、展开弱光匹配
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class PonPortReplaceThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,folder_path=''):
        super().__init__(parent)
        self.folder_path = folder_path

    def run(self):
        self.state_signal.emit('正在加载弱光ONU清单和光模块清单...')
        week_onu_file = ''
        hw_port_file = ''
        zte_port_file = ''
        for file in os.listdir(self.folder_path):
            if '弱光与边缘' in file and '$' not in file and '.xlsx' in file:
                week_onu_file = self.folder_path + '/' + file
            elif '华为光模块' in file and '$' not in file and '.xlsx' in file:
                hw_port_file = self.folder_path + '/' + file
            elif '中兴光模块' in file and '$' not in file and '.xlsx' in file:
                zte_port_file = self.folder_path + '/' + file

        if week_onu_file == '' or hw_port_file == '' or zte_port_file == '':
            self.error_signal.emit('未找到弱光ONU清单、华为光模块清单或中兴光模块清单')
            return;
        self.state_signal.emit('正在读取弱光ONU清单')
        week_onu_df = pd.read_excel(week_onu_file,engine='openpyxl')
        self.state_signal.emit('正在读取华为光模块清单')
        hw_port_df = pd.read_excel(hw_port_file,engine='openpyxl')
        self.state_signal.emit('正在读取中兴光模块清单')
        zte_port_df = pd.read_excel(zte_port_file,engine='openpyxl')  
        self.state_signal.emit('正在分析弱光清单U')
        hw_port_df = hw_port_df[['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)','PON口光模块类型']]
        zte_port_df = zte_port_df[['网元名称','机框','槽位','端口','等级(类型/子类型)','发送光功率(dBm)','业务类型']]
        hw_port_df['资源名称'] = hw_port_df['资源名称'].astype('str')
        hw_port_df['机框'],hw_port_df['槽位'],hw_port_df['端口'] = zip(*hw_port_df['资源名称'].apply(self.fixHwPort))
        hw_port_df = hw_port_df.rename(columns={'PON口光模块类型':'PON口类型'})
        zte_port_df = zte_port_df.rename(columns={'等级(类型/子类型)':'PON口光模块子类型','发送光功率(dBm)':'PON口发送光功率 (dBm)','业务类型':'PON口类型'})
        hw_port_df.drop(columns=['资源名称'],inplace=True)
        port_df = pd.concat([hw_port_df,zte_port_df],ignore_index=True)
        port_df = port_df.astype('str')
        port_df['PON'] = port_df['网元名称'] + '-' + port_df['机框'] + '/' + port_df['槽位'] + '/' + port_df['端口']
        port_df = port_df.groupby(['PON']).first().reset_index(drop=False)
        week_onu_df = pd.merge(week_onu_df,port_df,on='PON',how='left')
        self.state_signal.emit('正在分析弱光清单U的光模块替换分析')
        week_onu_df,week_port_table = self.analyzePonModel(week_onu_df)
        self.state_signal.emit('正在分析弱光清单U的可优化主光路清单,分析结构主光路问题')
        opt_port_df,long_pon_up_link,adjust_port_df,dev_df = self.analyzeLongPonLine(week_port_table)

        self.state_signal.emit('正在生成弱光清单光模块信息。')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with pd.ExcelWriter(f'结果/弱光清单光模块信息{dt}.xlsx') as writer:
            week_onu_df.to_excel(writer,sheet_name='弱光ONU清单',index=False)
            week_port_table.to_excel(writer,sheet_name='弱光PON口替换光模块分析过程',index=False)
            opt_port_df.to_excel(writer,sheet_name='可光模块替代的端口清单',index=False)
            long_pon_up_link.to_excel(writer,sheet_name='超长主光路调优方案',index=False)
            adjust_port_df.to_excel(writer,sheet_name='待调整结构的清单',index=False)
            dev_df.to_excel(writer,sheet_name='弱光聚合情况',index=False)
        self.state_signal.emit('分析完成')

    def analyzeLongPonLine(self,week_port_table):
        # 筛选可光模块替代的端口清单
        opt_port_df = week_port_table[week_port_table['替换光模块类型']!='--']

        # 分析可调优清单
        not_opt_port_df = week_port_table[week_port_table['替换光模块类型']=='--']
        long_pon_port = readDataBase('超长主光路清单')
        long_pon_port['PON'] = long_pon_port['PON口'].apply(self.fixLongPonPort)

        long_pon_port = long_pon_port.merge(not_opt_port_df,on='PON')

        long_pon_up_link = readDataBase('超长主光路调优方案')
        long_pon_up_link = long_pon_up_link[long_pon_up_link['割接可用芯数']>0]
        temp_df = long_pon_port[['区域','网格','PON口类型','PON','PON口','弱光ONU数','预估替换光模块可整治数','PON口光模块子类型','PON口发送光功率 (dBm)','替换光模块类型']]

        long_pon_up_link = long_pon_up_link.merge(temp_df,on='PON口')
        temp_df = long_pon_up_link[['PON']].copy()
        temp_df['是否可主光路调整'] = '是'

        long_pon_port = long_pon_port.merge(temp_df,on='PON',how='left')
        long_pon_port['是否可主光路调整'] = long_pon_port['是否可主光路调整'].fillna('否')

        # 分析待调整结构的清单
        adjust_port_df = long_pon_port[long_pon_port['是否可主光路调整']=='否']
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

        return opt_port_df,long_pon_up_link,adjust_port_df,dev_df

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


    def analyzePonModel(self,week_onu_df):
        '''
        分析更换光模块可解决的弱光PON口
        '''
        isOnuGoodm_vec = np.vectorize(self.isOnuDBmGood)
        week_onu_df['PON口发送光功率 (dBm)'] = pd.to_numeric(week_onu_df['PON口发送光功率 (dBm)'],errors='coerce')
        week_onu_df['接收光功率(dBm)'] = pd.to_numeric(week_onu_df['接收光功率(dBm)'],errors='coerce')
        week_onu_df['预估替换光模块可整治'] = isOnuGoodm_vec(week_onu_df['接收光功率(dBm)'],week_onu_df['PON口发送光功率 (dBm)'],week_onu_df['PON口类型'],week_onu_df['PON口光模块子类型'])
        week_port_table = pd.pivot_table(week_onu_df,index=['PON'],columns=['预估替换光模块可整治'],aggfunc={'区域':'count'},fill_value=0)
        week_port_table.columns = week_port_table.columns.droplevel(0)
        week_port_table = week_port_table.reset_index()
        week_port_table['弱光ONU数'] = week_port_table['是'] + week_port_table['否']
        week_port_table.rename(columns={'是':'预估替换光模块可整治数'},inplace=True)
        week_port_table = week_port_table[['PON','弱光ONU数','预估替换光模块可整治数']]
        temp_df = week_onu_df[['区域','网格','PON','PON口类型','PON口光模块子类型','PON口发送光功率 (dBm)']].copy()
        temp_df = temp_df.drop_duplicates(subset=['PON'],keep='first')
        week_port_table = pd.merge(week_port_table,temp_df,on='PON',how='left')
        install_opt_model_vec = np.vectorize(self.installOptModel)
        week_port_table['替换光模块类型'] = install_opt_model_vec(week_port_table['预估替换光模块可整治数'],week_port_table['PON口类型'])
        
        return week_onu_df,week_port_table

    def installOptModel(self,onu_num,port_type):
        '''
        判断更换光模块的类型
        '''
        if onu_num > 0:
            if port_type == 'GPON':
                return 'Class C++'
            else:
                return 'Class D'
        return '--'

    def isOnuDBmGood(self,onu_dbm,port_dbm,port_type,opt_type):
        '''
        判断弱光ONU收光是否可以通过更换光模块解决
        '''
        if port_type == '10GGPON' or port_type == 'XGPON+GPON' or port_type == 'XGSPON':
            if opt_type == 'CLASS C+' or opt_type == 'N2a' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7.8 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        if port_type == 'GPON':
            if opt_type == 'CLASS C+' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        return '否'


    def fixHwPort(self,port_name):
        regex = r'框:(\d+)/槽:(\d+)/端口:(\d+)'
        match = re.match(regex,port_name)
        if match:
            box = match.group(1)
            slot = match.group(2)
            port = match.group(3)
            return box,slot,port
        else:
            return '-','-','-'

'''
临界弱光+弱光，主光路调优分析
1、分析弱光+临界弱光ONU的清单，分析主光路可调优数量
2、根据分析结果，生成主光路调优建议
'''