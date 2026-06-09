# 分析OLT网元端口情况

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re

class AnalysisOltPortThread(QThread):
    state_signal = Signal(str,int,str) # 当前进度情况、百分比、预估完成时间

    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            conn = sqlite3.connect('data/transportNetwork.db')
            sql = """
            SELECT o.*,j.所属站点,j.业务级别 AS 机房类型,j.生命周期状态 AS 机房状态,j.产权单位 AS 产权单位
            FROM OLT网元 o
            JOIN 机房 j ON o.所属机房 = j.机房名称
            """
            olt_df = pd.read_sql_query(sql, conn)
            self.state_signal.emit(f"查询OLT网元清单完成，共{len(olt_df)}条",20,"")
            
            pon_df = pd.read_sql_query("SELECT * FROM PON端口", conn)
            self.state_signal.emit(f"查询PON端口清单完成，共{len(pon_df)}条",30,"")
            
            hw_df = pd.read_sql_query("SELECT * FROM 华为PON单板", conn)
            self.state_signal.emit(f"查询华为PON单板完成，共{len(hw_df)}条",35,"")
            
            zte_df = pd.read_sql_query("SELECT * FROM 中兴PON单板", conn)
            conn.close()
            self.state_signal.emit(f"查询中兴PON单板完成，共{len(zte_df)}条",40,"")
            
            pon_df = self.analysisOltPort(pon_df,hw_df,zte_df)
            self.state_signal.emit(f"分析PON端口清单完成，共{len(pon_df)}条",60,"")
            
            writeDataBase('PON口数据集',pon_df)
            self.state_signal.emit(f"写入PON口数据集完成",65,"")
            
            pon_table = self.ponTable(pon_df)
            self.state_signal.emit(f"统计PON端口清单完成，共{len(pon_table)}个OLT",80,"")
            
            # 生成PON板分析表
            board_df = hw_df.copy()
            board_df = board_df.rename(columns={'所属网元':'OLT网元','单板类型':'板卡类型','单板状态':'板卡状态'})
            zte_df_copy = zte_df.copy()
            zte_df_copy['槽位'] = zte_df_copy['板卡槽位'].apply(lambda x: int(str(x).split('-')[2]) if pd.notnull(x) else 0)
            zte_df_copy['板卡名称'] = zte_df_copy.apply(lambda row: self.stardBoard(row['网元名称'], row['槽位']), axis=1)
            zte_df_copy = zte_df_copy[['板卡名称','板卡状态','板卡类型']]
            board_df['板卡名称'] = board_df.apply(lambda row: self.stardBoard(row['OLT网元'], row['槽位号']), axis=1)
            board_df = board_df[['板卡名称','板卡状态','板卡类型']]
            board_df = pd.concat([board_df, zte_df_copy])
            board_df['板卡状态'] = board_df['板卡状态'].apply(self.fixState)
            
            pon_board_table = self.ponBoardTable(pon_df, board_df)
            writeDataBase('PON板分析表', pon_board_table)
            self.state_signal.emit(f"生成PON板分析表完成，共{len(pon_board_table)}条",85,"")
            
            olt_df = olt_df.rename(columns={'网元名称':'OLT网元'})
            olt_df = olt_df.merge(pon_table,on='OLT网元',how='left')
            olt_df = olt_df.fillna(0)
            
            olt_df['业务槽数量'] = olt_df['设备型号'].apply(self.srvBoardNum)
            olt_df['空闲业务槽数量'] = olt_df['业务槽数量'] - olt_df['业务槽占用数']
            
            olt_df['是否千兆'] = olt_df['设备型号'].apply(lambda x: '是' if 'MA5800' in str(x) or 'C600' in str(x) else '否')
            
            olt_df['闲置OLT'] = self.isNotUseOlt(olt_df['PON口总数'], olt_df['PON口空闲数'])
            
            writeDataBase('OLT网元数据集',olt_df)
            self.state_signal.emit(f"统计OLT网元及端口清单完成，共{len(olt_df)}条",100,"")

        except Exception as e:
            self.state_signal.emit(f"查询失败: {str(e)}",0,"")

    def ponTable(self,pon_df):
        pon_df = pon_df[pon_df['PON口类型'] != '非PON口']
        #数据透视表统计PON口数量
        pon_table = pd.pivot_table(pon_df,index=['OLT网元'],columns=['端口状态'],aggfunc={'端口名称':'count'},fill_value=0)
        pon_table.columns = pon_table.columns.droplevel()
        pon_table = pon_table.reset_index()
        pon_table['PON口使用数'] = pon_table['占用'] + pon_table['预占']
        pon_table.rename(columns={'空闲':'PON口空闲数'},inplace=True)
        pon_table = pon_table[['OLT网元','PON口使用数','PON口空闲数']]
        
        #数据透视表统计千兆PON口数量
        xg_pon_df = pon_df[pon_df['PON口类型']=='千兆'].copy()
        xg_pon_table = pd.pivot_table(xg_pon_df,index=['OLT网元'],columns=['端口状态'],aggfunc={'端口名称':'count'},fill_value=0)
        xg_pon_table.columns = xg_pon_table.columns.droplevel()
        xg_pon_table = xg_pon_table.reset_index()
        xg_pon_table['XGPON口使用数'] = xg_pon_table['占用'] + xg_pon_table['预占'] 
        xg_pon_table.rename(columns={'空闲':'XGPON口空闲数'},inplace=True)
        xg_pon_table = xg_pon_table[['OLT网元','XGPON口使用数','XGPON口空闲数']]

        # 统计用户数
        user_table = pd.pivot_table(pon_df,index=['OLT网元'],aggfunc={'PON口下挂用户数':'sum'},fill_value=0)
        user_table.rename(columns={'PON口下挂用户数':'用户数'},inplace=True)

        # 统计业务槽占用数
        board_df = pon_df[['OLT网元','板卡名称']].copy()
        board_df = board_df.drop_duplicates(subset=['板卡名称'])
        board_df['是否业务板'] = board_df['板卡名称'].apply(self.isSrvBoard)
        board_df = board_df[board_df['是否业务板'] == '是']
        
        if not board_df.empty:
            board_table = pd.pivot_table(board_df,index=['OLT网元'],aggfunc={'板卡名称':'count'},fill_value=0)
            board_table = board_table.reset_index()
            board_table.rename(columns={'板卡名称':'业务槽占用数'},inplace=True)
        else:
            board_table = pd.DataFrame({'OLT网元': pon_df['OLT网元'].unique(), '业务槽占用数': 0})

        # 合并表格
        pon_table = pon_table.merge(xg_pon_table,on='OLT网元',how='left')
        pon_table = pon_table.merge(user_table,on='OLT网元',how='left')
        pon_table = pon_table.merge(board_table,on='OLT网元',how='left')
        pon_table['PON口总数'] = pon_table['PON口使用数'] + pon_table['PON口空闲数']
        pon_table['XGPON口总数'] = pon_table['XGPON口使用数'] + pon_table['XGPON口空闲数']
        pon_table['业务槽占用数'] = pon_table['业务槽占用数'].fillna(0)
        pon_table = pon_table.fillna(0)
        pon_table = pon_table[['OLT网元','PON口总数','PON口使用数','PON口空闲数','XGPON口总数','XGPON口使用数','XGPON口空闲数','用户数','业务槽占用数']]
        return pon_table
    
    def srvBoardNum(self, devType):
        if 'MA5800-X17' in devType:
            return 17
        elif 'MA5680T' in devType:
            return 16
        elif 'MA5800-X7' in devType:
            return 7
        elif 'MA5683T' in devType:
            return 6
        elif 'C320' in devType:
            return 4
        elif 'C300' in devType:
            return 16
        elif 'C600' in devType:
            return 16
        else:
            return 0
    
    def isSrvBoard(self, boardName):
        if '5800-X17' in boardName:
            board_ids = ['9', '10']
        elif '5800-X7' in boardName:
            board_ids = ['8', '9']
        elif '5680' in boardName:
            board_ids = ['9','10','19', '20']
        elif '600' in boardName:
            board_ids = ['10', '11']
        elif '320' in boardName:
            board_ids = ['3', '4']
        elif '300' in boardName:
            board_ids = ['10','11','19','20']
        elif '5683' in boardName:
            board_ids = ['6','7','8','9']
        else:
            return '否'
        match = re.search(' (\d+)槽', boardName)
        if match:
            board_id = match.group(1)
            if board_id in board_ids:
                return '否'
        return '是'
    
    def ponBoardTable(self, pon_df, board_df):
        '''
        分析PON板空闲情况占用情况
        '''
        pon_df = pon_df[pon_df['PON口类型'] != '非PON口']
        
        not_use_table = pd.pivot_table(pon_df, index=['OLT网元', '板卡名称'], 
                                        columns=['端口状态'], 
                                        aggfunc={'端口名称': 'count'}, 
                                        fill_value=0)
        not_use_table.columns = not_use_table.columns.droplevel()
        not_use_table = not_use_table.reset_index()
        not_use_table = not_use_table.merge(board_df, on='板卡名称', how='left')
        
        not_use_table['是否千兆'] = not_use_table['板卡类型'].apply(self.isXgPonPort2)
        not_use_table['是否在用'] = not_use_table.apply(lambda row: self.isNotUse(row['占用'], row['预占']), axis=1)
        
        not_use_table['端口数量'] = not_use_table['占用'] + not_use_table['预占'] + not_use_table['空闲']
        not_use_table['在用端口数'] = not_use_table['占用'] + not_use_table['预占']
        not_use_table['设备系列'] = not_use_table['OLT网元'].apply(self.fixDevType)
        
        not_use_table.rename(columns={'OLT网元': '本地名称'}, inplace=True)
        
        return not_use_table
    
    def isXgPonPort2(self, boardType):
        if pd.isnull(boardType):
            return '否'
        boardType = str(boardType)
        if 'CG' in boardType:
            return '是'
        elif 'GFBT' in boardType or 'VSCP' in boardType:
            return '是'
        else:
            return '否'
    
    def isNotUse(self, use, need):
        if use == 0 and need == 0:
            return '否'
        else:
            return '是'
    
    def isNotUseOlt(self, ponNum, useNum):
        try:
            if int(ponNum) == int(useNum):
                return '是'
            else:
                return '否'
        except Exception:
            return '否'
    
    def fixDevType(self, devType):
        if pd.isnull(devType):
            return '-'
        devType = str(devType)
        if 'MA58' in devType:
            return 'MA58系列'
        elif 'MA56' in devType:
            return 'MA56系列'
        elif 'C600' in devType:
            return 'C600系列'
        elif 'C3' in devType:
            return 'C300系列'
        else:
            return '-'

    # 清洗PON端口数据
    def analysisOltPort(self,pon_df,hw_df,zte_df):
        #所属传输网元(TEXT), 端口名称(TEXT), PONID(TEXT), 端口状态(TEXT), PON口下挂用户数(INTEGER), 端口子类型(TEXT)
        pon_df = pon_df.rename(columns={'所属传输网元':'OLT网元'})
        # 所属网元(TEXT), 槽位号(INTEGER), 单板类型(TEXT), 单板状态(TEXT)
        hw_df = hw_df.rename(columns={'所属网元':'OLT网元','单板类型':'板卡类型','单板状态':'板卡状态'})
        # 网元名称(TEXT), 板卡槽位(TEXT), 板卡类型(TEXT), 板卡状态(TEXT)
        zte_df = zte_df.rename(columns={'网元名称':'OLT网元','板卡槽位':'槽位号'})
        zte_df['槽位'] = zte_df['槽位号'].apply(lambda x: int(x.split('-')[2]))
        standBoard_vec = np.vectorize(self.stardBoard)
        zte_df['板卡名称'] = standBoard_vec(zte_df['OLT网元'],zte_df['槽位'])
        zte_df['板卡状态'] = zte_df['板卡状态'].apply(self.fixState)
        zte_df = zte_df[['板卡名称','板卡状态','板卡类型']]
        hw_df['板卡名称'] = standBoard_vec(hw_df['OLT网元'],hw_df['槽位号'])
        # 重定义板卡状态
        hw_df['板卡状态'] = hw_df['板卡状态'].apply(self.fixState)
        hw_df = hw_df[['板卡名称','板卡状态','板卡类型']]
        board_df = pd.concat([zte_df,hw_df])
        pon_df['槽位号'],pon_df['端口号'] = zip(*pon_df['PONID'].apply(self.splitPonId))
        pon_df['板卡名称'] = standBoard_vec(pon_df['OLT网元'],pon_df['槽位号'])
        pon_df = pon_df.merge(board_df,on='板卡名称',how='left')
        pon_df['板卡状态'] = pon_df['板卡状态'].fillna('不在位')
        pon_df['PON口类型'] = pon_df['端口子类型'].apply(self.isPonPort)
        pon_df = pon_df[pon_df['板卡状态'] == '在位']
        pon_df.drop(columns=['板卡状态','端口子类型','PONID'],inplace=True)
        return pon_df

    def splitPonId(self,pon_id):
        if pon_id:
            parts = pon_id.split('-')
            if len(parts) >=3:
                return int(parts[-2]),int(parts[-1])
        return 100,100

    def stardBoard(self,olt_name,slot):
        return olt_name + ' ' + str(slot) + '槽'
    
    #重定义板卡状态
    def fixState(self,state):
        if state == '正常':
            return '在位'
        elif state == '在线':
            return '在位'
        elif state == '离线':
            return '不在位'
        else:
            return state
    
    def isPonPort(self,sub_type):
        if sub_type == 'GPON':
            return '普通'
        elif sub_type == 'GPON_XGPON' or sub_type == 'GPON_XGSPON' or sub_type == 'XGPON':
            return '千兆'
        return '非PON口'
    

# 箱体上联方案分析