# 分析ONU弱光的线程

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class FindWeakONUThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,folder_path=''):
        super().__init__(parent)
        self.folder_path = folder_path
    
    def run(self):
        try:
            onus,ports = self.loadData()
            if not onus or not ports:
                self.state_signal.emit('未加载到ONU或光模块的数据')
                return
            onu_df = pd.concat(onus,axis=0)
            port_df = pd.concat(ports,axis=0)
            # conn = sqlite3.connect('data/onu.db')
            # port_df.to_sql('pon_port',conn,if_exists='replace',index=False)
            # onu_df.to_sql('onu',conn,if_exists='replace',index=False)
            # port_df = pd.read_sql('select * from pon_port',conn)
            # onu_df = pd.read_sql('select * from onu',conn)
            # conn.close()
            port_df['匹配项'] = port_df['网元名称'] + ' ' + port_df['槽位'] + '槽' + port_df['端口'] + '口'
            onu_df['匹配项'] = onu_df['网元名称'] + ' ' + onu_df['槽位'] + '槽' + onu_df['端口'] + '口'
            self.state_signal.emit(f'共{onu_df.shape[0]}条ONU数据,正在分析ONU收光情况...')
            onu_df['ONU收光情况'] = onu_df['接收光功率(dBm)'].apply(self.onuType)
            onu_table = pd.pivot_table(onu_df,index='匹配项',columns=['ONU收光情况'],aggfunc={'网元名称':'count'},fill_value=0)
            onu_table.columns = onu_table.columns.droplevel(0)
            onu_table['有光ONU数'] = 0
            for col in onu_table.columns:
                if col != '有光ONU数' and col != '未知':
                    onu_table['有光ONU数'] += onu_table[col]
            onu_table = onu_table.reset_index()
            if '<-28.5dBm' in onu_table.columns:
                if '-28.5dBm~-27dBm' in onu_table.columns:
                    onu_table['弱光ONU数'] = onu_table['<-28.5dBm'] + onu_table['-28.5dBm~-27dBm']
                else:
                    onu_table['弱光ONU数'] = onu_table['<-28.5dBm']
            else:
                if '-28.5dBm~-27dBm' in onu_table.columns:
                    onu_table['弱光ONU数'] = onu_table['-28.5dBm~-27dBm']
                else:
                    onu_table['弱光ONU数'] = 0
            if '-27dBm~-25dBm' in onu_table.columns:
                onu_table['临界弱光ONU数'] = onu_table['-27dBm~-25dBm']
            else:
                onu_table['临界弱光ONU数'] = 0
            onu_table['弱光ONU整治数'] = onu_table['弱光ONU数'] + onu_table['临界弱光ONU数']
            onu_table['整治ONU比例%'] = round(onu_table['弱光ONU整治数']/onu_table['有光ONU数']*100,2)
            port_df = port_df.merge(onu_table,on='匹配项',how='left')
            # 匹配主光路
            pon_df = readDataBase('主光路')
            pon_df['光路文本路由'] = pon_df['光路文本路由'].astype(str)
            pon_df['跳数'] = pon_df['光路文本路由'].apply(findJumpNum)
            pon_df['光路长度'] = pd.to_numeric(pon_df['光路长度'], errors='coerce')
            pon_df['光路长度'] = round(pon_df['光路长度']/1000,2)
            pon_df['光衰'] = pon_df['跳数'] * 1 + pon_df['光路长度'] * 0.35
            pon_df['槽位'],pon_df['端口'] = zip(*pon_df['PON口'].apply(fixSrcPoNPort))
            pon_df['匹配项'] = pon_df['OLT名称'] + ' ' + pon_df['槽位'] + '槽' + pon_df['端口'] + '口'
            pon_df = pon_df[['匹配项','PON口','PON下挂ONU数量','OBD所属对象','光路名称','光路长度','光路文本路由','跳数','光衰']]
            port_df = port_df.merge(pon_df,on='匹配项',how='left')
            port_df['一级OBD前收光预算'] = port_df['PON口发送光功率 (dBm)'] - port_df['光衰']
            # 匹配超长主光路调优方案
            long_pon_df = readDataBase('超长主光路调优方案')
            long_pon_df = long_pon_df[['PON口','目标OLT机房','调整后距离','调整后跳数','调整后光衰','调整路径','优化光衰','割接点','割接路由','割接可用芯数']]
            port_df = port_df.merge(long_pon_df,on='PON口',how='left')

            # PON口光模块更换范围,发光光功率<5.5dBm，弱光ONU数>0，整治ONU数>=3，目标OLT机房为空或 目标机房不为空且割接可用芯数=0;-28.5dBm~-27dBm >0
            opitcal_model_df = port_df[(port_df['PON口发送光功率 (dBm)']<5.5) & (port_df['弱光ONU数']>0) & (port_df['-28.5dBm~-27dBm']>0) & (port_df['弱光ONU整治数']>=3) & (port_df['整治ONU比例%']>0) & ((port_df['目标OLT机房'].isnull()) | (port_df['割接可用芯数']==0))].copy()
            opitcal_model_df = opitcal_model_df.sort_values(by=['弱光ONU整治数'],ascending=[False])
            # opitcal_model_df = opitcal_model_df.drop(['目标OLT机房','调整后距离','调整后跳数','调整后光衰','调整路径','优化光衰','割接点','割接路由','割接可用芯数'],axis=1)

            # 主光路调优范围；优化光衰>=2dBm，ONU整治数>=3, 割接可用芯数>0
            adjust_pon_df = port_df[(port_df['优化光衰']>=2) & (port_df['弱光ONU整治数']>=3) & (port_df['割接可用芯数']>0)].copy()
            adjust_pon_df = adjust_pon_df.sort_values(by=['弱光ONU整治数'],ascending=[False])

            # 现场测试范围：弱光ONU整治数占比≥80%，且一级OBD前预算出光≥0dBm,弱光ONU整治数>=3
            test_pon_df = port_df[(port_df['整治ONU比例%']>=80) & (port_df['一级OBD前收光预算']>=0) & (port_df['弱光ONU整治数']>=3) & (port_df['PON口发送光功率 (dBm)']) ].copy()
            test_pon_df = test_pon_df.sort_values(by=['弱光ONU整治数'],ascending=[False])

            # 聚类弱光OBD所属对象分析；光衰≥6dBm，且调整后光衰为空或者调整后光衰≥6dBm
            cluster_pon_df = port_df[(port_df['光衰']>=6) & ((port_df['调整后光衰'].isnull()) | (port_df['调整后光衰']>=6))].copy()
            cluster_table = pd.pivot_table(cluster_pon_df,index='OBD所属对象',aggfunc={'PON口':'count','弱光ONU整治数':'sum'})
            cluster_table = cluster_table.reset_index().rename(columns={'PON口':'PON口数','弱光ONU整治数':'聚类弱光ONU整治数'})
            cluster_pon_df = cluster_pon_df.merge(cluster_table,on='OBD所属对象',how='left')
            cluster_pon_df = cluster_pon_df.sort_values(by=['PON口数','聚类弱光ONU整治数'],ascending=[False,False])


            self.state_signal.emit('分析完成，正在生成数据表格。')
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with pd.ExcelWriter(os.path.join(self.folder_path,f'ONU弱光分析结果{dt}.xlsx')) as writer:
                port_df.to_excel(writer,sheet_name='PON口详细清单',index=False)
                opitcal_model_df.to_excel(writer,sheet_name='PON口光模块更换清单',index=False)
                adjust_pon_df.to_excel(writer,sheet_name='主光路调优清单',index=False)
                test_pon_df.to_excel(writer,sheet_name='现场测试清单',index=False)
                cluster_pon_df.to_excel(writer,sheet_name='聚类弱光OBD所属对象分析',index=False)
            self.state_signal.emit('已完成...')
        except Exception as e:
            self.state_signal.emit('分析ONU弱光失败:' + str(e))
            
    def loadData(self):
        onus = []
        ports = []
        # 华为ONU ：网元名称 槽号 端口号 接收光功率(dBm)
        # 中兴ONU：网元名称 槽位 端口 接收光功率(dBm)
        # 华为光模块：网元名称	资源名称 PON口光模块子类型 PON口发送光功率 (dBm)；资源名称 框:0/槽:1/端口:0
        # 中兴光模块：网元名称 槽位 端口 发送光功率(dBm) 等级(类型/子类型)
        files = os.listdir(self.folder_path)
        for file in files:
            if '华为ONU' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽号','端口号','接收光功率(dBm)'])
                df = df[['网元名称','槽号','端口号','接收光功率(dBm)']].rename(columns={'槽号':'槽位','端口号':'端口'})
                df = df.astype({'槽位':str,'端口':str})
                df['接收光功率(dBm)'] = pd.to_numeric(df['接收光功率(dBm)'],errors='coerce')
                onus.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '中兴ONU' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽位','端口','接收光功率(dBm)'])
                df = df[['网元名称','槽位','端口','接收光功率(dBm)']]
                df = df.astype({'槽位':str,'端口':str})
                df['接收光功率(dBm)'] = pd.to_numeric(df['接收光功率(dBm)'],errors='coerce')
                onus.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '华为光模块' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)'])
                df = df[['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)']].rename(columns={'PON口光模块子类型':'PON口光模块类型'})
                df['槽位'],df['端口'] = zip(*df['资源名称'].apply(self.fixHwPort))
                df = df[['网元名称','槽位','端口','PON口光模块类型','PON口发送光功率 (dBm)']]
                df['PON口发送光功率 (dBm)'] = pd.to_numeric(df['PON口发送光功率 (dBm)'],errors='coerce')
                ports.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '中兴光模块' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽位','端口','发送光功率(dBm)','等级(类型/子类型)','光模块号/通道号'])
                df = df[['网元名称','槽位','端口','发送光功率(dBm)','等级(类型/子类型)','光模块号/通道号']].rename(columns={'发送光功率(dBm)':'PON口发送光功率 (dBm)','等级(类型/子类型)':'PON口光模块类型'})
                df['光模块号/通道号'] = df['光模块号/通道号'].astype(str)
                df = df[df['光模块号/通道号'] != '1']
                df = df[df['光模块号/通道号'] != '2']

                df = df[['网元名称','槽位','端口','PON口光模块类型','PON口发送光功率 (dBm)']]
                df = df.astype({'槽位':str,'端口':str})
                df['PON口发送光功率 (dBm)'] = pd.to_numeric(df['PON口发送光功率 (dBm)'],errors='coerce')
                ports.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
        return onus,ports
 
    def fixHwPort(self,port_name):
        regex = r'槽:(\d+)/端口:(\d+)'
        match = re.search(regex,port_name)
        if match:
            slot = match.group(1)
            port = match.group(2)
            return slot,port
        else:
            return '-','-'

    def onuType(self,onu_dbm):
        if pd.isnull(onu_dbm):
            return '未知'
        else:
            if onu_dbm >= -21:
                return '≥-21dBm'
            elif onu_dbm >= -25:
                return '-25dBm~-21dBm'
            elif onu_dbm >= -27:
                return '-27dBm~-25dBm'
            elif onu_dbm >= -28.5:
                return '-28.5dBm~-27dBm'
            else:
                return '<-28.5dBm'


# 单点A-B跳纤方案线程