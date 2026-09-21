# 箱体上联纤芯紧张状态分析

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class BusyBoxUplinkThread(QThread):
    state_signal = Signal(str)
    def __init__(self,dir_path):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super().__init__()
        self.dir_path = dir_path
    
    def run(self):
        # try:
        self.state_signal.emit('正在加载全量箱体上联OLT机房...')
        box_uplink_df = readDataBase('箱体上联OLT跳纤路径表')
        all_line_df = readDataBase('中继段')[[]]
        if box_uplink_df.shape[0] == 0:
            self.state_signal.emit('查询不到箱体上联方案,请先运行箱体上联方案分析...')
            return
        # self.busyBoxLevelUplink(box_uplink_df)
        self.busyBoxUplink(box_uplink_df)
        #     self.state_signal.emit('已完成...')
        # except Exception as e:
        #     self.state_signal.emit('分析箱体上联纤芯紧张状态失败:' + str(e))

    def busyBoxUplink(self,box_uplink_df):
        # 根据评分选取最优方案
        box_uplink_df.sort_values(by=['设施名称','方案得分'],ascending=[True,False],inplace=True)
        best_box_uplink_df = box_uplink_df.groupby('设施名称').first().reset_index()
        all_red_uplink_df = best_box_uplink_df[best_box_uplink_df['最小空闲芯数'] <=4]
        box_df = readDataBase('光交箱')[['设施名称','容量']]
        box_red_uplink_df = all_red_uplink_df.merge(box_df,on='设施名称')
        # box_red_uplink_df = box_red_uplink_df[box_red_uplink_df['容量'] >=96]
        box_red_uplink_df = box_red_uplink_df[box_red_uplink_df['容量'] >=288]
        self.state_signal.emit(f'已查询到{box_red_uplink_df.shape[0]}个288及以上光交箱上联纤芯紧张状态...')
        dfs = []
        for i in range(len(box_red_uplink_df)):
            row = box_red_uplink_df.iloc[i]
            lines = re.findall(r'{(.*?)}\((\d+)\/(\d+)\)', row['跳纤路径'])
            temp_df = pd.DataFrame(lines,columns=['中继段','空闲芯数','芯数'])
            temp_df['设施名称'] = row['设施名称']
            dfs.append(temp_df)
        line_df = pd.concat(dfs)
        line_df['空闲芯数'] = line_df['空闲芯数'].astype(int)
        line_df['芯数'] = line_df['芯数'].astype(int)
        line_df = line_df[line_df['空闲芯数'] <= 4]
        line_table = pd.pivot_table(line_df,index=['中继段'],aggfunc={'设施名称':'count'})
        line_table.rename(columns={'设施名称':'影响光交箱数'},inplace=True)
        # 将设施名称按中继段分组，并合并
        temp_grp = line_df.groupby('中继段')['设施名称'].apply(lambda x: ','.join(x)).reset_index()
        result_df = line_df[['中继段','空闲芯数','芯数']].drop_duplicates().copy()
        result_df = result_df.merge(line_table,on='中继段',how='left')
        result_df = result_df.merge(temp_grp,on='中继段',how='left')

        lines = readDataBase('中继段')
        temp_df = lines[['名称','长度']].copy().rename(columns={'名称':'中继段'})
        result_df = result_df.merge(temp_df,on='中继段',how='left')

        # 读取中继段-光缆段对应关系
        line_to_fiber = readDataBase('中继段至光缆段')
        fiber_df = line_to_fiber.merge(result_df,on='中继段').drop_duplicates()
        all_fiber = readDataBase('光缆段')
        all_fiber = all_fiber[['名称','光纤数目']].rename(columns={'名称':'光缆段','光纤数目':'光缆芯数'})
        fiber_df = fiber_df.merge(all_fiber,on='光缆段',how='left')
        temp_df = fiber_df[['光缆段']].copy().drop_duplicates()
        temp_df = temp_df.merge(line_to_fiber,on='光缆段',how='left')
        temp_df = temp_df.merge(lines,left_on='中继段',right_on='名称')
        temp_table = pd.pivot_table(temp_df,index=['光缆段'],aggfunc={'中继纤芯数量':'sum'})
        temp_table.rename(columns={'中继纤芯数量':'光缆成端数'},inplace=True)
        temp_table = temp_table.reset_index()
        fiber_df = fiber_df.merge(temp_table,on='光缆段',how='left')
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].fillna(0)
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].astype(int)
        fiber_df['光缆成端数'] = fiber_df['光缆成端数'].astype(int)
        fiber_df['是否有预留纤芯'] = '否'
        for i in range(fiber_df.shape[0]):
            row = fiber_df.iloc[i]
            if row['光缆芯数'] > row['光缆成端数']:
                fiber_df.loc[i,'是否有预留纤芯'] = '是'
        fiber_table = pd.pivot_table(fiber_df,index=['中继段'],columns=['是否有预留纤芯'],aggfunc={'中继段':'count'})
        fiber_table.columns = fiber_table.columns.droplevel(0)
        fiber_table['是否有预留纤芯'] = fiber_table['否'].apply(lambda x: '否' if x > 0 else '是')
        fiber_table = fiber_table.reset_index()[['中继段','是否有预留纤芯']]
        fiber_df['光缆成端数'] = fiber_df['光缆成端数'].astype(str)
        fiber_df['光缆芯数'] = fiber_df['光缆芯数'].astype(str)
        fiber_df['光缆段情况'] = fiber_df['光缆段'] + '(是否有预留：' + fiber_df['是否有预留纤芯'] + '【' + fiber_df['光缆成端数'] + '/' + fiber_df['光缆芯数'] + '】)'
        temp_df = fiber_df[['中继段','光缆段情况']].copy().drop_duplicates()
        temp_grp = temp_df.groupby('中继段')['光缆段情况'].apply(lambda x: ','.join(x)).reset_index()
        result_df = result_df.merge(fiber_table,on='中继段',how='left')
        result_df = result_df.merge(temp_grp,on='中继段',how='left')
        self.state_signal.emit('分析完成，正在生成表格，请稍后...')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with pd.ExcelWriter(f'{self.dir_path}/箱体上联纤芯紧张分析288及以上{dt}.xlsx') as writer:
            best_box_uplink_df.to_excel(writer,sheet_name='所有箱体上联最优方案',index=False)
            box_red_uplink_df.to_excel(writer,sheet_name='光交箱上联纤芯紧张状态',index=False)
            result_df.to_excel(writer,sheet_name='光交箱紧张中继段详细',index=False)
            fiber_df.to_excel(writer,sheet_name='光交箱紧张光缆段详细',index=False)
        self.state_signal.emit('分析完成，表格已生成')


    def houseLevel(self,house_df,olt_df):
        house_df = house_df[house_df['机房类型']=='传输机房']
        house_df = house_df[house_df['业务级别']!='用户']
        house_df = house_df[house_df['业务级别']!='本地接入']
        house_df = house_df[house_df['生命周期状态']!='退网']
        house_df = house_df[['机房名称','业务级别']].copy().rename(columns={'机房名称':'分纤点名称','业务级别':'细分'})
        house_df['类型'] = '汇聚机房'
        house_df['级别'] = 1
        olt_house_df = olt_df[['所属机房']].copy().rename(columns={'所属机房':'分纤点名称'}).drop_duplicates()
        olt_house_df = olt_house_df.merge(house_df,on='分纤点名称',how='left')
        olt_house_df = olt_house_df[olt_house_df['类型'].isnull()]
        olt_house_df['细分'] = 'OLT机房'
        olt_house_df['类型'] = 'OLT机房'
        olt_house_df['级别'] = 1
        return house_df,olt_house_df

    def getAllDev(self,house_df,box_df,oBox_df):
        house_df = house_df[house_df['业务级别']=='本地接入']
        house_df = house_df[house_df['生命周期状态']!='退网']
        house_df = house_df[['机房名称']].rename(columns={'机房名称':'分纤点名称'})
        house_df['设施类型'] = '接入机房'
        box_df = box_df[box_df['容量']>=96]
        box_df = box_df[['设施名称','机房名称','容量']].rename(columns={'设施名称':'分纤点名称'})
        box_df['设施类型'] = '光交箱'
        oBox_df = oBox_df[oBox_df['容量']>=96]
        oBox_df = oBox_df[['设施名称','机房名称','容量']].rename(columns={'设施名称':'分纤点名称'})
        oBox_df['设施类型'] = '分纤箱'
        house_box_df = pd.concat([box_df,oBox_df],ignore_index=True)
        temp_df = house_box_df[['分纤点名称','设施类型','容量']]
        dev_df = pd.concat([temp_df,house_df],ignore_index=True)
        dev_df = dev_df.drop_duplicates()
        house_box_df['机房名称'] = house_box_df['机房名称'].fillna('')
        house_box_df['机房名称'] = house_box_df['机房名称'].astype(str)
        house_box_df = house_box_df[house_box_df['机房名称']!='']
        return dev_df,house_box_df

    def notLevelDev(self,dev_df,point_df):
        temp_df = point_df[['分纤点名称','级别']]
        not_level_dev = dev_df.merge(temp_df,on='分纤点名称',how='left')
        not_level_dev = not_level_dev[not_level_dev['级别'].isnull()][['分纤点名称','设施类型','容量']]
        not_level_dev = not_level_dev.drop_duplicates()
        return not_level_dev

    def findDevLevel(self,not_level_df,point_df,line_df,run_count):
        if not_level_df.empty:
            return point_df
        line_df = line_df.merge(point_df,left_on='始端',right_on='分纤点名称')[['始端','终端']]
        line_df = line_df.merge(not_level_df,left_on='终端',right_on='分纤点名称')
        temp_df = line_df[['分纤点名称','设施类型','始端','容量']]
        temp_df = temp_df.drop_duplicates(subset=['分纤点名称'],keep='first')
        temp_df['级别'] = 2
        temp_df['细分'] = f'第{run_count}轮二级分纤点分析出，上联：'+temp_df['始端']
        temp_df['类型'] = temp_df['设施类型']
        temp_df = temp_df[['分纤点名称','级别','细分','类型','容量']]
        point_df = pd.concat([point_df,temp_df],ignore_index=True)
        return point_df

    def boxGrpLevel(self,box_grp_df,point_df):
        box_grp_df = box_grp_df.rename(columns={'设备名称':'分纤点名称'})
        box_grp_df = box_grp_df.merge(point_df,on='分纤点名称',how='left')
        box_grp_df['级别'] = box_grp_df['级别'].fillna(3)
        not_level_box_grp = box_grp_df[box_grp_df['级别']==3]
        if not_level_box_grp.empty:
            return point_df
        box_min_level = box_grp_df.groupby('集群列表')['级别'].min().reset_index().rename(columns={'级别':'最高级别'})
        box_grp_df = box_grp_df.merge(box_min_level,on='集群列表',how='left')
        best_box = box_grp_df[box_grp_df['级别']==box_grp_df['最高级别']]
        best_box = best_box.drop_duplicates(subset=['集群列表'],keep='first')[['集群列表','分纤点名称','最高级别']].rename(columns={'分纤点名称':'最高级别的分纤点名称'})
        not_level_box_grp = not_level_box_grp.merge(best_box,on='集群列表',how='left')
        not_level_box_grp = not_level_box_grp[not_level_box_grp['最高级别']<3]
        if not_level_box_grp.empty:
            return point_df
        not_level_box_grp['最高级别'] = not_level_box_grp['最高级别'].astype(int)
        not_level_box_grp = not_level_box_grp[['分纤点名称','最高级别','最高级别的分纤点名称']].astype(str)
        not_level_box_grp['细分'] = '集群箱体：' + not_level_box_grp['最高级别的分纤点名称'] + '(' + not_level_box_grp['最高级别'] + ')'
        not_level_box_grp['最高级别'] = not_level_box_grp['最高级别'].astype(int)
        not_level_box_grp = not_level_box_grp[['分纤点名称','细分','最高级别']].rename(columns={'最高级别':'级别'}).drop_duplicates()
        not_level_box_grp['类型'] = '集群箱体'
        point_df = pd.concat([point_df,not_level_box_grp],ignore_index=True)
        return point_df

    def houseBoxLevel(self,house_box_df,point_df):
        temp_df = point_df[['分纤点名称','级别']].copy().rename(columns={'级别':'分纤点级别'})
        house_box_df = house_box_df.merge(temp_df,on='分纤点名称',how='left')
        house_box_df = house_box_df[house_box_df['分纤点级别'].isnull()]
        temp_df = point_df[['分纤点名称','级别']].copy().rename(columns={'分纤点名称':'机房名称','级别':'机房级别'})
        house_box_df = house_box_df.merge(temp_df,on='机房名称')
        house_box_df['级别'] = house_box_df['机房级别']
        house_box_df['类型'] = house_box_df['设施类型']
        house_box_df['机房级别'] = house_box_df['机房级别'].astype(str)
        house_box_df['细分'] = '归属机房:' + house_box_df['机房名称'] + '(级别：' + house_box_df['机房级别'] + ')'
        house_box_df = house_box_df[['分纤点名称','级别','细分','类型']].drop_duplicates()
        point_df = pd.concat([point_df,house_box_df],ignore_index=True)
        return point_df

    def getLevel(self,house_df,aggr_house_df,olt_house_df,line_df,box_df,oBox_df,box_grp_df):
        line_df = line_df[['名称','中继纤芯数量','始端机房','终端机房','始端设施','终端设施']]
        line_df = line_df[line_df['中继纤芯数量']>=12]
        line_df2 = line_df.copy().rename(columns={'始端机房':'终端机房','终端机房':'始端机房','始端设施':'终端设施','终端设施':'始端设施'})
        line_df = pd.concat([line_df,line_df2],ignore_index=True)

        temp_df = aggr_house_df[['分纤点名称']].copy().rename(columns={'分纤点名称':'始端机房'})
        link_to_level1_house = line_df.merge(temp_df,on='始端机房')

        box_576up_df = box_df[box_df['容量']>=576].copy()
        box_576up_df = box_576up_df[['设施名称','容量']].rename(columns={'设施名称':'终端设施'})
        first_box = link_to_level1_house.merge(box_576up_df,on='终端设施')
        first_box = first_box[['终端设施','始端机房','容量']].drop_duplicates(subset=['终端设施'],keep='first').rename(columns={'终端设施':'分纤点名称'})
        first_box['级别'] = 1
        first_box['类型'] = '光交箱'
        first_box['细分'] = '直达汇聚:' + first_box['始端机房']
        step_1_box = first_box[['分纤点名称','级别','细分','类型','容量']].drop_duplicates()
        point_df = pd.concat([aggr_house_df,olt_house_df,step_1_box],ignore_index=True)

        point_df = self.boxGrpLevel(box_grp_df,point_df)

        all_dev_df,house_box_df = self.getAllDev(house_df,box_df,oBox_df)
        line_df['始端'] = fixSite(line_df['始端机房'],line_df['始端设施'])
        line_df['终端'] = fixSite(line_df['终端机房'],line_df['终端设施'])
        line_df = line_df[['始端','终端']]

        run_flag = True
        run_count = 1
        current_shape = point_df.shape[0]
        while run_flag:
            not_level_df = self.notLevelDev(all_dev_df,point_df)
            point_df = self.findDevLevel(not_level_df,point_df,line_df,run_count)
            if point_df.shape[0] == current_shape:
                run_flag = False
            else:
                current_shape = point_df.shape[0]
                run_count += 1
            point_df = self.boxGrpLevel(box_grp_df,point_df)
            if run_count > 4:
                run_flag = False

        point_df = self.houseBoxLevel(house_box_df,point_df)
        return point_df

    def busyBoxLevelUplink(self,box_uplink_df):
        house_df = readDataBase('机房')
        olt_df = readDataBase('OLT网元')
        line_df = readDataBase('中继段')
        box_df = readDataBase('光交箱')
        oBox_df = readDataBase('分纤箱')
        box_grp_df = readDataBase('集群管理')

        aggr_house_df,olt_house_df = self.houseLevel(house_df,olt_df)
        point_df = self.getLevel(house_df,aggr_house_df,olt_house_df,line_df,box_df,oBox_df,box_grp_df)

        box_uplink_df.sort_values(by=['设施名称','方案得分'],ascending=[True,False],inplace=True)
        best_box_uplink_df = box_uplink_df.groupby('设施名称').first().reset_index()

        box_level_df = point_df[(point_df['级别']<=2) & ((point_df['类型']=='光交箱') | (point_df['类型']=='分纤箱'))].copy()
        box_level_df = box_level_df.rename(columns={'分纤点名称':'设施名称'})

        box_level_uplink_df = box_level_df.merge(best_box_uplink_df,on='设施名称',how='left')
        box_level_uplink_df['上联紧张'] = box_level_uplink_df['最小空闲芯数'].apply(lambda x: '是' if x <= 2 else '否')

        site_df = readDataBase('站点')
        site_df = site_df[['站点名称','所属区县']].rename(columns={'站点名称':'所属站点','所属区县':'所属区县'})

        box_df_full = readDataBase('光交箱')
        oBox_df_full = readDataBase('分纤箱')
        all_box_df = pd.concat([box_df_full[['设施名称','所属站点']],oBox_df_full[['设施名称','所属站点']]],ignore_index=True)

        box_level_uplink_df = box_level_uplink_df.merge(all_box_df,on='设施名称',how='left')
        box_level_uplink_df = box_level_uplink_df.merge(site_df,on='所属站点',how='left')
        box_level_uplink_df['所属区县'] = box_level_uplink_df['所属区县'].fillna('未知')

        box_level_uplink_df['级别名称'] = box_level_uplink_df['级别'].apply(lambda x: '一级' if x == 1 else '二级')

        level_grp = box_level_uplink_df.groupby(['所属区县','级别名称','类型']).agg(
            箱体数=('设施名称','count'),
            上联紧张数=('上联紧张',lambda x: (x=='是').sum())
        ).reset_index()

        level_grp['上联紧张比例'] = level_grp['上联紧张数'] / level_grp['箱体数']
        level_grp['上联紧张比例'] = level_grp['上联紧张比例'].apply(lambda x: f'{x*100:.2f}%')

        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with pd.ExcelWriter(f'{self.dir_path}/一二级箱体上联紧张分析{dt}.xlsx') as writer:
            box_level_uplink_df.to_excel(writer,sheet_name='一二级箱体上联紧张清单',index=False)
            level_grp.to_excel(writer,sheet_name='区县级别箱体统计',index=False)
        
        self.state_signal.emit(f'已完成一二级箱体上联紧张分析，共分析{box_level_uplink_df.shape[0]}个箱体')