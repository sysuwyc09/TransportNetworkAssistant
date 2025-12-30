# 公共线程模块,Pyside6 QThread
from PySide6.QtCore import QThread
from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from publicFunc import *
import time
import re

class CheckTableThread(QThread):
    tableReady = Signal(str)  # 信号：表名和查询结果
    resultReady = Signal(bool)  # 信号：表名和查询结果
    
    def __init__(self, analysis_type, parent=None):
        super().__init__(parent)
        self.analysis_type = analysis_type
    
    def run(self):
        # 根据分析类型确定需要检查的表格
        tables_to_check = self.get_tables_for_analysis()
        is_check = True
        try:
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            # 检查每个表格是否存在并查询数据
            for table in tables_to_check:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if cursor.fetchone():
                    # 表格存在，查询数据表的列数，行数
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    # 表格存在，查询数据表的行数
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    row_count = cursor.fetchone()[0]
                    self.tableReady.emit(table + f': 表格校验通过, 列数: {len(columns)}, 行数: {row_count}')
                else:
                    if table == '光交上联方案集':
                        self.tableReady.emit(table + ': 不存在这个表格,请先执行光设施分析')
                    else:
                        self.tableReady.emit(table + '：不存在这个表格，请先在资源数据中导入表格')
                    self.resultReady.emit(False)
                    is_check = False
            if is_check:
                self.resultReady.emit(True)
        except Exception as e:
            self.tableReady.emit(f'数据库操作错误: {e}')
            self.resultReady.emit(False)
        finally:
            conn.close()
    
    def get_tables_for_analysis(self):
        """根据分析类型返回需要检查的表格列表"""
        if self.analysis_type == "光设施":
            return ["OLT网元","机房", "中继段",'光交箱','分纤箱']
        elif self.analysis_type == "OLT端口":
            return ['OLT网元', 'PON端口', '机房', '华为PON单板','中兴PON单板']
        elif self.analysis_type == "主光路":
            return ['主光路', '光交上联方案集']



class ImportFileThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号
    result_signal = Signal(pd.DataFrame)  # 列名和数据信号
    
    def __init__(self, file_path, table_name):
        super().__init__()
        self.file_path = file_path
        self.table_name = table_name
    
    def run(self):
        try:
            self.state_signal.emit("正在读取文件,请稍后...")
            # 读取文件到DataFrame
            df = pd.read_excel(self.file_path)
            if self.table_name == '中继段':
                self.convertLine(df)
            # 发送状态信号
            self.state_signal.emit("导入成功,请选择对应文件列")
            # 发送结果信号
            self.result_signal.emit(df)
        except Exception as e:
            self.state_signal.emit(f"导入失败: {str(e)}")
            self.result_signal.emit([], [])

    def convertLine(self,df):
        value_vars = df.columns.tolist()[16:]
        result = df.melt(id_vars=['名称'], value_vars=value_vars,value_name='光缆段').drop(columns=['variable'])  # 移除不需要的variable列
        # 重置索引
        result = result.reset_index(drop=True)
        result = result[result['光缆段'].notnull()]
        result.rename(columns={'名称':'中继段'},inplace=True)
        writeDataBase('中继段至光缆段',result)

class UpdateDBThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号

    
    def __init__(self, table_name,df):
        super().__init__()
        self.df = df
        self.table_name = table_name
    
    def run(self):
        try:
            self.state_signal.emit('正在清洗数据')
            self.selectData()
            self.state_signal.emit('正在更新数据库数据')
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            self.df.to_sql(self.table_name, conn, if_exists='replace', index=False)
            # 更新 表格更新时间 表 table_name的更新时间 为当前时间
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M')
            # 判断表格是否存在并执行更新或插入操作
            cursor.execute("SELECT COUNT(*) FROM 表格更新时间 WHERE 表名=?", (self.table_name,))
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE 表格更新时间 SET 更新时间=? WHERE 表名=?", (now, self.table_name))
            else:
                cursor.execute("INSERT INTO 表格更新时间 (表名, 更新时间) VALUES (?, ?)", (self.table_name, now))
            conn.commit()
            conn.close()
            self.state_signal.emit("更新成功")
        except Exception as e:
            self.state_signal.emit(f"更新失败: {str(e)}")

    def selectData(self):
        if self.table_name == 'OLT网元':
            self.selectOLT()

    def selectOLT(self):
        self.df = self.df.astype(str)
        # 删除 生命周期状态列 包含 退网 的行
        self.df = self.df[~self.df['生命周期状态'].str.contains('退网')]
        # 删除 生命周期状态列 为 工程无业务 的行
        self.df = self.df[self.df['生命周期状态']!='工程无业务']
        # 删除 生命周期状态列 为 工程在建 的行
        self.df = self.df[self.df['生命周期状态']!='工程在建']

