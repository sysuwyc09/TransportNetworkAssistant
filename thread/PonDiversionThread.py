# OLT PON端口分流自动分析

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
import os
from .publicFunc import *
import time

class PonDiversionThread(QThread):
    state_signal = Signal(str)

    def __init__(self, olt_names):
        super().__init__()
        self.olt_names = olt_names
    
    def run(self):
        try:
            self.state_signal.emit('正在初始化分析...')
            
            olt_df = pd.DataFrame({'OLT名称': self.olt_names})
            self.state_signal.emit(f'获取到{len(olt_df)}个OLT网元')
            
            self.state_signal.emit('正在读取主光路数据...')
            pon_df = readDataBase('主光路')
            src_df = pon_df.merge(olt_df, on='OLT名称', how='inner')
            self.state_signal.emit(f'匹配到{len(src_df)}条主光路')
            
            if len(src_df) == 0:
                self.state_signal.emit('未匹配到任何主光路数据')
                return
            
            self.state_signal.emit('正在读取箱体上联OLT跳纤路径表...')
            box_up_df = readDataBase('箱体上联OLT跳纤路径表')
            obj_df = src_df.merge(box_up_df, left_on='OBD所属对象', right_on='设施名称', how='left')
            self.state_signal.emit(f'获取到{len(obj_df)}条跳纤路径信息')
            
            self.state_signal.emit('正在读取OLT网元信息...')
            olt_net_df = readDataBase('OLT网元')[['网元名称', '所属机房']].rename(columns={'网元名称': 'OLT名称', '所属机房': '原OLT机房'})
            obj_df = obj_df.merge(olt_net_df, on='OLT名称', how='inner')
            
            obj_df = obj_df[obj_df['原OLT机房'] != obj_df['目标OLT机房']]
            self.state_signal.emit(f'筛选出{len(obj_df)}条跨机房主光路')
            
            if len(obj_df) == 0:
                self.state_signal.emit('没有需要分析的跨机房主光路')
                return
            
            obj_df = self.analyze_pon_diversion(obj_df)
            
            if len(obj_df) == 0:
                self.state_signal.emit('没有可行的分流方案')
                return
            
            result_df = src_df.merge(obj_df[['PON口', '目标OLT机房','调整路径', '调整后光衰', '割接点', '割接路由', '割接可用芯数']], on='PON口', how='left')
            
            result_df = result_df.sort_values(by=['OLT名称', 'PON口'])
            
            os.makedirs('结果', exist_ok=True)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'结果/PON分流分析结果{timestamp}.xlsx'
            result_df.to_excel(output_file, index=False)
            self.state_signal.emit(f'分析完成，文件已保存至: {output_file}')

        except Exception as e:
            self.state_signal.emit(f'分析失败: {str(e)}')
    
    def analyze_pon_diversion(self, obj_df):
        obj_df['光路文本路由'] = obj_df['光路文本路由'].astype(str)
        obj_df['跳数'] = obj_df['光路文本路由'].apply(findJumpNum)
        obj_df['光路长度'] = obj_df['光路长度'].astype(float)
        obj_df['调整前光衰'] = obj_df['跳数'] * 1 + obj_df['光路长度'] / 1000 * 0.35
        
        obj_df = obj_df.rename(columns={'光衰预算': '调整后光衰', '跳纤路径': '调整路径'})
        
        box_df = readDataBase('光交箱')[['设施名称', '机房名称']]
        oBox_df = readDataBase('分纤箱')[['设施名称', '机房名称']]
        odf_df = readDataBase('ODF')[['设施名称', '机房名称']]
        all_site_df = pd.concat([box_df, oBox_df, odf_df], axis=0)
        all_site_df = all_site_df.ffill(axis=1)
        site_dict = all_site_df.set_index('设施名称')['机房名称'].to_dict()

        
        obj_df = obj_df.reset_index(drop=True)
        findKeyPointVec = np.vectorize(findKeyPoint, excluded=['site_dict'])
        obj_df['割接点'], obj_df['割接路由'], obj_df['割接可用芯数'] = findKeyPointVec(
            obj_df['光路文本路由'], obj_df['调整路径'], site_dict=site_dict
        )
        
        obj_df = obj_df[obj_df['割接可用芯数'] > 0]
        
        if len(obj_df) == 0:
            return obj_df
        
        obj_df = obj_df.sort_values(by=['PON口', '调整后光衰'])
        obj_df = obj_df.drop_duplicates(subset=['PON口'], keep='first')
        
        return obj_df
