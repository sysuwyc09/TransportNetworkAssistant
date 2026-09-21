# 汇聚层中继段落高利用率分析
# 匹配始端/终端机房业务级别均为“普通汇聚”的中继段，按站点段落聚合，
# 输出剩余纤芯不足12芯且纤芯占用率超85%的紧张段落清单及段落详细清单。

from PySide6.QtCore import QThread, Signal
import sqlite3
import os
import datetime
import pandas as pd
import numpy as np
from .publicFunc import *


class AggrBusyLineThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            self.state_signal.emit('正在读取中继段表...')
            relay_df = readDataBase('中继段')
            if relay_df.empty:
                self.error_signal.emit('中继段表为空')
                return

            self.state_signal.emit('正在读取机房表...')
            house_df = readDataBase('机房')
            if house_df.empty:
                self.error_signal.emit('机房表为空')
                return

            self.state_signal.emit('正在筛选普通汇聚机房...')
            aggr_house_df = house_df[(house_df['业务级别'].isin(['普通汇聚', '业务汇聚','重要汇聚']))][['机房名称']].drop_duplicates()
            if aggr_house_df.empty:
                self.error_signal.emit('机房表中未找到业务级别为“普通汇聚”或“业务汇聚”或“重要汇聚”的机房')
                return

            self.state_signal.emit('正在匹配汇聚中继段...')
            merged = relay_df.merge(aggr_house_df, left_on='始端机房', right_on='机房名称', how='inner')
            merged = merged.merge(aggr_house_df, left_on='终端机房', right_on='机房名称', how='inner',
                                  suffixes=('_始', '_终'))
            merged = merged[merged['始端机房'] != merged['终端机房']]
            merged.drop(columns=['机房名称_终', '机房名称_始'], inplace=True)
            if merged.empty:
                self.error_signal.emit('未匹配到始端、终端机房均为汇聚机房的中继段')
                return

            self.state_signal.emit('正在统一段落名称并聚合...')
            merged = merged.copy()
            merged['始端站点'] = merged['始端站点'].fillna('').astype(str)
            merged['终端站点'] = merged['终端站点'].fillna('').astype(str)
            merged['中继纤芯数量'] = pd.to_numeric(merged['中继纤芯数量'], errors='coerce').fillna(0)
            merged['空闲数量'] = pd.to_numeric(merged['空闲数量'], errors='coerce').fillna(0)
            merged['段落名称'] = merged.apply(lambda r: '-'.join(sorted([r['始端站点'], r['终端站点']])), axis=1)

            detail_df = merged.groupby('段落名称').agg(
                中继段数量=('名称', 'count'),
                中继纤芯数量=('中继纤芯数量', 'sum'),
                空闲数量=('空闲数量', 'sum'),
                段落长度=('长度', 'min')
            ).reset_index()
            detail_df['占用数量'] = (detail_df['中继纤芯数量'] - detail_df['空闲数量']).astype(int)
            detail_df['中继段数量'] = detail_df['中继段数量'].astype(int)
            detail_df['中继纤芯数量'] = detail_df['中继纤芯数量'].astype(int)
            detail_df['空闲数量'] = detail_df['空闲数量'].astype(int)
            detail_df['纤芯占用率(%)'] = detail_df.apply(
                lambda r: round(r['占用数量'] / r['中继纤芯数量'] * 100, 2) if r['中继纤芯数量'] > 0 else 0,
                axis=1
            )

            cols = ['段落名称', '段落长度', '中继段数量', '中继纤芯数量', '占用数量', '空闲数量', '纤芯占用率(%)']
            detail_df = detail_df[cols].sort_values(by='纤芯占用率(%)', ascending=False).reset_index(drop=True)

            self.state_signal.emit('正在筛选紧张段落...')
            tense_df = detail_df[(detail_df['空闲数量'] < 12) & (detail_df['纤芯占用率(%)'] > 80)].reset_index(drop=True)
            tense_df = tense_df[tense_df['中继纤芯数量'] >= 24]
            tense_df['段落长度'] = tense_df['段落长度'].astype(int).apply(lambda x: round(x/1000, 2))
            # 中继段表更新日期
            dt = self.getRelayUpdateDate()

            self.state_signal.emit('正在生成分析结果文件...')
            os.makedirs('结果', exist_ok=True)
            out_path = os.path.join('结果', f'汇聚段落紧张分析-{dt}.xlsx')
            with pd.ExcelWriter(out_path) as writer:
                tense_df.to_excel(writer, sheet_name='段落紧张清单', index=False)
                detail_df.to_excel(writer, sheet_name='汇聚中继段落详细清单', index=False)
                merged.to_excel(writer, sheet_name='汇聚中继段原始数据', index=False)

            self.state_signal.emit(f'分析完成，结果已保存至：{out_path}')
        except Exception as e:
            self.error_signal.emit(f'分析失败：{str(e)}')

    def getRelayUpdateDate(self):
        '''获取中继段表的更新日期，返回 YYYY-MM-DD 格式'''
        try:
            update_df = readDataBase('表格更新时间')
            if not update_df.empty and '表名' in update_df.columns and '更新时间' in update_df.columns:
                row = update_df[update_df['表名'] == '中继段']
                if len(row) > 0 and pd.notna(row.iloc[0]['更新时间']):
                    return str(row.iloc[0]['更新时间']).split(' ')[0]
        except Exception:
            pass
        return datetime.datetime.now().strftime('%Y-%m-%d')