# 下载文件线程
class downloadThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号
    
    def __init__(self, table_names, dfs,file_path):
        super().__init__()
        self.table_names = table_names
        self.dfs = dfs
        self.file_path = file_path
    
    def run(self):
        try:
            self.state_signal.emit("正在导出文件,请稍后...")
            # 下载表格数据实现
            with pd.ExcelWriter(self.file_path) as writer:
                for table_name, df in zip(self.table_names, self.dfs):
                    df.to_excel(writer, sheet_name=table_name, index=False)
            self.state_signal.emit("导出成功！")
        except Exception as e:
            self.state_signal.emit(f"导出失败: {str(e)}")

# 查询数据库 存在的表格清单 ，匹配最后更新时间， 列名及类型，行数
class DatabaseInfoThread(QThread):
    resultReady = Signal(pd.DataFrame)
    state_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            self.state_signal.emit("正在查询数据库,请稍后...")
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            # 获取所有表格名称
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            data = []
            for table in tables:
                # 获取表格最后更新时间
                cursor.execute(f"SELECT 更新时间 FROM 表格更新时间 WHERE 表名='{table}'")
                update_time = cursor.fetchone()
                update_time = update_time[0] if update_time else '未知'
                # 获取列名和类型
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                columns_info = ', '.join([f"{col[1]}({col[2]})" for col in columns])
                # 获取行数
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                data.append({
                    '表名': table,
                    '列名及类型': columns_info,
                    '行数': row_count,
                    '最后更新时间': update_time,
                })
            conn.close()
            df = pd.DataFrame(data)
            self.resultReady.emit(df)
            self.state_signal.emit("查询完成")
        except Exception as e:
            self.state_signal.emit(f"查询失败: {str(e)}")

# 分析OLT网元端口情况
class AnalysisOltPortThread(QThread):
    state_signal = Signal(str,int,str) # 当前进度情况、百分比、预估完成时间

    def __init__(self):
        super().__init__()
    
    def run(self):
        # try:
        conn = sqlite3.connect('data/transportNetwork.db')
        # 查询 OLT网元 表 匹配 机房 表，on 
        sql = """
        SELECT o.*,j.所属站点,j.业务级别 AS 机房类型,j.生命周期状态 AS 机房状态
        FROM OLT网元 o
        JOIN 机房 j ON o.所属机房 = j.机房名称
        """
        olt_df = pd.read_sql_query(sql, conn)
        self.state_signal.emit(f"查询OLT网元清单完成",20,"")
        pon_df = pd.read_sql_query("SELECT * FROM PON端口", conn)
        hw_df = pd.read_sql_query("SELECT * FROM 华为PON单板", conn)
        zte_df = pd.read_sql_query("SELECT * FROM 中兴PON单板", conn)
        conn.close()
        self.state_signal.emit(f"查询PON端口清单完成",40,"")
        pon_df = self.analysisOltPort(pon_df,hw_df,zte_df)
        self.state_signal.emit(f"分析PON端口清单完成",60,"")
        writeDataBase('PON口数据集',pon_df)
        pon_table = self.ponTable(pon_df)
        self.state_signal.emit(f"统计PON端口清单完成",80,"")
        olt_df = olt_df.rename(columns={'网元名称':'OLT网元'})
        olt_df = olt_df.merge(pon_table,on='OLT网元',how='left')
        olt_df = olt_df.fillna(0)
        writeDataBase('OLT网元数据集',olt_df)
        self.state_signal.emit(f"统计OLT网元及端口清单完成",100,"")

        # except Exception as e:
        #     self.state_signal.emit(f"查询失败: {str(e)}",0,"")

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

        # 合并三个表格
        pon_table = pon_table.merge(xg_pon_table,on='OLT网元',how='left')
        pon_table = pon_table.merge(user_table,on='OLT网元',how='left')
        pon_table['PON口总数'] = pon_table['PON口使用数'] + pon_table['PON口空闲数']
        pon_table['XGPON口总数'] = pon_table['XGPON口使用数'] + pon_table['XGPON口空闲数']
        pon_table = pon_table.fillna(0)
        pon_table = pon_table[['OLT网元','PON口总数','PON口使用数','PON口空闲数','XGPON口总数','XGPON口使用数','XGPON口空闲数','用户数']]
        return pon_table


    
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
        elif sub_type == 'GPON_XGPON' or sub_type == 'GPON_XGSPON':
            return '千兆'
        return '非PON口'
    

