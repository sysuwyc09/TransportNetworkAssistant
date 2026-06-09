'''
机房箱体分纤点级别定义业务逻辑
直连纤芯需要12芯以上，二级分纤点机房为本地接入；
1、汇聚机房：一级分纤点
2、直达一级机房：576以上【光交箱】：一级分纤点
3、OLT机房：一级分纤点
4、直达一级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点
5、直达二级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点；循环次数4次
6、集群光交箱：就高的箱体级别
7、归属机房的光交箱、分纤箱：按照机房的分纤点级别
'''

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class BoxLevelThreadV2(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
    
    def run(self):
        if self.fileNotRequired():
            return;
        house_df = readDataBase('机房')
        olt_df = readDataBase('OLT网元')
        self.state_signal.emit('正在分析一级分纤点机房...')
        aggr_house_df,olt_house_df = self.houseLevel(house_df,olt_df)
        line_df = readDataBase('中继段')
        box_df = readDataBase('光交箱')
        oBox_df = readDataBase('分纤箱')
        box_grp_df = readDataBase('集群管理')
        self.state_signal.emit(f'已完成机房分析。')
        point_df = self.getLevel(house_df,aggr_house_df,olt_house_df,line_df,box_df,oBox_df,box_grp_df)
        self.state_signal.emit('正在生成分析表格...')
        point_df.to_excel(self.file_path,index=False)
        self.state_signal.emit('已完成！')

    def fileNotRequired(self):
        # 校验数据库表格需求文件是否存在
        self.state_signal.emit('正在校验数据库表格')
        needs_files = ['OLT网元','机房','光交箱','分纤箱','中继段','集群管理']
        # 查看data\transportNetwork.db是否存在这些表
        conn = sqlite3.connect('data/transportNetwork.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        for table in needs_files:
            if table not in tables:
                self.error_signal.emit(f'数据库表格中不存在{table}表')
                return True
        return False

    def houseLevel(self,house_df,olt_df):
        # step 1 OLT机房和汇聚机房定义为一级分纤点
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

    def getLevel(self,house_df,aggr_house_df,olt_house_df,line_df,box_df,oBox_df,box_grp_df):
        '''
        本地接入机房、箱体分纤箱级别定义逻辑
        1、直连纤芯需要12芯以上；机房为本地接入，不含退网态；
        2、直达一级机房：288以上GJ：一级分纤点【光交箱】
        3、直达一级分纤点的设施：定义为二级分纤点【光交箱+96芯以上分纤箱+本地接入机房】
        4、直达二级分纤点的设施：定义为二级分纤点【光交箱+96芯以上分纤箱+本地接入机房】；循环次数4次
        5、集群光交箱：就高的箱体级别
        '''
        line_df = line_df[['名称','中继纤芯数量','始端机房','终端机房','始端设施','终端设施']]
        line_df = line_df[line_df['中继纤芯数量']>=12]

        line_df2 = line_df.copy().rename(columns={'始端机房':'终端机房','终端机房':'始端机房','始端设施':'终端设施','终端设施':'始端设施'})
        line_df = pd.concat([line_df,line_df2],ignore_index=True)

        # 判断直达一级机房的接入机房及光交设施；
        temp_df = aggr_house_df[['分纤点名称']].copy().rename(columns={'分纤点名称':'始端机房'})
        link_to_level1_house = line_df.merge(temp_df,on='始端机房')

        # 判断直达一级机房的576以上光交箱；
        box_576up_df = box_df[box_df['容量']>=576].copy()
        box_576up_df = box_576up_df[['设施名称','容量']].rename(columns={'设施名称':'终端设施'})
        first_box = link_to_level1_house.merge(box_576up_df,on='终端设施')
        first_box = first_box[['终端设施','始端机房','容量']].drop_duplicates(subset=['终端设施'],keep='first').rename(columns={'终端设施':'分纤点名称'})
        first_box['级别'] = 1
        first_box['类型'] = '光交箱'
        first_box['细分'] = '直达汇聚:' + first_box['始端机房']
        step_1_box = first_box[['分纤点名称','级别','细分','类型','容量']].drop_duplicates()
        point_df = pd.concat([aggr_house_df,olt_house_df,step_1_box],ignore_index=True)

        # 集群分析
        point_df = self.boxGrpLevel(box_grp_df,point_df)
        self.state_signal.emit(f'已完成一级分纤点分析，已分析{point_df.shape[0]}个分纤点')

        # 所有接入设施
        all_dev_df,house_box_df = self.getAllDev(house_df,box_df,oBox_df)
        line_df['始端'] = fixSite(line_df['始端机房'],line_df['始端设施'])
        line_df['终端'] = fixSite(line_df['终端机房'],line_df['终端设施'])
        line_df = line_df[['始端','终端']]

        # 循环分析直连一级及二级的设施及箱体
        run_flag = True
        run_count = 1
        current_shape = point_df.shape[0]
        while run_flag:
            # 未纳入分级的设施,分析直连一级的设施及箱体
            not_level_df = self.notLevelDev(all_dev_df,point_df)
            point_df = self.findDevLevel(not_level_df,point_df,line_df,run_count)
            self.state_signal.emit(f'完成第{run_count}轮二级的设施及箱体分析，已分析{point_df.shape[0]}个分纤点')
            if point_df.shape[0] == current_shape:
                run_flag = False
            else:
                current_shape = point_df.shape[0]
                run_count += 1
            point_df = self.boxGrpLevel(box_grp_df,point_df)
            if run_count > 4:
                run_flag = False
        # 归属机房的箱体按机房级别定义：
        point_df = self.houseBoxLevel(house_box_df,point_df)
        # 未纳入分级的设施；定义为级别3
        not_level_df = self.notLevelDev(all_dev_df,point_df)
        # not_level_df = not_level_df[not_level_df['设施类型']!='本地接入']
        not_level_df = not_level_df.rename(columns={'设施类型':'类型'})
        not_level_df['级别'] = 3
        not_level_df['细分'] = '未纳入分级的设施'
        point_df = pd.concat([point_df,not_level_df],ignore_index=True)
        return point_df

    def houseBoxLevel(self,house_box_df,point_df):
        '''
        归属到机房的箱体的级别，按照机房的级别进行定义
        '''
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

    def boxGrpLevel(self,box_grp_df,point_df):
        '''
        集群管理：
        1、集群光交箱：就高的箱体级别
        '''
        box_grp_df = box_grp_df.rename(columns={'设备名称':'分纤点名称'})
        # 将匹配哪些无级别的分纤点
        box_grp_df = box_grp_df.merge(point_df,on='分纤点名称',how='left')
        box_grp_df['级别'] = box_grp_df['级别'].fillna(3)
        not_level_box_grp = box_grp_df[box_grp_df['级别']==3]
        if not_level_box_grp.empty:
            return point_df
        box_min_level = box_grp_df.groupby('集群列表')['级别'].min().reset_index().rename(columns={'级别':'最高级别'})
        box_grp_df = box_grp_df.merge(box_min_level,on='集群列表',how='left')
        # 获取最高级别的分纤点名称
        best_box = box_grp_df[box_grp_df['级别']==box_grp_df['最高级别']]
        best_box = best_box.drop_duplicates(subset=['集群列表'],keep='first')[['集群列表','分纤点名称','最高级别']].rename(columns={'分纤点名称':'最高级别的分纤点名称'})
        not_level_box_grp = not_level_box_grp.merge(best_box,on='集群列表',how='left')        
        # 未纳入1,2级的清单
        not_level_box_grp  = not_level_box_grp[not_level_box_grp['最高级别']<3]
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

    def findDevLevel(self,not_level_df,point_df,line_df,run_count):
        '''根据line_df判断level2的接入设施'''
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

    def notLevelDev(self,dev_df,point_df):
        '''分析未有级别的分纤点设施'''
        temp_df = point_df[['分纤点名称','级别']]
        not_level_dev = dev_df.merge(temp_df,on='分纤点名称',how='left')
        not_level_dev = not_level_dev[not_level_dev['级别'].isnull()][['分纤点名称','设施类型','容量']]
        not_level_dev = not_level_dev.drop_duplicates()
        return not_level_dev
    
    def getAllDev(self,house_df,box_df,oBox_df):
        '''
        汇总所有接入点设施：
        1、业务级别为本地接入，非退网态的机房；
        2、96芯以上的光交箱；
        3、96芯以上的分纤箱
        '''
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



# 知识库相关进程
'''
OLT 站点知识库的进程，读取OLT表格，然后获取OLT的markdown格式文档
'''