'''
2000M用户割接分析线程，用于分析2000M用户的割接情况
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re


class TwoXGAnalysisThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, parent=None, file_path=''):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        try:
            self.state_signal.emit('正在加载2000M用户清单...')
            user_df = pd.read_excel(self.file_path, sheet_name='Sheet1', engine='openpyxl')
            
            self.state_signal.emit('正在筛选湛江用户...')
            # 2、筛选CITY列为"湛江"的用户
            zhanjiang_df = user_df[user_df['CITY'] == '湛江'].copy()
            
            self.state_signal.emit('正在判断重点小区用户...')
            # 3、判断是否为重点小区的用户
            zhanjiang_df['是否重点小区'] = (
                (zhanjiang_df['IS_4WAN_IMP_ADDR'] == '是') | 
                (zhanjiang_df['IS_9QIAN_IMP_ADDR'] == '是')
            ).apply(lambda x: '是' if x else '否')
            
            self.state_signal.emit('正在判断是否需割接...')
            # 4、判断是否需割接
            zhanjiang_df['是否需割接'] = (zhanjiang_df['TRANSPORT_TYPE'] == 'GPON').apply(lambda x: '是' if x else '否')
            
            self.state_signal.emit('正在统计PON口用户数...')
            # 5、按OLT_NAME、PORT_NAME分组统计，只统计需割接的用户
            need_cutover_df = zhanjiang_df[zhanjiang_df['是否需割接'] == '是'].copy()
            
            pon_port_table = need_cutover_df.groupby(['OLT_NAME', 'PORT_NAME']).agg({
                '是否需割接': 'size',
                '是否重点小区': lambda x: (x == '是').sum()
            }).reset_index()
            pon_port_table = pon_port_table.rename(columns={
                '是否需割接': '需要割接用户数',
                '是否重点小区': '重点小区需割接用户数'
            })
            pon_port_table['非重点小区需割接用户数'] = pon_port_table['需要割接用户数'] - pon_port_table['重点小区需割接用户数']
            
            self.state_signal.emit('正在读取OLT网元数据集...')
            # 6、读取数据库《OLT网元数据集》
            olt_df = readDataBase('OLT网元数据集')
            olt_df = olt_df[['OLT网元', '所属站点', '设备型号', 'XGPON口总数', 'XGPON口空闲数']]
            
            self.state_signal.emit('正在匹配OLT网元信息...')
            # 7、匹配OLT网元信息
            pon_port_table = pon_port_table.merge(
                olt_df,
                left_on='OLT_NAME',
                right_on='OLT网元',
                how='left'
            )
            pon_port_table = pon_port_table.drop(columns=['OLT网元'])
            
            self.state_signal.emit('正在读取主光路表...')
            # 读取主光路表
            main_path_df = readDataBase('主光路')
            # 只保留需要的列
            main_path_df = main_path_df[['PON口', '光路名称', '光路文本路由']]
            # 去重，保留第一个
            main_path_df = main_path_df.drop_duplicates(subset=['PON口'], keep='first')
            
            self.state_signal.emit('正在匹配光路信息...')
            # 匹配光路名称、光路文本路由
            pon_port_table = pon_port_table.merge(
                main_path_df,
                left_on='PORT_NAME',
                right_on='PON口',
                how='left'
            )
            pon_port_table = pon_port_table.drop(columns=['PON口'])
            
            self.state_signal.emit('正在判断千兆设备...')
            # 8、判断是否为千兆设备
            olt_df['是否千兆设备'] = olt_df['设备型号'].apply(
                lambda x: '是' if ('C600' in str(x) or '5800' in str(x)) else '否'
            )
            
            self.state_signal.emit('正在统计站点千兆设备...')
            # 9、按所属站点分组统计
            site_table = olt_df[olt_df['是否千兆设备'] == '是'].groupby('所属站点').agg({
                '是否千兆设备': 'size',
                'XGPON口总数': 'sum',
                'XGPON口空闲数': 'sum'
            }).reset_index()
            site_table = site_table.rename(columns={'是否千兆设备': '千兆OLT数'})
            
            self.state_signal.emit('正在匹配站点信息...')
            # 10、匹配站点千兆设备统计表
            pon_port_table = pon_port_table.merge(
                site_table,
                on='所属站点',
                how='left',
                suffixes=('', '_站点')
            )
            pon_port_table['千兆OLT数'] = pon_port_table['千兆OLT数'].fillna(0)
            pon_port_table['XGPON口总数_站点'] = pon_port_table['XGPON口总数_站点'].fillna(0)
            pon_port_table['XGPON口空闲数_站点'] = pon_port_table['XGPON口空闲数_站点'].fillna(0)
            
            self.state_signal.emit('正在制定PON口割接策略...')
            # 11、制定PON口割接策略
            pon_port_table = self.makeCutoverStrategy(pon_port_table)
            
            self.state_signal.emit('正在匹配割接目标OLT...')
            # 匹配割接目标OLT
            pon_port_table = self.matchTargetOLT(pon_port_table, olt_df)
            
            self.state_signal.emit('正在判断区域...')
            # 根据OLT_NAME使用正则表达式判断区域
            pon_port_table['区域'] = pon_port_table['OLT_NAME'].apply(self.getAreaFromOLTName)
            
            self.state_signal.emit('正在统计重点小区维度信息...')
            # 12、按是否重点小区维度分组统计
            key_area_table = self.analyzeByKeyArea(zhanjiang_df, pon_port_table)
            
            
            self.state_signal.emit('正在生成分析结果...')
            # 13、输出结果前，先筛选出两个额外的sheet
            # 重点小区待割接PON口：筛选重点小区需割接用户数>0的行
            key_area_pon_port = pon_port_table[pon_port_table['重点小区需割接用户数'] > 0].copy()
            
            # 非重点小区待割接PON口：筛选重点小区需割接用户数=0且割接策略=可割接的行，然后按所属站点分组，筛选超过2个的行
            non_key_area_pon_port = pon_port_table[
                (pon_port_table['重点小区需割接用户数'] == 0) & 
                (pon_port_table['割接策略'] == '可割接')
            ].copy()
            
            # 按所属站点分组，筛选超过2个的站点
            site_count = non_key_area_pon_port.groupby('所属站点').size()
            sites_with_more_than_2 = site_count[site_count > 2].index
            non_key_area_pon_port = non_key_area_pon_port[non_key_area_pon_port['所属站点'].isin(sites_with_more_than_2)]
            
            # 输出结果
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
            dir = os.path.dirname(self.file_path)
            out_file_path = os.path.join(dir, '2000M用户割接分析_' + dt + '.xlsx')
            with pd.ExcelWriter(out_file_path) as writer:
                key_area_table.to_excel(writer, sheet_name='统计表', index=False)
                pon_port_table.to_excel(writer, sheet_name='2000M用户需割接PON口明细表', index=False)
                key_area_pon_port.to_excel(writer, sheet_name='重点小区待割接PON口', index=False)
                non_key_area_pon_port.to_excel(writer, sheet_name='非重点小区待割接PON口（超2个）', index=False)
            
            self.state_signal.emit('分析完成！结果已保存到: ' + out_file_path)
        except Exception as e:
            self.error_signal.emit(f'分析过程出错: {str(e)}')

    def makeCutoverStrategy(self, pon_port_table):
        '''
        制定PON口割接策略
        '''
        # 按所属站点分组
        site_groups = pon_port_table.groupby('所属站点')
        strategy_list = []
        
        for site_name, group in site_groups:
            group = group.reset_index(drop=True)
            giga_olt_count = group['千兆OLT数'].iloc[0]
            xgpon_free_count = int(group['XGPON口空闲数_站点'].iloc[0])
            
            if giga_olt_count == 0:
                # 站点千兆OLT数为0
                group['割接策略'] = '暂不割接，需新建千兆OLT'
            else:
                site_pon_count = len(group)
                if site_pon_count > xgpon_free_count:
                    # 站点维度PON口数大于XGPON口空闲数，前XGPON口空闲数个为可割接
                    for i in range(len(group)):
                        if i < xgpon_free_count:
                            group.loc[i, '割接策略'] = '可割接'
                        else:
                            group.loc[i, '割接策略'] = '暂不割接，需扩容PON板'
                else:
                    # 站点维度PON口数小于等于XGPON口空闲数，全部可割接
                    group['割接策略'] = '可割接'
            
            strategy_list.append(group)
        
        return pd.concat(strategy_list, ignore_index=True)

    def analyzeByKeyArea(self, user_df, pon_port_table):
        '''
        按是否重点小区维度分组统计
        '''
        # 先将用户数据与PON口统计表合并，获取割接策略（只对需割接的用户）
        user_with_strategy = user_df.merge(
            pon_port_table[['OLT_NAME', 'PORT_NAME', '割接策略']],
            on=['OLT_NAME', 'PORT_NAME'],
            how='left'
        )
        # 对于不需要割接的用户，割接策略为空
        user_with_strategy.loc[user_with_strategy['是否需割接'] == '否', '割接策略'] = ''
        
        # 按是否重点小区分组
        key_area_stats = []
        
        for is_key in ['是', '否']:
            subset = user_with_strategy[user_with_strategy['是否重点小区'] == is_key]
            if len(subset) == 0:
                continue
                
            total_users = len(subset)
            need_cutover = len(subset[subset['是否需割接'] == '是'])
            can_cutover = len(subset[(subset['割接策略'] == '可割接') & (subset['是否需割接'] == '是')])
            need_expand = len(subset[(subset['割接策略'] == '暂不割接，需扩容PON板') & (subset['是否需割接'] == '是')])
            need_new_olt = len(subset[(subset['割接策略'] == '暂不割接，需新建千兆OLT') & (subset['是否需割接'] == '是')])
            
            key_area_stats.append({
                '是否重点小区': is_key,
                '用户数': total_users,
                '需要割接用户数': need_cutover,
                '可割接用户数': can_cutover,
                '暂不割接，需扩容PON板用户数': need_expand,
                '暂不割接，需新建千兆OLT用户数': need_new_olt
            })
        
        key_area_table = pd.DataFrame(key_area_stats)
        
        # 添加合计行
        if len(key_area_table) > 0:
            total_row = {
                '是否重点小区': '合计',
                '用户数': key_area_table['用户数'].sum(),
                '需要割接用户数': key_area_table['需要割接用户数'].sum(),
                '可割接用户数': key_area_table['可割接用户数'].sum(),
                '暂不割接，需扩容PON板用户数': key_area_table['暂不割接，需扩容PON板用户数'].sum(),
                '暂不割接，需新建千兆OLT用户数': key_area_table['暂不割接，需新建千兆OLT用户数'].sum()
            }
            key_area_table = pd.concat([key_area_table, pd.DataFrame([total_row])], ignore_index=True)
        
        return key_area_table

    def matchTargetOLT(self, pon_port_table, olt_df):
        '''
        匹配割接目标OLT
        '''
        # 先筛选出千兆OLT
        giga_olt_df = olt_df[
            (olt_df['设备型号'].apply(lambda x: 'C600' in str(x) or '5800' in str(x)))
        ].copy()
        
        # 初始化目标OLT列为空
        pon_port_table['目标OLT'] = ''
        
        # 按所属站点分组处理
        for site_name in pon_port_table['所属站点'].unique():
            # 获取当前站点的PON口
            site_pon_ports = pon_port_table[pon_port_table['所属站点'] == site_name]
            
            # 获取当前站点的千兆OLT
            site_giga_olts = giga_olt_df[giga_olt_df['所属站点'] == site_name]
            
            if len(site_giga_olts) == 0:
                continue
            
            # 处理两种情况：可割接 和 暂不割接需扩容
            for cutover_type in ['可割接', '暂不割接，需扩容PON板']:
                # 计算当前类型的PON口数量
                pon_count = len(site_pon_ports[site_pon_ports['割接策略'] == cutover_type])
                
                if pon_count == 0:
                    continue
                
                # 寻找满足要求的千兆OLT
                # 优先选择空闲口最多的OLT
                suitable_olt = None
                max_free_ports = 0
                
                for _, olt_row in site_giga_olts.iterrows():
                    # 对于"可割接"类型，要求空闲口 >= 需要的数量
                    # 对于"暂不割接，需扩容PON板"类型，即使空闲口不够，也选择空闲口最多的
                    if cutover_type == '可割接':
                        if olt_row['XGPON口空闲数'] >= pon_count:
                            if olt_row['XGPON口空闲数'] > max_free_ports:
                                max_free_ports = olt_row['XGPON口空闲数']
                                suitable_olt = olt_row['OLT网元']
                    else:
                        # 对于"暂不割接，需扩容PON板"，直接选择空闲口最多的OLT
                        if olt_row['XGPON口空闲数'] >= max_free_ports:
                            max_free_ports = olt_row['XGPON口空闲数']
                            suitable_olt = olt_row['OLT网元']
                
                # 如果找到了合适的OLT，将其设置为目标OLT
                if suitable_olt is not None:
                    pon_port_table.loc[
                        (pon_port_table['所属站点'] == site_name) & 
                        (pon_port_table['割接策略'] == cutover_type), 
                        '目标OLT'
                    ] = suitable_olt
        
        return pon_port_table

    def getAreaFromOLTName(self, olt_name):
        '''
        根据OLT_NAME使用正则表达式判断区域
        '''
        if pd.isna(olt_name):
            return '其他'
        
        olt_name_str = str(olt_name)
        
        # 使用正则表达式匹配区域
        area_pattern = r'(赤坎|麻章|霞山|坡头|开发区|雷州|廉江|吴川|遂溪|徐闻)'
        match = re.search(area_pattern, olt_name_str)
        
        if match:
            return match.group(1)
        else:
            return '其他'
