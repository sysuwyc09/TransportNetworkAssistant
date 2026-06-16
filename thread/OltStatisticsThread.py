# 统计OLT站点OLT数量及网元类型详细

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import datetime
from .publicFunc import *

class OltStatisticsThread(QThread):
    state_signal = Signal(str, int, str)  # 当前进度情况、百分比、预估完成时间
    result_signal = Signal(str)  # 输出文件路径信号

    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            self.state_signal.emit("开始统计OLT站点信息", 10, "")
            
            conn = sqlite3.connect('data/transportNetwork.db')
            
            sql = """
            SELECT o.*, j.所属站点, j.业务级别 AS 机房类型, j.生命周期状态 AS 机房状态, j.产权单位 AS 产权单位
            FROM OLT网元 o
            JOIN 机房 j ON o.所属机房 = j.机房名称
            """
            olt_df = pd.read_sql_query(sql, conn)
            self.state_signal.emit(f"查询OLT网元数据完成，共{len(olt_df)}条", 30, "")
            
            # 统计每个站点的OLT数量
            site_olt_count = olt_df.groupby('所属站点')['网元名称'].count().reset_index()
            site_olt_count.rename(columns={'网元名称': 'OLT数量'}, inplace=True)
            
            # 统计每个站点的设备型号分布
            site_device_type = olt_df.groupby(['所属站点', '设备型号']).size().reset_index(name='设备数量')
            
            # 按站点透视设备型号
            device_type_pivot = pd.pivot_table(
                site_device_type, 
                index='所属站点', 
                columns='设备型号', 
                values='设备数量', 
                fill_value=0
            ).reset_index()
            
            # 合并OLT数量和设备型号分布
            result_df = site_olt_count.merge(device_type_pivot, on='所属站点', how='left')
            
            # 判断是否为千兆OLT
            def is_10g_olt(device_type):
                device_type = str(device_type)
                return 'MA5800' in device_type or 'C600' in device_type
            
            # 获取每个站点的OLT列表（格式：型号（数量）、型号（数量））
            def format_olt_list(group):
                device_count = group['设备型号'].value_counts()
                items = []
                for device_type, count in device_count.items():
                    items.append(f"{device_type}（{count}）")
                return '、'.join(items)
            
            # 获取每个站点的千兆OLT列表（格式：型号（数量）、型号（数量））
            def format_10g_olt_list(group):
                # 筛选千兆OLT
                ten_g_olt = group[group['设备型号'].apply(is_10g_olt)]
                if len(ten_g_olt) == 0:
                    return ''
                device_count = ten_g_olt['设备型号'].value_counts()
                items = []
                for device_type, count in device_count.items():
                    items.append(f"{device_type}（{count}）")
                return '、'.join(items)
            
            site_olt_list = olt_df.groupby('所属站点').apply(format_olt_list).reset_index()
            site_olt_list.rename(columns={0: 'OLT列表'}, inplace=True)
            result_df = result_df.merge(site_olt_list, on='所属站点', how='left')
            
            site_10g_olt_list = olt_df.groupby('所属站点').apply(format_10g_olt_list).reset_index()
            site_10g_olt_list.rename(columns={0: '千兆OLT列表'}, inplace=True)
            result_df = result_df.merge(site_10g_olt_list, on='所属站点', how='left')
            
            # 按OLT数量降序排序
            result_df = result_df.sort_values('OLT数量', ascending=False)
            
            self.state_signal.emit(f"统计完成，共{len(result_df)}个站点", 80, "")
            
            # 生成输出文件名
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"OLT站点统计_{timestamp}.xlsx"
            
            # 写入Excel
            result_df.to_excel(output_file, index=False)
            writeDataBase('OLT站点统计表', result_df)
            
            self.state_signal.emit(f"统计完成，文件已保存至: {output_file}", 100, "")
            self.result_signal.emit(output_file)
            
            conn.close()
            
        except Exception as e:
            self.state_signal.emit(f"统计失败: {str(e)}", 0, "")