# 箱体上联方案分析
class BoxUpLineThread(QThread):
    state_signal = Signal(str,int,str)
    def __init__(self):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(BoxUpLineThread, self).__init__()

    def run(self):
        self.state_signal.emit('正在加载中继段信息，请稍后...',0,'')
        self.line_df = loadLine2Df()
        self.state_signal.emit('正在加载全量光交设施...',0,'')
        self.all_dev = readDevs()
        self.state_signal.emit('已加载全量光交设施...',0,'')
        self.all_dev.rename(columns={'机房名称':'设施所属机房','业务区':'设施所属业务区'},inplace=True)
        self.all_dev['设施所属位置'] = fixSite(self.all_dev['设施所属机房'],self.all_dev['设施名称'])
        obds = list(set(list(self.all_dev['设施所属位置'])))
        self.state_signal.emit(f'已查询到{len(obds)}个光交设施...',0,'')
        # 按500一组进行分组，如果最后一组不足500则为剩余值
        obds_groups = [obds[i:i+500] for i in range(0, len(obds), 500)]
        result_dfs = []
        start_time = time.time()
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToOlt(obds_group,self.line_df)
            if temp_df.shape[0] > 0:
                temp_df = selectBestPath(temp_df)
            result_dfs.append(temp_df)
            # 计算预估剩余时间
            elapsed_time = time.time() - start_time
            avg_time_per_group = elapsed_time / (i+1)
            remaining_groups = len(obds_groups) - (i+1)
            estimated_time = avg_time_per_group * remaining_groups
            self.state_signal.emit(f'已完成{i+1}/{len(obds_groups)}组光设施跳纤分析,',90/len(obds_groups)*(i+1),f'剩余约{int(estimated_time/60)}分{int(estimated_time%60)}秒')
        result_df = pd.concat(result_dfs)
        self.state_signal.emit(f'已完成调度方案输出',90,'')
        if result_df.shape[0] == 0:
            self.state_signal.emit('查询不到上联方案')
            return
        odevs = self.all_dev[['设施名称','设施所属位置']]
        result_df = result_df.rename(columns={'A端':'设施所属位置','B端':'目标OLT机房'})
        result_df.drop(['B端类型'],axis=1,inplace=True)
        odevs = odevs.merge(result_df,on='设施所属位置',how='left')
        writeDataBase('箱体上联OLT跳纤路径表', odevs)
        self.state_signal.emit('已完成...',100,'')


# 箱体上联纤芯紧张状态分析
class BusyBoxUplinkThread(QThread):
    state_signal = Signal(str)
    def __init__(self,dir_path):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super().__init__()
        self.dir_path = dir_path
    
    def run(self):
        try:
            self.state_signal.emit('正在加载全量箱体上联OLT机房...')
            box_uplink_df = readDataBase('箱体上联OLT跳纤路径表')
            if box_uplink_df.shape[0] == 0:
                self.state_signal.emit('查询不到箱体上联方案,请先运行箱体上联方案分析...')
                return
            self.busyBoxUplink(box_uplink_df)
            self.state_signal.emit('已完成...')
        except Exception as e:
            self.state_signal.emit('分析箱体上联纤芯紧张状态失败:' + str(e))

    def busyBoxUplink(self,box_uplink_df):
        # 根据评分选取最优方案
        box_uplink_df.sort_values(by=['设施名称','方案得分'],ascending=[True,False],inplace=True)
        best_box_uplink_df = box_uplink_df.groupby('设施名称').first().reset_index()
        all_red_uplink_df = best_box_uplink_df[best_box_uplink_df['最小空闲芯数'] <=6]
        box_df = readDataBase('光交箱')[['设施名称','容量']]
        box_red_uplink_df = all_red_uplink_df.merge(box_df,on='设施名称')
        box_red_uplink_df = box_red_uplink_df[box_red_uplink_df['容量'] >= 288]
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
        line_df = line_df[line_df['空闲芯数'] <= 6]
        line_table = pd.pivot_table(line_df,index=['中继段'],aggfunc={'设施名称':'count'})
        line_table.rename(columns={'设施名称':'影响288以上光交箱数'},inplace=True)
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
        with pd.ExcelWriter(f'{self.dir_path}/箱体上联纤芯紧张分析{dt}.xlsx') as writer:
            best_box_uplink_df.to_excel(writer,sheet_name='所有箱体上联最优方案',index=False)
            box_red_uplink_df.to_excel(writer,sheet_name='288以上光交箱上联纤芯紧张状态',index=False)
            result_df.to_excel(writer,sheet_name='288以上光交箱紧张中继段详细',index=False)
            fiber_df.to_excel(writer,sheet_name='288以上光交箱紧张光缆段详细',index=False)


