# 超长主光路调优分析

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class FindLongPonLineThread(QThread):
    state_signal = Signal(str,float,str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
    
    def run(self):
        try:
            self.state_signal.emit('正在分析超长主光路清单...',0,'')
            pon_df = readDataBase('主光路')
            pon_num = pon_df.shape[0]
            self.state_signal.emit(f'存量共有{pon_num}条主光路，按1跳1dB、1公里0.35dB估算超长主光路（超6dB）',0,'')
            pon_df['光路文本路由'] = pon_df['光路文本路由'].astype(str)
            pon_df['跳数'] = pon_df['光路文本路由'].apply(findJumpNum)
            pon_df['光路长度'] = pon_df['光路长度'].astype(float)
            pon_df['光衰'] = pon_df['跳数'] * 1 + pon_df['光路长度'] / 1000 * 0.35
            lon_pon_df = pon_df[pon_df['光衰'] >= 6]
            self.state_signal.emit(f'按1跳1dB、1公里0.35dB估算，共有{lon_pon_df.shape[0]}条主光路超6dB',10,'')
            lon_pon_df.sort_values(by=['光衰'],ascending=False,inplace=True)
            writeDataBase('超长主光路清单',lon_pon_df)
            
            box_up_df = readDataBase('箱体上联OLT跳纤路径表')
            box_up_df = box_up_df[['设施名称','目标OLT机房','跳纤距离','跳数','光衰预算','跳纤路径']].rename(
                columns={'设施名称':'OBD所属对象','跳纤距离':'调整后距离','跳数':'调整后跳数','光衰预算':'调整后光衰','跳纤路径':'调整路径'})
            box_up_df = box_up_df.sort_values(by=['OBD所属对象','调整后光衰'],ascending=[True,True])
            box_up_df = box_up_df.drop_duplicates(subset=['OBD所属对象'],keep='first')
            
            lon_pon_df = lon_pon_df.merge(box_up_df,on='OBD所属对象',how='left')
            lon_pon_df['调整后光衰'] = lon_pon_df['调整后光衰'].fillna(999)
            lon_pon_df['优化光衰'] = lon_pon_df['光衰'] - lon_pon_df['调整后光衰']
            # 筛选出优化光衰大于等于1dB的主光路
            lon_pon_df = lon_pon_df[lon_pon_df['优化光衰'] >= 1]
            self.state_signal.emit(f'主光路能调优1dB，共有{lon_pon_df.shape[0]}条主光路',30,'')
            # 筛选割接点及割接可行纤芯
            box_df = readDataBase('光交箱')[['设施名称','机房名称']]
            oBox_df = readDataBase('分纤箱')[['设施名称','机房名称']]
            odf_df = readDataBase('ODF')[['设施名称','机房名称']]
            all_site_df = pd.concat([box_df,oBox_df,odf_df],axis=0)
            all_site_df = all_site_df.ffill(axis=1)
            site_dict = all_site_df.set_index('设施名称')['机房名称'].to_dict()
            findKeyPointVec = np.vectorize(findKeyPoint,excluded=['site_dict'])
            lon_pon_df = lon_pon_df.reset_index(drop=True)
            # print(findKeyPoint(lon_pon_df.iloc[0]['光路文本路由'],lon_pon_df.iloc[0]['调整路径'],site_dict=site_dict))
            lon_pon_df['割接点'],lon_pon_df['割接路由'],lon_pon_df['割接可用芯数'] = findKeyPointVec(lon_pon_df['光路文本路由'],lon_pon_df['调整路径'],site_dict=site_dict)
            
            # 剔除割接点，原机房，目标OLT机房 三者同时相同的主光路
            olt_df = readDataBase('OLT网元')[['网元名称','所属机房']].rename(columns={'网元名称':'OLT名称','所属机房':'原机房'})
            lon_pon_df = lon_pon_df.merge(olt_df,on='OLT名称',how='left')
            lon_pon_df = lon_pon_df[(lon_pon_df['割接点'] != lon_pon_df['原机房']) | (lon_pon_df['割接点'] != lon_pon_df['目标OLT机房'])]
            lon_pon_df = lon_pon_df.reset_index(drop=True)
            lon_pon_df.drop(columns=['原机房'],inplace=True)

            self.state_signal.emit('割接路由分析完成，正在写入数据库，请稍后...',90,'')
            writeDataBase('超长主光路调优方案',lon_pon_df)
            self.state_signal.emit('已完成...',100,'')

            
        except Exception as e:
            self.state_signal.emit('分析超长PON主光路调优方案失败:' + str(e),0,'')


# 分析ONU弱光的线程