import pandas as pd
import numpy as np
import sqlite3
import os
import re
from datetime import datetime
from PySide6.QtCore import QThread, Signal


def stardBoard(oltName, boardId):
    if boardId == 300:
        return oltName + ' 不明槽位'
    else:
        return oltName + ' ' + str(boardId) + '槽'


def fixState(state):
    if state == '正常':
        return '在位'
    elif state == '在线':
        return '在位'
    elif state == '离线':
        return '不在位'
    else:
        return state


def isNotUse(use, need):
    if use == 0 and need == 0:
        return '否'
    else:
        return '是'


def isPonPort(portSubType):
    if portSubType in ['GPON_XGPON', 'GPON_XGSPON', 'GPON', 'EPON口', 'GPON口', 'XGPON']:
        return '是'
    else:
        return '否'


def isXgPonPort2(boardType):
    if 'CG' in str(boardType):
        return '是'
    elif 'GFBT' in str(boardType) or 'VSCP' in str(boardType):
        return '是'
    else:
        return '否'


def fixDevType(devType):
    if 'MA58' in str(devType):
        return 'MA58系列'
    elif 'MA56' in str(devType):
        return 'MA56系列'
    elif 'C600' in str(devType):
        return 'C600系列'
    elif 'C3' in str(devType):
        return 'C300系列'
    else:
        return '-'


class OltBoardAnalysisThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, output_dir):
        super(OltBoardAnalysisThread, self).__init__()
        self.output_dir = output_dir

    def run(self):
        # try:
        self.state_signal.emit('开始分析OLT PON板...')
        conn = sqlite3.connect('data/transportNetwork.db')

        self.state_signal.emit('读取PON端口数据...')
        pon_port_sql = '''SELECT * FROM PON端口'''
        pon_port_df = pd.read_sql(pon_port_sql, conn)

        self.state_signal.emit('读取华为PON单板数据...')
        hw_board_sql = '''SELECT * FROM 华为PON单板'''
        hw_board_df = pd.read_sql(hw_board_sql, conn)

        self.state_signal.emit('读取中兴PON单板数据...')
        zte_board_sql = '''SELECT * FROM 中兴PON单板'''
        zte_board_df = pd.read_sql(zte_board_sql, conn)

        self.state_signal.emit('读取OLT网元数据集...')
        olt_ne_sql = '''SELECT * FROM OLT网元数据集'''
        olt_ne_df = pd.read_sql(olt_ne_sql, conn)

        conn.close()

        if pon_port_df.empty:
            self.error_signal.emit('PON端口表为空')
            return
        if hw_board_df.empty and zte_board_df.empty:
            self.error_signal.emit('华为PON单板表和中兴PON单板表均为空')
            return
        if olt_ne_df.empty:
            self.error_signal.emit('OLT网元数据集表为空')
            return

        self.state_signal.emit('处理华为PON单板数据...')
        hw_board_df['槽位'] = pd.to_numeric(hw_board_df['槽位号'], errors='coerce').fillna(0).astype(int)
        hw_board_df['板卡名称'] = hw_board_df.apply(lambda row: stardBoard(row['所属网元'], row['槽位']), axis=1)
        hw_board_df = hw_board_df[['板卡名称', '单板状态', '单板类型']]
        hw_board_df.rename(columns={'单板状态': '板卡状态', '单板类型': '板卡类型'}, inplace=True)

        self.state_signal.emit('处理中兴PON单板数据...')
        zte_board_df['槽位'] = zte_board_df['板卡槽位'].apply(
            lambda x: int(x.split('-')[2]) if isinstance(x, str) and '-' in x else 0
        )
        zte_board_df['板卡名称'] = zte_board_df.apply(lambda row: stardBoard(row['网元名称'], row['槽位']), axis=1)
        zte_board_df = zte_board_df[['板卡名称', '板卡状态', '板卡类型']]

        self.state_signal.emit('合并板卡数据...')
        board_df = pd.concat([hw_board_df, zte_board_df], ignore_index=True)
        board_df['板卡状态'] = board_df['板卡状态'].apply(fixState)
        self.state_signal.emit('筛选PON口...')
        pon_port_df['是否PON口'] = pon_port_df['端口子类型'].apply(isPonPort)
        pon_port_df = pon_port_df[pon_port_df['是否PON口'] == '是']

        if pon_port_df.empty:
            self.error_signal.emit('未筛选到PON口数据')
            return

        self.state_signal.emit('构建板卡名称...')
        pon_port_df['OLT'] = pon_port_df['所属传输网元']
        pon_port_df['槽位'] = pon_port_df['PONID'].apply(lambda x: int(x.split('-')[-2]) if isinstance(x, str) and '-' in x else 300)
        pon_port_df['板卡名称'] = pon_port_df.apply(lambda row: stardBoard(row['所属传输网元'], row['槽位']), axis=1)

        self.state_signal.emit('匹配PON端口与板卡状态...')
        pon_port_df = pon_port_df.merge(board_df, on='板卡名称', how='left')
        pon_port_df['板卡状态'] = pon_port_df['板卡状态'].fillna('网管不存在')
        pon_port_df['板卡类型'] = pon_port_df['板卡类型'].fillna('网管不存在')
        all_pon_table = pd.pivot_table(pon_port_df,index=['OLT', '板卡名称', '板卡状态', '板卡类型','槽位'], columns=['端口状态'], aggfunc={'端口名称': 'count'}, fill_value=0)
        all_pon_table.columns = all_pon_table.columns.droplevel()
        all_pon_table = all_pon_table.reset_index()
        for col in ['占用', '空闲', '预占', '部分占用']:
            if col not in all_pon_table.columns:
                all_pon_table[col] = 0        
        src_board_df = all_pon_table[['OLT', '板卡名称', '板卡状态', '板卡类型','槽位','占用','空闲','预占','部分占用']].drop_duplicates()
        src_board_df['槽位'] = src_board_df['槽位'].apply(lambda x: '不明槽位' if x==300 else x)


        self.state_signal.emit('筛选在位板卡...')
        pon_port_df = pon_port_df[pon_port_df['板卡状态'] == '在位']

        if pon_port_df.empty:
            self.error_signal.emit('未筛选到在位板卡数据')
            return

        self.state_signal.emit('生成OLT PON板清单...')
        not_use_table = pd.pivot_table(
            pon_port_df,
            index=['OLT', '板卡名称'],
            columns=['端口状态'],
            aggfunc={'端口名称': 'count'},
            fill_value=0
        )
        if not_use_table.columns.nlevels > 1:
            not_use_table.columns = not_use_table.columns.droplevel()
        not_use_table = not_use_table.reset_index()

        not_use_table = not_use_table.merge(board_df, on='板卡名称', how='left')

        for col in ['占用', '空闲', '预占', '部分占用']:
            if col not in not_use_table.columns:
                not_use_table[col] = 0

        not_use_table['是否千兆'] = not_use_table['板卡类型'].apply(isXgPonPort2)
        not_use_table['是否在用'] = np.where((not_use_table['占用'] == 0) & (not_use_table['预占'] == 0), '否', '是')
        not_use_table['端口数量'] = not_use_table['占用'] + not_use_table['预占'] + not_use_table['空闲'] + not_use_table['部分占用']
        not_use_table['在用端口数'] = not_use_table['占用'] + not_use_table['预占']
        not_use_table['设备系列'] = not_use_table['OLT'].apply(fixDevType)
        not_use_table.rename(columns={'OLT': '本地名称'}, inplace=True)

        temp_df = olt_ne_df[['OLT网元', '设备型号', '所属站点', '所属机房', '生命周期状态']].copy()
        temp_df.rename(columns={'OLT网元': '本地名称', '所属机房': '所属机房/位置点'}, inplace=True)
        not_use_table = not_use_table.merge(temp_df, how='left', on='本地名称')

        result_cols = [
            '本地名称', '板卡名称', '占用', '空闲', '部分占用', '预占', '板卡状态', '板卡类型',
            '是否千兆', '是否在用', '端口数量', '在用端口数', '设备系列', '设备型号',
            '所属站点', '所属机房/位置点', '生命周期状态'
        ]
        for col in result_cols:
            if col not in not_use_table.columns:
                not_use_table[col] = ''

        olt_pon_board_list = not_use_table[result_cols]

        self.state_signal.emit('生成不在位板卡清单...')
        absent_board_df = src_board_df[(src_board_df['板卡状态'] == '不在位')|(src_board_df['板卡状态'] == '网管不存在')].copy()
        temp_df = olt_ne_df[['OLT网元', '设备型号', '所属站点', '所属机房', '生命周期状态']].copy().rename(columns={'OLT网元': 'OLT'})
        absent_board_df = absent_board_df.merge(temp_df, how='left', on='OLT')
        absent_board_df['生命周期状态'] = absent_board_df['生命周期状态'].fillna('非现网态')


        self.state_signal.emit('输出分析结果...')
        dt = datetime.now().strftime('%Y-%m-%d')
        output_path = os.path.join(self.output_dir, f'OLT_PON板_分析结果-{dt}.xlsx')

        with pd.ExcelWriter(output_path) as writer:
            olt_pon_board_list.to_excel(writer, sheet_name='OLT PON板清单', index=False)
            absent_board_df.to_excel(writer, sheet_name='不在位的板卡清单', index=False)

        self.state_signal.emit(f'分析完成，结果已保存至：{output_path}')

        # except Exception as e:
        #     self.error_signal.emit(f'分析失败：{str(e)}')