# 查找中继段资源的类
#名称(TEXT), 长度(REAL), 空闲数量(REAL), 占用数量(REAL), 中继纤芯数量(REAL), 始端站点(TEXT), 终端站点(TEXT), 始端机房(TEXT), 终端机房(TEXT), 始端设施(TEXT), 终端设施(TEXT)
class FindRelayLineThread(QThread):
    state_signal = Signal(str)
    result_signal = Signal(pd.DataFrame)
    def __init__(self,parent=None,keywords=[]):
        super().__init__(parent)
        self.keywords = keywords
        self.cols = ['名称','长度','中继纤芯数量','占用数量','空闲数量','始端机房','终端机房']
    
    def run(self):
        try:
            self.state_signal.emit('正在查找中继段资源，请稍后...')
            lines = readDataBase('中继段')
            lines = lines[lines['中继纤芯数量'] > 0]
            lines['长度'] = round(lines['长度']/1000,2)
            lines = lines.astype({'名称':str,'始端机房':str,'终端机房':str,'中继纤芯数量':int,'占用数量':int,'空闲数量':int})
            lines['查找项'] = lines['名称'] + lines['始端机房'] + lines['终端机房']
            result_df = lines[lines['查找项'].apply(lambda x: self.search(x,self.keywords))]
            result_df = result_df[self.cols]
            result_df.sort_values(by=['中继纤芯数量'],ascending=[False],inplace=True)
            result_df =result_df.reset_index(drop=True)
            self.result_signal.emit(result_df)
            self.state_signal.emit('查找完成')
        except Exception as e:
            self.state_signal.emit('查找中继段资源失败:' + str(e))
    
    def search(self,text,keywords=[]):
        for keyword in keywords:
            if keyword not in text:
                return False
        return True
    

# 查找端口不足的OLT站点
class FindRedOltPortSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','全量PON口数量','空闲PON口数量','PON口利用率','千兆PON口数量','空闲千兆PON口数量','千兆PON口利用率','是否有端口不足']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析存在端口不足的OLT站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            olt_count = pd.pivot_table(df,index=['所属站点','设备型号'],aggfunc={'OLT网元':'count'})
            olt_count.columns = ['OLT网元数量']
            olt_count = olt_count.reset_index()
            olt_count = olt_count.astype(str)
            olt_count['OLT情况'] = olt_count['设备型号'] + '(' + olt_count['OLT网元数量'] + ')'
            olt_grp = olt_count.groupby('所属站点')['OLT情况'].apply(lambda x: ','.join(x)).reset_index()
            
            port_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count','PON口总数':'sum','PON口空闲数':'sum','XGPON口总数':'sum','XGPON口空闲数':'sum'})
            port_table = port_table.reset_index()
            port_table.columns = ['所属站点','OLT网元数量','全量PON口数量','空闲PON口数量','千兆PON口数量','空闲千兆PON口数量']
            port_table = port_table.merge(olt_grp,on='所属站点',how='left')
            port_table['PON口利用率'] = round((1-port_table['空闲PON口数量']/port_table['全量PON口数量'])*100,2)
            port_table['千兆PON口利用率'] = round((1-port_table['空闲千兆PON口数量']/port_table['千兆PON口数量'])*100,2)
            isRedOltPortSite_vec = np.vectorize(self.isRedOltPortSite)
            port_table['是否有端口不足'] = isRedOltPortSite_vec(port_table['空闲PON口数量'],port_table['PON口利用率'])
            port_table = port_table[self.cols]
            port_table.sort_values(by=['是否有端口不足','全量PON口数量'],ascending=[False,False],inplace=True)
            self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            with pd.ExcelWriter(self.file_path) as writer:
                port_table.to_excel(writer,sheet_name='端口资源分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析存在端口不足的OLT站点失败:' + str(e))

    def isRedOltPortSite(self,left_port_num,percent):
        if left_port_num < 5 and percent >= 90:
            return '是'
        else:
            return '否'

# 未部署OLT的汇聚站点
# 所属站点(TEXT), 机房类型(TEXT), 机房名称(TEXT), 业务级别(TEXT), 生命周期状态(TEXT)
class FindNoOltSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','全量PON口数量','空闲PON口数量','PON口利用率','千兆PON口数量','空闲千兆PON口数量','千兆PON口利用率','是否有端口不足']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析未部署OLT的汇聚站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            house = readDataBase('机房')
            house = house[house['业务级别'].str.contains('汇聚')]
            house = house[house['机房类型'] == '传输机房']
            house = house[house['生命周期状态'] == '现网在用']
            site_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count'})
            site_table.columns = ['站点OLT网元数量']
            site_table = site_table.reset_index()
            house_table = pd.pivot_table(df,index=['所属机房'],aggfunc={'OLT网元':'count'})
            house_table = house_table.reset_index()
            house_table.columns = ['机房名称','机房OLT数量']
            house = house.merge(site_table,on='所属站点',how='left')
            house = house.merge(house_table,on='机房名称',how='left')
            house.fillna(0,inplace=True)
            house.sort_values(by=['站点OLT网元数量','机房OLT数量'],ascending=[True,True],inplace=True)
            self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            with pd.ExcelWriter(self.file_path) as writer:
                house.to_excel(writer,sheet_name='汇聚站点部署OLT分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析未部署OLT的汇聚站点失败:' + str(e))
