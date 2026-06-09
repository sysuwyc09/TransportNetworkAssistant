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

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class WriteBoxKmlThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, output_dir='结果/箱体图层', parent=None):
        super().__init__(parent)
        self.output_dir = output_dir
        
    def run(self):
        try:
            self.state_signal.emit('开始读取数据库...')
            conn = sqlite3.connect('data/TransportNetwork.db')
            
            self.state_signal.emit('读取ODF表格...')
            odf_df = pd.read_sql('SELECT 机房名称, 所属区县, 经度, 纬度 FROM ODF', conn)
            odf_df = odf_df.drop_duplicates()
            house_df = pd.read_sql('SELECT 机房名称, 业务级别 FROM 机房', conn)
            house_df = house_df.merge(odf_df,on='机房名称').drop_duplicates()
            house_df['类型'] = house_df['业务级别'] + '机房'
            house_df['名称'] = house_df['机房名称']
            house_df = house_df[['名称', '所属区县', '经度', '纬度', '类型']]
            
            self.state_signal.emit('读取光交箱表格...')
            gjx_df = pd.read_sql('SELECT 设施名称, 所属区县, 经度, 纬度, 分纤点级别 FROM 光交箱', conn)
            gjx_df = gjx_df.drop_duplicates()
            gjx_df['类型'] = gjx_df['分纤点级别'] + '光交箱'
            gjx_df['名称'] = gjx_df['设施名称']
            gjx_df = gjx_df[['名称', '所属区县', '经度', '纬度', '类型']]
            
            self.state_signal.emit('读取分纤箱表格...')
            fqx_df = pd.read_sql('SELECT 设施名称, 所属区县, 经度, 纬度, 容量 FROM 分纤箱', conn)
            fqx_df = fqx_df[fqx_df['容量'] >= 72].drop_duplicates()
            fqx_df['类型'] = '分纤箱'
            fqx_df['名称'] = fqx_df['设施名称']
            fqx_df = fqx_df[['名称', '所属区县', '经度', '纬度', '类型']]
            
            conn.close()
            
            all_df = pd.concat([house_df, gjx_df, fqx_df], ignore_index=True)
            all_df = all_df.drop_duplicates().astype(str)
            
            os.makedirs(self.output_dir, exist_ok=True)
            type_icon_map = {
                '核心(本地骨干)机房': 'star.png',
                '核心(省际)机房': 'star.png',
                '核心(省内)机房': 'star.png',
                '普通汇聚机房': 'homegardenbusiness.png',
                '业务汇聚机房': 'ranger_station.png',
                '本地接入机房': 'campground.png',
                '用户机房': 'info-i.png',
                '重要汇聚机房': 'sunny.png',
                '分纤箱': 'open-diamond.png',
                '一级光交箱': 'post_office.png',
                '二级光交箱': 'track.png',
                '接入网分纤箱光交箱': 'placemark_circle.png',
                '末端光交箱': 'placemark_circle.png',
                '普通光交箱': 'placemark_square.png'
            }
            
            districts = all_df['所属区县'].unique()
            total_districts = len(districts)
            
            for idx, district in enumerate(districts):
                self.state_signal.emit(f'正在处理 {district} ({idx+1}/{total_districts})...')
                district_df = all_df[all_df['所属区县'] == district]
                
                types = district_df['类型'].unique()
                folders = []
                
                for box_type in types:
                    type_df = district_df[district_df['类型'] == box_type]
                    places = []
                    icon = type_icon_map.get(box_type, 'donut.png')
                    
                    for _, row in type_df.iterrows():
                        places.append(writePoint(row['名称'], row['经度'], row['纬度'], icon, row['类型']))
                    
                    folders.append(writeFolder(box_type, places))
                
                kml_content = writeDoc(f'{district}机房箱体图层', folders)
                dt = datetime.datetime.now().strftime('%Y%m%d')
                file_path = os.path.join(self.output_dir, f'{district}箱体_{dt}.kml')
                
                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(kml_content)
            
            self.state_signal.emit(f'已完成！共处理 {total_districts} 个区县，输出至 {self.output_dir}')
            
        except Exception as e:
            self.error_signal.emit(f'处理失败: {str(e)}')

'''
更新一键数据线程
'''