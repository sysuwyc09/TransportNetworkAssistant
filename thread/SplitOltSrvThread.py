# OLT承载分流分析
# 对所选目标OLT网元，分析现有主光路哪些PON口可改割接至目标OLT网元所属机房。
# 通过箱体上联OLT跳纤路径表获取目标OLT机房三跳内可达设施及其跳纤路径，
# 匹配主光路（其OLT归属机房与目标OLT机房不一致），参照主光路调优逻辑计算割接字段，
# 按PON口去重取方案得分最高项，输出统计表与明细表。

from PySide6.QtCore import QThread, Signal
import os
import re
import datetime
import numpy as np
import pandas as pd
from .publicFunc import *


def extractRouteFacilities(route):
    '''提取光路文本路由中按顺序出现的割接点设施名称'''
    sites = re.findall('>(.*?)\([ABCD正反/面ODM0-9]+-\d+-\d+', route)
    if not sites:
        return []
    if '-POS' in sites[-1]:
        sites[-1] = re.findall('(.*)-POS', sites[-1])[0]
    return sites


class SplitOltSrvThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, olt_names):
        super().__init__()
        self.olt_names = olt_names

    def run(self):
        try:
            self.state_signal.emit('正在读取数据库资源...')
            olt_data_df = readDataBase('OLT网元数据集')
            relay_df = readDataBase('中继段')
            box_up_df = readDataBase('箱体上联OLT跳纤路径表')
            box_df = readDataBase('光交箱')[['设施名称', '机房名称']]
            oBox_df = readDataBase('分纤箱')[['设施名称', '机房名称']]
            odf_df = readDataBase('ODF')[['设施名称', '机房名称']]
            pon_df = readDataBase('主光路')

            if olt_data_df.empty or box_up_df.empty or pon_df.empty:
                self.error_signal.emit('数据库缺少OLT网元数据集、箱体上联OLT跳纤路径表或主光路数据')
                return

            # 目标OLT网元 -> 所属机房（目标OLT机房）
            target_olt_df = pd.DataFrame({'目标OLT网元': self.olt_names})
            olt_map = olt_data_df[['OLT网元', '所属机房']].drop_duplicates(subset=['OLT网元'])
            target_olt_df = target_olt_df.merge(olt_map, left_on='目标OLT网元', right_on='OLT网元',
                                                how='left').drop(columns=['OLT网元'])
            target_olt_df = target_olt_df.rename(columns={'所属机房': '目标OLT机房'})
            target_olt_df = target_olt_df.dropna(subset=['目标OLT机房'])
            target_rooms = target_olt_df['目标OLT机房'].dropna().unique().tolist()
            if not target_rooms:
                self.error_signal.emit('所选OLT网元在数据库均未找到所属机房')
                return

            # OLT机房集合（OLT网元所属机房），用于排除OLT机房之间跳纤的场景
            olt_rooms = set(olt_map['所属机房'].dropna().astype(str))
            # 设施->机房映射（用于判断设施所属机房是否为OLT机房）
            fac_room_map = pd.concat([box_df, oBox_df, odf_df], axis=0)
            fac_room_map = fac_room_map.dropna(subset=['设施名称', '机房名称'])
            fac_room_map = fac_room_map[fac_room_map['机房名称'] != '']
            fac_room_map = fac_room_map.drop_duplicates(subset='设施名称').set_index('设施名称')['机房名称']

            # 中继段的始端/终端设施可能为ODF、分纤箱、光交箱，且这些设施可能属于某机房；
            # 同一机房内设施间可跳纤，不同机房设施通过中继段跳纤。该可达关系已预计算进
            # 箱体上联OLT跳纤路径表（跳数<=3 即为三跳内可达）。筛选目标OLT机房一致、
            # 三跳内可达的设施，同一设施保留方案得分最高的一条。
            self.state_signal.emit('正在筛选目标OLT机房三跳内可达设施...')
            box_up_sel = box_up_df[box_up_df['目标OLT机房'].isin(target_rooms)].copy()
            box_up_sel['跳数'] = pd.to_numeric(box_up_sel['跳数'], errors='coerce')
            box_up_sel['方案得分'] = pd.to_numeric(box_up_sel['方案得分'], errors='coerce')
            box_up_sel = box_up_sel[box_up_sel['跳数'] <= 3]
            box_up_sel = box_up_sel.dropna(subset=['方案得分'])
            # 同一设施保留方案得分最高的一条
            box_up_sel = box_up_sel.sort_values(by='方案得分', ascending=False).drop_duplicates(
                subset='设施名称', keep='first')
            box_up_sel = box_up_sel[~box_up_sel['设施名称'].map(fac_room_map).isin(olt_rooms)]
            box_up_sel = box_up_sel.rename(columns={
                '跳纤距离': '调整后距离', '跳数': '调整后跳数',
                '光衰预算': '调整后光衰', '跳纤路径': '调整路径'
            })
            box_up_sel = box_up_sel[['设施名称', '目标OLT机房', '调整后距离', '调整后跳数',
                                     '调整后光衰', '调整路径', '方案得分']]
            if box_up_sel.empty:
                self.error_signal.emit('目标OLT机房三跳内未找到可达设施')
                return

            # 主光路与目标设施清单匹配：从光路文本路由按顺序提取割接点设施名称，
            # 取第一个出现在目标设施清单（box_up_sel）中的设施作为割接点，其对应的
            # 目标OLT机房即为目标OLT机房。
            self.state_signal.emit('正在匹配可割接主光路...')
            pon_df['光路文本路由'] = pon_df['光路文本路由'].astype(str)
            pon_df['光路长度'] = pd.to_numeric(pon_df['光路长度'], errors='coerce').fillna(0)
            pon_df['跳数'] = pon_df['光路文本路由'].apply(findJumpNum)
            pon_df['光衰'] = pon_df['跳数'] * 1 + pon_df['光路长度'] / 1000 * 0.35

            box_up_facilities = set(box_up_sel['设施名称'].dropna().astype(str))

            def matchRouteFacility(route):
                for site in extractRouteFacilities(route):
                    if site in box_up_facilities:
                        return site
                return None

            pon_df['设施名称'] = pon_df['光路文本路由'].apply(matchRouteFacility)
            pon_df = pon_df[pon_df['设施名称'].notna()].copy()
            if pon_df.empty:
                self.error_signal.emit('光路文本路由未包含目标设施')
                return
            # 按命中的割接点设施名称关联其目标OLT机房及跳纤路径信息
            pon_df = pon_df.merge(box_up_sel, on='设施名称', how='left')

            # 主光路OLT名称归属机房（原机房）
            olt_room_df = olt_map.rename(columns={'OLT网元': 'OLT名称', '所属机房': '原机房'})
            pon_df = pon_df.merge(olt_room_df, on='OLT名称', how='left')
            pon_df = pon_df[pon_df['原机房'] != pon_df['目标OLT机房']]
            if pon_df.empty:
                self.error_signal.emit('未找到OLT归属机房与目标OLT机房不一致的可割接主光路')
                return

            self.state_signal.emit('正在计算割接方案...')
            pon_df['优化光衰'] = pon_df['光衰'] - pon_df['调整后光衰']

            # 设施->机房映射（含中继段的始端/终端设施到机房关系）
            facility_df = pd.concat([
                box_df, oBox_df, odf_df,
                relay_df[['始端设施', '始端机房']].rename(columns={'始端设施': '设施名称', '始端机房': '机房名称'}),
                relay_df[['终端设施', '终端机房']].rename(columns={'终端设施': '设施名称', '终端机房': '机房名称'}),
            ], axis=0)
            facility_df = facility_df.dropna(subset=['设施名称', '机房名称'])
            facility_df = facility_df[facility_df['机房名称'] != '']
            facility_df = facility_df.drop_duplicates(subset='设施名称')
            site_dict = facility_df.set_index('设施名称')['机房名称'].to_dict()

            pon_df = pon_df.reset_index(drop=True)
            findKeyPointVec = np.vectorize(findKeyPoint, excluded=['site_dict'])
            pon_df['割接点'], pon_df['割接路由'], pon_df['割接可用芯数'] = findKeyPointVec(
                pon_df['光路文本路由'], pon_df['调整路径'], site_dict=site_dict)
            # 排除割接点为OLT机房的方案（不考虑从一个OLT机房跳纤割接到另一个OLT机房）
            pon_df = pon_df[~pon_df['割接点'].astype(str).isin(olt_rooms)]

            # 按PON口去重，只取方案得分最高的项
            pon_df = pon_df.sort_values(by='方案得分', ascending=False).drop_duplicates(
                subset='PON口', keep='first')
            pon_df['PON下挂ONU数量'] = pd.to_numeric(pon_df['PON下挂ONU数量'], errors='coerce').fillna(0).astype(int)

            if pon_df.empty:
                self.error_signal.emit('没有可行的割接方案')
                return

            self.state_signal.emit('正在生成分析结果...')
            # 明细表
            detail_cols = ['OLT名称', 'PON口', 'PON下挂ONU数量', 'OBD所属对象', '光路名称', '光路长度',
                           '光路文本路由', '跳数', '光衰', '目标OLT机房', '调整后距离', '调整后跳数',
                           '调整后光衰', '调整路径', '优化光衰', '割接点', '割接路由', '割接可用芯数']
            detail_df = pon_df[detail_cols].copy()

            # 统计表：目标OLT网元、目标OLT机房、可割接PON口数、下带ONU总数
            stat_rows = []
            for _, row in target_olt_df.iterrows():
                sub = detail_df[detail_df['目标OLT机房'] == row['目标OLT机房']]
                stat_rows.append({
                    '目标OLT网元': row['目标OLT网元'],
                    '目标OLT机房': row['目标OLT机房'],
                    '可割接PON口数': int(len(sub)),
                    '下带ONU总数': int(sub['PON下挂ONU数量'].sum()),
                })
            stat_df = pd.DataFrame(stat_rows, columns=['目标OLT网元', '目标OLT机房', '可割接PON口数', '下带ONU总数'])
            stat_df = stat_df.sort_values(by='可割接PON口数', ascending=False).reset_index(drop=True)

            os.makedirs('结果', exist_ok=True)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            out_path = os.path.join('结果', f'OLT承载分流分析结果{timestamp}.xlsx')
            with pd.ExcelWriter(out_path) as writer:
                stat_df.to_excel(writer, sheet_name='统计表', index=False)
                detail_df.to_excel(writer, sheet_name='明细表', index=False)

            self.state_signal.emit(f'分析完成，结果已保存至：{out_path}')
        except Exception as e:
            self.error_signal.emit(f'OLT承载分流分析失败：{str(e)}')