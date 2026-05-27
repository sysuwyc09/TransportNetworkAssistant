# 公共线程模块,Pyside6 QThread

from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from publicFunc import *
import time
import re

# 检查数据库表格是否存在线程
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
                    if table == '箱体上联OLT跳纤路径表':
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
            return ["OLT网元","机房", "中继段",'光交箱','分纤箱','主光路']
        elif self.analysis_type == "OLT端口":
            return ['OLT网元', 'PON端口', '机房', '华为PON单板','中兴PON单板']
        elif self.analysis_type == "主光路":
            return ['主光路', '箱体上联OLT跳纤路径表','光交箱','分纤箱','ODF']

# 导入文件线程
class ImportFileThread(QThread):
    # 定义两个信号
    state_signal = Signal(str)  # 状态信号
    result_signal = Signal(pd.DataFrame)  # 列名和数据信号
    
    def __init__(self, file_paths, table_name, header_line):
        super().__init__()
        self.file_paths = file_paths
        self.table_name = table_name
        self.header_line = header_line
    
    def run(self):
        try:
            self.state_signal.emit("正在读取文件,请稍后...")
            # 读取文件到DataFrame
            dfs = []
            for file in self.file_paths:
                if file.endswith('.xlsx') or file.endswith('.XLSX'):
                    df = pd.read_excel(file,header=self.header_line-1)
                    dfs.append(df)
                if file.endswith('.csv') or file.endswith('.CSV'):
                    df = readCsvFile(file,header=self.header_line-1)
                    dfs.append(df)
            df = pd.concat(dfs, ignore_index=True)
            if self.table_name == '中继段':
                self.convertLine(df)
            # 发送状态信号
            self.state_signal.emit("导入成功,请选择对应文件列")
            # 发送结果信号
            self.result_signal.emit(df)
        except Exception as e:
            self.state_signal.emit(f"导入失败: {str(e)}")
            self.result_signal.emit(pd.DataFrame)

    def convertLine(self,df):
        value_vars = df.columns.tolist()[16:]
        result = df.melt(id_vars=['名称'], value_vars=value_vars,value_name='光缆段').drop(columns=['variable'])  # 移除不需要的variable列
        # 重置索引
        result = result.reset_index(drop=True)
        result = result[result['光缆段'].notnull()]
        result.rename(columns={'名称':'中继段'},inplace=True)
        writeDataBase('中继段至光缆段',result)

# 更新数据库线程
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
        line2Df = loadLine2Df()
        oltDf = loadOltTypeDf()
        self.state_signal.emit(f'已查询到{len(line2Df)}个跳纤中继段...',0,'')
        self.state_signal.emit('正在加载全量光交设施(超72芯分纤箱、光交箱、ODF) ...',0,'')
        self.all_dev = readDevs()
        self.state_signal.emit('已加载全量光交设施...',0,'')
        self.all_dev.rename(columns={'机房名称':'设施所属机房','业务区':'设施所属业务区'},inplace=True)
        self.all_dev['设施所属位置'] = fixSite(self.all_dev['设施所属机房'],self.all_dev['设施名称'])
        obds = list(set(list(self.all_dev['设施所属位置'])))
        self.state_signal.emit(f'已查询到{len(obds)}个光交设施...',0,'')
        # 按300一组进行分组，如果最后一组不足300则为剩余值
        obds_groups = [obds[i:i+300] for i in range(0, len(obds), 300)]
        result_dfs = []
        start_time = time.time()
        self.state_signal.emit(f'按300个为一组，共{len(obds_groups)}组光交设施进行跳纤路径分析，正在进行第1组...',0,'')
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToMany(obds_group,line2Df,oltDf,'OLT',7,15)
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
        odevs2 = odevs.copy().drop(['设施名称'],axis=1).rename(columns={'设施所属位置':'设施名称'})
        odevs = odevs.drop(['设施所属位置'],axis=1)
        odevs = pd.concat([odevs,odevs2],axis=0).drop_duplicates()
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
# class FindRelayLineThread(QThread):
#     state_signal = Signal(str)
#     result_signal = Signal(pd.DataFrame)
#     def __init__(self,parent=None,keywords=[]):
#         super().__init__(parent)
#         self.keywords = keywords
#         self.cols = ['名称','长度','中继纤芯数量','占用数量','空闲数量','始端机房','终端机房']
    
#     def run(self):
#         try:
#             self.state_signal.emit('正在查找中继段资源，请稍后...')
#             lines = readDataBase('中继段')
#             lines = lines[lines['中继纤芯数量'] > 0]
#             lines['长度'] = round(lines['长度']/1000,2)
#             lines = lines.astype({'名称':str,'始端机房':str,'终端机房':str,'中继纤芯数量':int,'占用数量':int,'空闲数量':int})
#             lines['查找项'] = lines['名称'] + lines['始端机房'] + lines['终端机房']
#             result_df = lines[lines['查找项'].apply(lambda x: self.search(x,self.keywords))]
#             result_df = result_df[self.cols]
#             result_df.sort_values(by=['中继纤芯数量'],ascending=[False],inplace=True)
#             result_df =result_df.reset_index(drop=True)
#             self.result_signal.emit(result_df)
#             self.state_signal.emit('查找完成')
#         except Exception as e:
#             self.state_signal.emit('查找中继段资源失败:' + str(e))
    
#     def search(self,text,keywords=[]):
#         for keyword in keywords:
#             if keyword not in text:
#                 return False
#         return True

# 加载中继段资源的类
class LoadRelayLineThread(QThread):
    state_signal = Signal(str)
    result_signal = Signal(pd.DataFrame)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.cols = ['名称','始端机房','终端机房','长度','纤芯数量','空闲数量','占用数量','查找项']
    
    def run(self):
        try:
            self.state_signal.emit('正在加载中继段资源，请稍后...')
            lines = readDataBase('中继段')
            lines = lines[lines['中继纤芯数量'] > 0]
            lines['长度'] = round(lines['长度']/1000,2)
            lines = lines.astype({'名称':str,'始端机房':str,'终端机房':str,'中继纤芯数量':int,'占用数量':int,'空闲数量':int})
            lines['查找项'] = lines['名称'] + lines['始端机房'] + lines['终端机房']
            lines = lines.rename(columns={'中继纤芯数量':'纤芯数量'})
            lines = lines[self.cols]
            lines.sort_values(by=['纤芯数量'],ascending=[False],inplace=True)
            lines =lines.reset_index(drop=True)
            self.result_signal.emit(lines)
        except Exception as e:
            self.state_signal.emit('加载中继段资源失败:' + str(e))



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


class FindNoXgOltSiteThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
        self.cols = ['所属站点','OLT网元数量','OLT情况','千兆OLT数','用户数','全量PON口数量','空闲PON口数量','PON口利用率']
    
    def run(self):
        try:
            self.state_signal.emit('正在分析未部署千兆OLT的超1000户站点，请稍后...')
            df = readDataBase('OLT网元数据集')
            # site_table = pd.pivot_table(df,index=['所属站点'],aggfunc={'OLT网元':'count','用户数':'sum'})
            # site_table.columns = ['OLT网元数量','用户数']
            # site_table = site_table.reset_index()
            # site_table = site_table[site_table['用户数'] >= 1000]
            # self.state_signal.emit('分析完成，正在生成表格，请稍后...')
            # with pd.ExcelWriter(self.file_path) as writer:
            #     site_table.to_excel(writer,sheet_name='超1000户站点部署OLT分析',index=False)
            self.state_signal.emit('表格生成完成!')
        except Exception as e:
            self.state_signal.emit('分析未部署千兆OLT的超1000户站点失败:' + str(e))

# 超长主光路调优分析
class FindLongPonLineThread(QThread):
    state_signal = Signal(str,float,str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
    
    def run(self):
        try:
            self.state_signal.emit('正在分析超长主光路清单...',0,'')
            pon_df = readDataBase('主光路')
            pon_num = pon_df.shape[0]
            self.state_signal.emit(f'存量共有{pon_num}条主光路，按1跳1dB、1公里0.35dB估算超长主光路（超6dB）',0,'')
            pon_df['光路文本路由'] = pon_df['光路文本路由'].astype(str)
            pon_df['跳数'] = pon_df['光路文本路由'].apply(findJumpNum)
            pon_df['光路长度'] = pon_df['光路长度'].astype(float)
            pon_df['光衰'] = pon_df['跳数'] * 1 + pon_df['光路长度'] / 1000 * 0.35
            lon_pon_df = pon_df[pon_df['光衰'] >= 6]
            self.state_signal.emit(f'按1跳1dB、1公里0.35dB估算，共有{lon_pon_df.shape[0]}条主光路超6dB',10,'')
            lon_pon_df.sort_values(by=['光衰'],ascending=False,inplace=True)
            writeDataBase('超长主光路清单',lon_pon_df)
            
            box_up_df = readDataBase('箱体上联OLT跳纤路径表')
            box_up_df = box_up_df[['设施名称','目标OLT机房','跳纤距离','跳数','光衰预算','跳纤路径']].rename(
                columns={'设施名称':'OBD所属对象','跳纤距离':'调整后距离','跳数':'调整后跳数','光衰预算':'调整后光衰','跳纤路径':'调整路径'})
            box_up_df = box_up_df.sort_values(by=['OBD所属对象','调整后光衰'],ascending=[True,True])
            box_up_df = box_up_df.drop_duplicates(subset=['OBD所属对象'],keep='first')
            
            lon_pon_df = lon_pon_df.merge(box_up_df,on='OBD所属对象',how='left')
            lon_pon_df['调整后光衰'] = lon_pon_df['调整后光衰'].fillna(999)
            lon_pon_df['优化光衰'] = lon_pon_df['光衰'] - lon_pon_df['调整后光衰']
            # 筛选出优化光衰大于等于1dB的主光路
            lon_pon_df = lon_pon_df[lon_pon_df['优化光衰'] >= 1]
            self.state_signal.emit(f'主光路能调优1dB，共有{lon_pon_df.shape[0]}条主光路',30,'')
            # 筛选割接点及割接可行纤芯
            box_df = readDataBase('光交箱')[['设施名称','机房名称']]
            oBox_df = readDataBase('分纤箱')[['设施名称','机房名称']]
            odf_df = readDataBase('ODF')[['设施名称','机房名称']]
            all_site_df = pd.concat([box_df,oBox_df,odf_df],axis=0)
            all_site_df = all_site_df.ffill(axis=1)
            site_dict = all_site_df.set_index('设施名称')['机房名称'].to_dict()
            findKeyPointVec = np.vectorize(findKeyPoint,excluded=['site_dict'])
            lon_pon_df = lon_pon_df.reset_index(drop=True)
            # print(findKeyPoint(lon_pon_df.iloc[0]['光路文本路由'],lon_pon_df.iloc[0]['调整路径'],site_dict=site_dict))
            lon_pon_df['割接点'],lon_pon_df['割接路由'],lon_pon_df['割接可用芯数'] = findKeyPointVec(lon_pon_df['光路文本路由'],lon_pon_df['调整路径'],site_dict=site_dict)
            
            # 剔除割接点，原机房，目标OLT机房 三者同时相同的主光路
            olt_df = readDataBase('OLT网元')[['网元名称','所属机房']].rename(columns={'网元名称':'OLT名称','所属机房':'原机房'})
            lon_pon_df = lon_pon_df.merge(olt_df,on='OLT名称',how='left')
            lon_pon_df = lon_pon_df[(lon_pon_df['割接点'] != lon_pon_df['原机房']) | (lon_pon_df['割接点'] != lon_pon_df['目标OLT机房'])]
            lon_pon_df = lon_pon_df.reset_index(drop=True)
            lon_pon_df.drop(columns=['原机房'],inplace=True)

            self.state_signal.emit('割接路由分析完成，正在写入数据库，请稍后...',90,'')
            writeDataBase('超长主光路调优方案',lon_pon_df)
            self.state_signal.emit('已完成...',100,'')

            
        except Exception as e:
            self.state_signal.emit('分析超长PON主光路调优方案失败:' + str(e),0,'')


# 分析ONU弱光的线程
class FindWeakONUThread(QThread):
    state_signal = Signal(str)
    def __init__(self,parent=None,folder_path=''):
        super().__init__(parent)
        self.folder_path = folder_path
    
    def run(self):
        try:
            onus,ports = self.loadData()
            if not onus or not ports:
                self.state_signal.emit('未加载到ONU或光模块的数据')
                return
            onu_df = pd.concat(onus,axis=0)
            port_df = pd.concat(ports,axis=0)
            # conn = sqlite3.connect('data/onu.db')
            # port_df.to_sql('pon_port',conn,if_exists='replace',index=False)
            # onu_df.to_sql('onu',conn,if_exists='replace',index=False)
            # port_df = pd.read_sql('select * from pon_port',conn)
            # onu_df = pd.read_sql('select * from onu',conn)
            # conn.close()
            port_df['匹配项'] = port_df['网元名称'] + ' ' + port_df['槽位'] + '槽' + port_df['端口'] + '口'
            onu_df['匹配项'] = onu_df['网元名称'] + ' ' + onu_df['槽位'] + '槽' + onu_df['端口'] + '口'
            self.state_signal.emit(f'共{onu_df.shape[0]}条ONU数据,正在分析ONU收光情况...')
            onu_df['ONU收光情况'] = onu_df['接收光功率(dBm)'].apply(self.onuType)
            onu_table = pd.pivot_table(onu_df,index='匹配项',columns=['ONU收光情况'],aggfunc={'网元名称':'count'},fill_value=0)
            onu_table.columns = onu_table.columns.droplevel(0)
            onu_table['有光ONU数'] = 0
            for col in onu_table.columns:
                if col != '有光ONU数' and col != '未知':
                    onu_table['有光ONU数'] += onu_table[col]
            onu_table = onu_table.reset_index()
            if '<-28.5dBm' in onu_table.columns:
                if '-28.5dBm~-27dBm' in onu_table.columns:
                    onu_table['弱光ONU数'] = onu_table['<-28.5dBm'] + onu_table['-28.5dBm~-27dBm']
                else:
                    onu_table['弱光ONU数'] = onu_table['<-28.5dBm']
            else:
                if '-28.5dBm~-27dBm' in onu_table.columns:
                    onu_table['弱光ONU数'] = onu_table['-28.5dBm~-27dBm']
                else:
                    onu_table['弱光ONU数'] = 0
            if '-27dBm~-25dBm' in onu_table.columns:
                onu_table['临界弱光ONU数'] = onu_table['-27dBm~-25dBm']
            else:
                onu_table['临界弱光ONU数'] = 0
            onu_table['弱光ONU整治数'] = onu_table['弱光ONU数'] + onu_table['临界弱光ONU数']
            onu_table['整治ONU比例%'] = round(onu_table['弱光ONU整治数']/onu_table['有光ONU数']*100,2)
            port_df = port_df.merge(onu_table,on='匹配项',how='left')
            # 匹配主光路
            pon_df = readDataBase('主光路')
            pon_df['光路文本路由'] = pon_df['光路文本路由'].astype(str)
            pon_df['跳数'] = pon_df['光路文本路由'].apply(findJumpNum)
            pon_df['光路长度'] = pd.to_numeric(pon_df['光路长度'], errors='coerce')
            pon_df['光路长度'] = round(pon_df['光路长度']/1000,2)
            pon_df['光衰'] = pon_df['跳数'] * 1 + pon_df['光路长度'] * 0.35
            pon_df['槽位'],pon_df['端口'] = zip(*pon_df['PON口'].apply(fixSrcPoNPort))
            pon_df['匹配项'] = pon_df['OLT名称'] + ' ' + pon_df['槽位'] + '槽' + pon_df['端口'] + '口'
            pon_df = pon_df[['匹配项','PON口','PON下挂ONU数量','OBD所属对象','光路名称','光路长度','光路文本路由','跳数','光衰']]
            port_df = port_df.merge(pon_df,on='匹配项',how='left')
            port_df['一级OBD前收光预算'] = port_df['PON口发送光功率 (dBm)'] - port_df['光衰']
            # 匹配超长主光路调优方案
            long_pon_df = readDataBase('超长主光路调优方案')
            long_pon_df = long_pon_df[['PON口','目标OLT机房','调整后距离','调整后跳数','调整后光衰','调整路径','优化光衰','割接点','割接路由','割接可用芯数']]
            port_df = port_df.merge(long_pon_df,on='PON口',how='left')

            # PON口光模块更换范围,发光光功率<5.5dBm，弱光ONU数>0，整治ONU数>=3，目标OLT机房为空或 目标机房不为空且割接可用芯数=0;-28.5dBm~-27dBm >0
            opitcal_model_df = port_df[(port_df['PON口发送光功率 (dBm)']<5.5) & (port_df['弱光ONU数']>0) & (port_df['-28.5dBm~-27dBm']>0) & (port_df['弱光ONU整治数']>=3) & (port_df['整治ONU比例%']>0) & ((port_df['目标OLT机房'].isnull()) | (port_df['割接可用芯数']==0))].copy()
            opitcal_model_df = opitcal_model_df.sort_values(by=['弱光ONU整治数'],ascending=[False])
            # opitcal_model_df = opitcal_model_df.drop(['目标OLT机房','调整后距离','调整后跳数','调整后光衰','调整路径','优化光衰','割接点','割接路由','割接可用芯数'],axis=1)

            # 主光路调优范围；优化光衰>=2dBm，ONU整治数>=3, 割接可用芯数>0
            adjust_pon_df = port_df[(port_df['优化光衰']>=2) & (port_df['弱光ONU整治数']>=3) & (port_df['割接可用芯数']>0)].copy()
            adjust_pon_df = adjust_pon_df.sort_values(by=['弱光ONU整治数'],ascending=[False])

            # 现场测试范围：弱光ONU整治数占比≥80%，且一级OBD前预算出光≥0dBm,弱光ONU整治数>=3
            test_pon_df = port_df[(port_df['整治ONU比例%']>=80) & (port_df['一级OBD前收光预算']>=0) & (port_df['弱光ONU整治数']>=3) & (port_df['PON口发送光功率 (dBm)']) ].copy()
            test_pon_df = test_pon_df.sort_values(by=['弱光ONU整治数'],ascending=[False])

            # 聚类弱光OBD所属对象分析；光衰≥6dBm，且调整后光衰为空或者调整后光衰≥6dBm
            cluster_pon_df = port_df[(port_df['光衰']>=6) & ((port_df['调整后光衰'].isnull()) | (port_df['调整后光衰']>=6))].copy()
            cluster_table = pd.pivot_table(cluster_pon_df,index='OBD所属对象',aggfunc={'PON口':'count','弱光ONU整治数':'sum'})
            cluster_table = cluster_table.reset_index().rename(columns={'PON口':'PON口数','弱光ONU整治数':'聚类弱光ONU整治数'})
            cluster_pon_df = cluster_pon_df.merge(cluster_table,on='OBD所属对象',how='left')
            cluster_pon_df = cluster_pon_df.sort_values(by=['PON口数','聚类弱光ONU整治数'],ascending=[False,False])


            self.state_signal.emit('分析完成，正在生成数据表格。')
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with pd.ExcelWriter(os.path.join(self.folder_path,f'ONU弱光分析结果{dt}.xlsx')) as writer:
                port_df.to_excel(writer,sheet_name='PON口详细清单',index=False)
                opitcal_model_df.to_excel(writer,sheet_name='PON口光模块更换清单',index=False)
                adjust_pon_df.to_excel(writer,sheet_name='主光路调优清单',index=False)
                test_pon_df.to_excel(writer,sheet_name='现场测试清单',index=False)
                cluster_pon_df.to_excel(writer,sheet_name='聚类弱光OBD所属对象分析',index=False)
            self.state_signal.emit('已完成...')
        except Exception as e:
            self.state_signal.emit('分析ONU弱光失败:' + str(e))
            
    def loadData(self):
        onus = []
        ports = []
        # 华为ONU ：网元名称 槽号 端口号 接收光功率(dBm)
        # 中兴ONU：网元名称 槽位 端口 接收光功率(dBm)
        # 华为光模块：网元名称	资源名称 PON口光模块子类型 PON口发送光功率 (dBm)；资源名称 框:0/槽:1/端口:0
        # 中兴光模块：网元名称 槽位 端口 发送光功率(dBm) 等级(类型/子类型)
        files = os.listdir(self.folder_path)
        for file in files:
            if '华为ONU' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽号','端口号','接收光功率(dBm)'])
                df = df[['网元名称','槽号','端口号','接收光功率(dBm)']].rename(columns={'槽号':'槽位','端口号':'端口'})
                df = df.astype({'槽位':str,'端口':str})
                df['接收光功率(dBm)'] = pd.to_numeric(df['接收光功率(dBm)'],errors='coerce')
                onus.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '中兴ONU' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽位','端口','接收光功率(dBm)'])
                df = df[['网元名称','槽位','端口','接收光功率(dBm)']]
                df = df.astype({'槽位':str,'端口':str})
                df['接收光功率(dBm)'] = pd.to_numeric(df['接收光功率(dBm)'],errors='coerce')
                onus.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '华为光模块' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)'])
                df = df[['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)']].rename(columns={'PON口光模块子类型':'PON口光模块类型'})
                df['槽位'],df['端口'] = zip(*df['资源名称'].apply(self.fixHwPort))
                df = df[['网元名称','槽位','端口','PON口光模块类型','PON口发送光功率 (dBm)']]
                df['PON口发送光功率 (dBm)'] = pd.to_numeric(df['PON口发送光功率 (dBm)'],errors='coerce')
                ports.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
            if '中兴光模块' in file:
                if '.xlsx' in file and '$' not in file:
                    df = pd.read_excel(os.path.join(self.folder_path,file))
                elif '.csv' in file or '.CSV' in file:
                    df = readCsvFile(os.path.join(self.folder_path,file))
                else:
                    df = pd.DataFrame(columns=['网元名称','槽位','端口','发送光功率(dBm)','等级(类型/子类型)','光模块号/通道号'])
                df = df[['网元名称','槽位','端口','发送光功率(dBm)','等级(类型/子类型)','光模块号/通道号']].rename(columns={'发送光功率(dBm)':'PON口发送光功率 (dBm)','等级(类型/子类型)':'PON口光模块类型'})
                df['光模块号/通道号'] = df['光模块号/通道号'].astype(str)
                df = df[df['光模块号/通道号'] != '1']
                df = df[df['光模块号/通道号'] != '2']

                df = df[['网元名称','槽位','端口','PON口光模块类型','PON口发送光功率 (dBm)']]
                df = df.astype({'槽位':str,'端口':str})
                df['PON口发送光功率 (dBm)'] = pd.to_numeric(df['PON口发送光功率 (dBm)'],errors='coerce')
                ports.append(df)
                self.state_signal.emit(f'已加载{file}，共{df.shape[0]}条数据')
        return onus,ports
 
    def fixHwPort(self,port_name):
        regex = r'槽:(\d+)/端口:(\d+)'
        match = re.search(regex,port_name)
        if match:
            slot = match.group(1)
            port = match.group(2)
            return slot,port
        else:
            return '-','-'

    def onuType(self,onu_dbm):
        if pd.isnull(onu_dbm):
            return '未知'
        else:
            if onu_dbm >= -21:
                return '≥-21dBm'
            elif onu_dbm >= -25:
                return '-25dBm~-21dBm'
            elif onu_dbm >= -27:
                return '-27dBm~-25dBm'
            elif onu_dbm >= -28.5:
                return '-28.5dBm~-27dBm'
            else:
                return '<-28.5dBm'


# 单点A-B跳纤方案线程
class DispatchABThread(QThread):
    state_signal = Signal(str) 
    def __init__(self,parent=None,a_name='',b_name='',jump_num=5,dbm_num=14,must_devs=[],not_devs=[]):
        super().__init__(parent)
        self.a_name = a_name
        self.b_name = b_name
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.must_devs = must_devs
        self.not_devs = not_devs
    
    def run(self):
        try:
            self.state_signal.emit('正在加载中继段信息...')
            line2Df = loadLine2Df()
            resultDf = dispatchOneToOne(line2Df,self.a_name,self.b_name,self.jump_num,self.dbm_num,self.not_devs)
            if resultDf.shape[0] == 0:
                self.state_signal.emit('未找到符合条件的跳纤路径')
            else:
                if self.must_devs:
                    for dev in self.must_devs:
                        resultDf = resultDf[resultDf['跳纤路径'].str.contains(dev)]
                if resultDf.shape[0] == 0:
                    self.state_signal.emit('未找到符合条件的跳纤路径')
                else:
                    self.state_signal.emit(f'已找到{resultDf.shape[0]}条符合条件的跳纤路径')
                    # 评估方案得分，算法如下：
                    resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
                    resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
                    resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
                    resultDf = resultDf.sort_values(by='方案得分',ascending=False)
                    dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
                    # 清除a_name和b_name不符合文件命名的字符
                    temp_a_name = re.sub(r'[^\w]','',self.a_name)
                    temp_b_name = re.sub(r'[^\w]','',self.b_name)
                    out_file_name = f'结果\\{temp_a_name}_{temp_b_name}_跳纤路径{dt}.xlsx'
                    resultDf.to_excel(out_file_name,index=False)
                    os.startfile(out_file_name)
                    self.state_signal.emit(f'已将结果保存至{out_file_name}')
        except Exception as e:
            self.state_signal.emit(f'发生错误：{e}')


# 批量A-B跳纤方案线程
class DispatchABSThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,jump_num=5,dbm_num=14,file_path=''):
        super().__init__(parent)
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.file_path = file_path
    
    def run(self):
        self.state_signal.emit('正在加载需求文件信息...')
        df = pd.read_excel(self.file_path)
        df = df.astype(str)
        if 'A端' not in df.columns or 'B端' not in df.columns:
            self.error_signal.emit('需求文件格式错误，必须包含A端和B端列')
            return;
        self.state_signal.emit('正在加载中继段信息...')
        line2Df = loadLine2Df()
        self.state_signal.emit('正在分析跳纤路由...')
        results = []
        for i in range(df.shape[0]):
            a_name = df.loc[i,'A端']
            b_name = df.loc[i,'B端']
            if a_name == b_name:
                temp_df = pd.DataFrame({'A端':[a_name],'B端':[b_name],'跳纤路径':'A端等于B端'})
            else:
                temp_df = dispatchOneToOne(line2Df,a_name,b_name,self.jump_num,self.dbm_num,[])
            if temp_df.shape[0] == 0:
                temp_df = pd.DataFrame({'A端':[a_name],'B端':[b_name],'跳纤路径':'未找到符合条件的跳纤路径'})
            results.append(temp_df)
            self.state_signal.emit(f'处理进度：{i+1}/{df.shape[0]}')
        resultDf = pd.concat(results,ignore_index=True).drop_duplicates().reset_index(drop=True)
        if resultDf.shape[0] == 0:
            self.error_signal.emit('未找到符合条件的跳纤路径')
        else:
            # 评估方案得分，算法如下：
            resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
            resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
            resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
            resultDf = resultDf.sort_values(by=['A端','B端','方案得分'],ascending=[False,False,False])
            best_df = resultDf.groupby(['A端','B端']).first().reset_index(drop=False)
            dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
            file_name = self.file_path.split('/')[-1].split('.')[0]
            out_file_name = f'结果\\{file_name}_批量需求跳纤路径{dt}.xlsx'
            with pd.ExcelWriter(out_file_name) as writer:
                resultDf.to_excel(writer,sheet_name='所有跳纤路径',index=False)
                best_df.to_excel(writer,sheet_name='最优跳纤路径',index=False)
            os.startfile(out_file_name)
            self.state_signal.emit(f'已将结果保存至{out_file_name}')

# 集中跳纤至OLT、CRAN机房的线程
class DispatchToManyThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,jump_num=5,dbm_num=14,file_path='',b_type='CRAN'):
        super().__init__(parent)
        self.jump_num = jump_num
        self.dbm_num = dbm_num
        self.file_path = file_path
        self.b_type = b_type
    
    def run(self):
        self.state_signal.emit('正在加载需求文件信息...')
        df = pd.read_excel(self.file_path)
        df = df.astype(str)
        if '需求名称' not in df.columns:
            self.error_signal.emit('需求文件格式错误，必须包含需求名称列')
            return;
        obds = df['需求名称'].tolist()
        if len(obds) == 0:
            self.error_signal.emit('需求行为空')
            return;
        self.state_signal.emit(f'共{len(obds)}个需求，将按500一组进行分析')
        # 按500一组进行分组，如果最后一组不足500则为剩余值
        obds_groups = [obds[i:i+500] for i in range(0, len(obds), 500)]

        self.state_signal.emit('正在加载中继段信息...')
        line2Df = loadLine2Df()
        self.state_signal.emit(f'正在加载{self.b_type}机房信息...')
        if self.b_type == 'CRAN':
            b_df = loadCranTypeDf()
        elif self.b_type == 'OLT':
            b_df = loadOltTypeDf()
        self.state_signal.emit('正在分析跳纤路由...')
        result_dfs = []
        start_time = time.time()
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToMany(obds_group,line2Df,b_df,self.b_type,self.jump_num,self.dbm_num)
            result_dfs.append(temp_df)
            # 计算预估剩余时间
            elapsed_time = time.time() - start_time
            avg_time_per_group = elapsed_time / (i+1)
            remaining_groups = len(obds_groups) - (i+1)
            estimated_time = avg_time_per_group * remaining_groups
            self.state_signal.emit(f'已完成{i+1}/{len(obds_groups)}组光设施跳纤分析,剩余约{int(estimated_time/60)}分{int(estimated_time%60)}秒')
        resultDf = pd.concat(result_dfs,ignore_index=True).drop_duplicates().reset_index(drop=True)
        if resultDf.shape[0] == 0:
            self.error_signal.emit(f'未找到符合条件的跳纤路径')
            return;
        resultDf['最小空闲芯数评分'] = resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
        # 评估方案得分，算法如下：
        resultDf['最小空闲芯数得分'] =  resultDf['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
        resultDf['方案得分'] = round(resultDf['最小空闲芯数得分']/resultDf['光衰预算'],2)
        resultDf.drop(columns=['最小空闲芯数得分'],inplace=True)
        resultDf = resultDf.sort_values(by=['A端','方案得分'],ascending=[False,False])
        best_df = resultDf.groupby(['A端']).first().reset_index(drop=False)
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        file_name = self.file_path.split('/')[-1].split('.')[0]
        out_file_name = f'结果\\{file_name}_需求至{self.b_type}的跳纤路径{dt}.xlsx'

        all_df = pd.DataFrame({'A端':obds})
        all_df = pd.merge(all_df,resultDf,on='A端',how='left')
        not_df = all_df[all_df['跳纤路径'].isnull()].copy()
        not_df['跳纤路径'] = '未找到符合条件的跳纤路径'
        self.state_signal.emit('分析完成，正在生成表格中')
        with pd.ExcelWriter(out_file_name) as writer:
            all_df.to_excel(writer,sheet_name='所有跳纤路径',index=False)
            best_df.to_excel(writer,sheet_name='最优跳纤路径',index=False)
            not_df.to_excel(writer,sheet_name='未找到跳纤路径',index=False)
        os.startfile(out_file_name)
        self.state_signal.emit(f'已将结果保存至{out_file_name}')


'''
通报弱光清单分析
1、分析C+光模块替换分析
2、分析可优化主光路清单,选取不能替换的光模块PON口
3、弱光ODB经纬度匹配,全量匹配
4、展开弱光匹配
''' 
class PonPortReplaceThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,folder_path=''):
        super().__init__(parent)
        self.folder_path = folder_path

    def run(self):
        self.state_signal.emit('正在加载弱光ONU清单和光模块清单...')
        week_onu_file = ''
        hw_port_file = ''
        zte_port_file = ''
        for file in os.listdir(self.folder_path):
            if '7天内4天弱光清单' in file and '$' not in file and '.xlsx' in file:
                week_onu_file = self.folder_path + '/' + file
            elif '华为光模块' in file and '$' not in file and '.xlsx' in file:
                hw_port_file = self.folder_path + '/' + file
            elif '中兴光模块' in file and '$' not in file and '.xlsx' in file:
                zte_port_file = self.folder_path + '/' + file

        if week_onu_file == '' or hw_port_file == '' or zte_port_file == '':
            self.error_signal.emit('未找到弱光ONU清单、华为光模块清单或中兴光模块清单')
            return;
        self.state_signal.emit('正在读取弱光ONU清单')
        week_onu_df = pd.read_excel(week_onu_file,engine='openpyxl')
        self.state_signal.emit('正在读取华为光模块清单')
        hw_port_df = pd.read_excel(hw_port_file,engine='openpyxl')
        self.state_signal.emit('正在读取中兴光模块清单')
        zte_port_df = pd.read_excel(zte_port_file,engine='openpyxl')  
        self.state_signal.emit('正在分析弱光清单U')
        hw_port_df = hw_port_df[['网元名称','资源名称','PON口光模块子类型','PON口发送光功率 (dBm)','PON口光模块类型']]
        zte_port_df = zte_port_df[['网元名称','机框','槽位','端口','等级(类型/子类型)','发送光功率(dBm)','业务类型']]
        hw_port_df['资源名称'] = hw_port_df['资源名称'].astype('str')
        hw_port_df['机框'],hw_port_df['槽位'],hw_port_df['端口'] = zip(*hw_port_df['资源名称'].apply(self.fixHwPort))
        hw_port_df = hw_port_df.rename(columns={'PON口光模块类型':'PON口类型'})
        zte_port_df = zte_port_df.rename(columns={'等级(类型/子类型)':'PON口光模块子类型','发送光功率(dBm)':'PON口发送光功率 (dBm)','业务类型':'PON口类型'})
        hw_port_df.drop(columns=['资源名称'],inplace=True)
        port_df = pd.concat([hw_port_df,zte_port_df],ignore_index=True)
        port_df = port_df.astype('str')
        port_df['PON'] = port_df['网元名称'] + '-' + port_df['机框'] + '/' + port_df['槽位'] + '/' + port_df['端口']
        port_df = port_df.groupby(['PON']).first().reset_index(drop=False)
        week_onu_df = pd.merge(week_onu_df,port_df,on='PON',how='left')
        self.state_signal.emit('正在分析弱光清单U的光模块替换分析')
        week_onu_df,week_port_table = self.analyzePonModel(week_onu_df)
        self.state_signal.emit('正在分析弱光清单U的可优化主光路清单,分析结构主光路问题')
        opt_port_df,long_pon_up_link,adjust_port_df,dev_df = self.analyzeLongPonLine(week_port_table)

        self.state_signal.emit('正在生成7天内4天弱光清单匹配光模块信息。')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with pd.ExcelWriter(f'结果/7天内4天弱光清单匹配光模块信息{dt}.xlsx') as writer:
            week_onu_df.to_excel(writer,sheet_name='弱光ONU清单',index=False)
            week_port_table.to_excel(writer,sheet_name='弱光PON口替换光模块分析过程',index=False)
            opt_port_df.to_excel(writer,sheet_name='可光模块替代的端口清单',index=False)
            long_pon_up_link.to_excel(writer,sheet_name='超长主光路调优方案',index=False)
            adjust_port_df.to_excel(writer,sheet_name='待调整结构的清单',index=False)
            dev_df.to_excel(writer,sheet_name='弱光聚合情况',index=False)
        self.state_signal.emit('分析完成')

    def analyzeLongPonLine(self,week_port_table):
        # 筛选可光模块替代的端口清单
        opt_port_df = week_port_table[week_port_table['替换光模块类型']!='--']

        # 分析可调优清单
        not_opt_port_df = week_port_table[week_port_table['替换光模块类型']=='--']
        long_pon_port = readDataBase('超长主光路清单')
        long_pon_port['PON'] = long_pon_port['PON口'].apply(self.fixLongPonPort)

        long_pon_port = long_pon_port.merge(not_opt_port_df,on='PON')

        long_pon_up_link = readDataBase('超长主光路调优方案')
        long_pon_up_link = long_pon_up_link[long_pon_up_link['割接可用芯数']>0]
        temp_df = long_pon_port[['区域','新网格','PON口类型','PON','PON口','弱光ONU数','预估替换光模块可整治数','PON口光模块子类型','PON口发送光功率 (dBm)','替换光模块类型']]

        long_pon_up_link = long_pon_up_link.merge(temp_df,on='PON口')
        temp_df = long_pon_up_link[['PON']].copy()
        temp_df['是否可主光路调整'] = '是'

        long_pon_port = long_pon_port.merge(temp_df,on='PON',how='left')
        long_pon_port['是否可主光路调整'] = long_pon_port['是否可主光路调整'].fillna('否')

        # 分析待调整结构的清单
        adjust_port_df = long_pon_port[long_pon_port['是否可主光路调整']=='否']
        all_dev_df = readDevsWithCoord()[['设施名称','经度','纬度']]
        all_dev_df.rename(columns={'设施名称':'OBD所属对象'},inplace=True)
        adjust_port_df = adjust_port_df.merge(all_dev_df,on='OBD所属对象',how='left')

        # 分析弱光聚合情况
        dfs = adjust_port_df['光路文本路由'].apply(self.fixPathPoint)
        pon_path_df = pd.concat(dfs.tolist(),ignore_index=True)
        pon_path_df = pon_path_df.drop_duplicates()
        dev_df = pd.pivot_table(pon_path_df,index='光交设施',aggfunc={'光路文本路由':'count'},fill_value=0)
        dev_df = dev_df.reset_index()
        dev_df.columns = ['光交设施','光路数']
        adjust_port_unique = adjust_port_df[['光路文本路由','PON口']].drop_duplicates(subset=['光路文本路由'], keep='first')
        pon_path_df = pon_path_df.merge(adjust_port_unique,on='光路文本路由',how='left')
        temp_df = pon_path_df[['光交设施','PON口']]
        temp_grp = temp_df.groupby('光交设施').agg('、'.join)
        temp_grp = temp_grp.reset_index().rename(columns={'PON口':'弱光PON口清单'})
        dev_df = dev_df.merge(temp_grp,on='光交设施',how='left')
        dev_df.sort_values(by='光路数',ascending=False,inplace=True)

        return opt_port_df,long_pon_up_link,adjust_port_df,dev_df

    def fixLongPonPort(self,pon_port):
        parts = pon_port.split('-')
        olt_name = '-'.join(parts[:-5])
        return olt_name + '-' + parts[-5] + '/' + parts[-4] + '/' + parts[-2]

    def fixPathPoint(self,pon_path):
        sites = re.findall('>(.*?)\([AB正反/面ODM0-9]+-\d+-\d+',pon_path)
        items = []
        # 倒序查询割接路径上的割接点,排除空字符串和NA值
        for site in sites:
            if site not in items:
                items.append(site)
        items = items[1:]
        df = pd.DataFrame(items,columns=['光交设施'])
        df['光路文本路由'] = pon_path
        return df


    def analyzePonModel(self,week_onu_df):
        '''
        分析更换光模块可解决的弱光PON口
        '''
        isOnuGoodm_vec = np.vectorize(self.isOnuDBmGood)
        week_onu_df['PON口发送光功率 (dBm)'] = pd.to_numeric(week_onu_df['PON口发送光功率 (dBm)'],errors='coerce')
        week_onu_df['RMS收光+软探针'] = pd.to_numeric(week_onu_df['RMS收光+软探针'],errors='coerce')
        week_onu_df['预估替换光模块可整治'] = isOnuGoodm_vec(week_onu_df['RMS收光+软探针'],week_onu_df['PON口发送光功率 (dBm)'],week_onu_df['PON口类型'],week_onu_df['PON口光模块子类型'])
        week_port_table = pd.pivot_table(week_onu_df,index=['PON'],columns=['预估替换光模块可整治'],aggfunc={'区域':'count'},fill_value=0)
        week_port_table.columns = week_port_table.columns.droplevel(0)
        week_port_table = week_port_table.reset_index()
        week_port_table['弱光ONU数'] = week_port_table['是'] + week_port_table['否']
        week_port_table.rename(columns={'是':'预估替换光模块可整治数'},inplace=True)
        week_port_table = week_port_table[['PON','弱光ONU数','预估替换光模块可整治数']]
        temp_df = week_onu_df[['区域','新网格','PON','PON口类型','PON口光模块子类型','PON口发送光功率 (dBm)']].copy()
        temp_df = temp_df.drop_duplicates(subset=['PON'],keep='first')
        week_port_table = pd.merge(week_port_table,temp_df,on='PON',how='left')
        install_opt_model_vec = np.vectorize(self.installOptModel)
        week_port_table['替换光模块类型'] = install_opt_model_vec(week_port_table['预估替换光模块可整治数'],week_port_table['PON口类型'])
        
        return week_onu_df,week_port_table

    def installOptModel(self,onu_num,port_type):
        '''
        判断更换光模块的类型
        '''
        if onu_num > 0:
            if port_type == 'GPON':
                return 'Class C++'
            else:
                return 'Class D'
        return '--'

    def isOnuDBmGood(self,onu_dbm,port_dbm,port_type,opt_type):
        '''
        判断弱光ONU收光是否可以通过更换光模块解决
        '''
        if port_type == '10GGPON' or port_type == 'XGPON+GPON' or port_type == 'XGSPON':
            if opt_type == 'CLASS C+' or opt_type == 'N2a' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7.8 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        if port_type == 'GPON':
            if opt_type == 'CLASS C+' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        return '否'


    def fixHwPort(self,port_name):
        regex = r'框:(\d+)/槽:(\d+)/端口:(\d+)'
        match = re.match(regex,port_name)
        if match:
            box = match.group(1)
            slot = match.group(2)
            port = match.group(3)
            return box,slot,port
        else:
            return '-','-','-'

'''
临界弱光+弱光，主光路调优分析
1、分析弱光+临界弱光ONU的清单，分析主光路可调优数量
2、根据分析结果，生成主光路调优建议
'''
class WeekOnuPortAnalyzeThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        self.state_signal.emit('正在加载弱光ONU清单清单...')
        week_onu_df = pd.read_excel(self.file_path,engine='openpyxl')
        self.state_signal.emit('正在分析弱光清单U')
        week_onu_df,week_port_table = self.analyzeWeekPort(week_onu_df)

        self.state_signal.emit('正在分析弱光清单U的可优化主光路清单,分析结构主光路问题')
        week_port_table,long_pon_up_link,adjust_port_df,dev_df = self.analyzeLongPonLine(week_port_table)


        self.state_signal.emit('正在生成分析结果。')
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        out_file_path = '结果/'+self.file_path.split('/')[-1].split('.')[0]+'_分析结果'+dt+'.xlsx'

        with pd.ExcelWriter(out_file_path) as writer:
            week_onu_df.to_excel(writer,sheet_name='弱光ONU清单',index=False)
            week_port_table.to_excel(writer,sheet_name='弱光PON口清单',index=False)
            long_pon_up_link.to_excel(writer,sheet_name='超长主光路可调优方案',index=False)
            adjust_port_df.to_excel(writer,sheet_name='超长待调整结构的清单',index=False)
            dev_df.to_excel(writer,sheet_name='弱光聚合情况',index=False)
        self.state_signal.emit('分析完成')

    def analyzeWeekPort(self,week_onu_df):
        '''
        分析弱光清单U的弱光类型
        '''
        week_onu_df['接收光功率(dBm)'] = pd.to_numeric(week_onu_df['接收光功率(dBm)'],errors='coerce')
        week_onu_df['弱光类型'] = week_onu_df['接收光功率(dBm)'].apply(lambda x: '弱光' if x <= -27 else ('临界弱光' if x <= -25 else '正常'))
        week_onu_df['弱光类型'] = week_onu_df['弱光类型'].fillna('正常') 
        anaylyzeArea_vec = np.vectorize(self.anaylyzeArea)
        week_onu_df['区域'] = anaylyzeArea_vec(week_onu_df['区域'],week_onu_df['PON'])
        week_port_table = pd.pivot_table(week_onu_df,index=['PON'],columns=['弱光类型'],aggfunc='size',fill_value=0)
        week_port_table = week_port_table.reset_index()
        week_port_table = week_port_table.rename(columns={'弱光':'弱光ONU数','临界弱光':'临界弱光ONU数'})
        week_port_table['待整治数'] = week_port_table['弱光ONU数'] + week_port_table['临界弱光ONU数']
        port_area = week_onu_df[['PON','区域','网格']].drop_duplicates(subset=['PON'],keep='first')
        week_port_table = week_port_table.merge(port_area,on='PON',how='left')
        return week_onu_df,week_port_table

    def anaylyzeArea(self,company,olt_name):
        if pd.isnull(company):
            company = fixCompany(olt_name)
        elif company == '':
            company = fixCompany(olt_name)    
        return company

    def analyzeLongPonLine(self,week_port_table):

        # 分析可调优清单
        long_pon_port = readDataBase('超长主光路清单')
        long_pon_port['PON'] = long_pon_port['PON口'].apply(self.fixLongPonPort)

        temp_df = long_pon_port[['PON','PON口']].copy()
        temp_df['是否超长主光路'] = '是'
        week_port_table = week_port_table.merge(temp_df,on='PON',how='left')
        week_port_table['是否超长主光路'] = week_port_table['是否超长主光路'].fillna('否')

        long_pon_up_link = readDataBase('超长主光路调优方案')
        long_pon_up_link = long_pon_up_link[long_pon_up_link['割接可用芯数']>0]
        long_pon_up_link = long_pon_up_link.merge(week_port_table,on='PON口')


        temp_df = long_pon_up_link[['PON口']].copy()
        temp_df['是否可主光路调整'] = '是'
        week_port_table = week_port_table.merge(temp_df,on='PON口',how='left')
        week_port_table['是否可主光路调整'] = week_port_table['是否可主光路调整'].fillna('否')

        # 分析待调整结构的清单
        adjust_port_df = week_port_table[week_port_table['是否可主光路调整']=='否'].merge(long_pon_port,on=['PON','PON口'])
        all_dev_df = readDevsWithCoord()[['设施名称','经度','纬度']]
        all_dev_df.rename(columns={'设施名称':'OBD所属对象'},inplace=True)
        adjust_port_df = adjust_port_df.merge(all_dev_df,on='OBD所属对象',how='left')

        # 分析弱光聚合情况
        dfs = adjust_port_df['光路文本路由'].apply(self.fixPathPoint)
        pon_path_df = pd.concat(dfs.tolist(),ignore_index=True)
        pon_path_df = pon_path_df.drop_duplicates()
        dev_df = pd.pivot_table(pon_path_df,index='光交设施',aggfunc={'光路文本路由':'count'},fill_value=0)
        dev_df = dev_df.reset_index()
        dev_df.columns = ['光交设施','光路数']
        adjust_port_unique = adjust_port_df[['光路文本路由','PON口']].drop_duplicates(subset=['光路文本路由'], keep='first')
        pon_path_df = pon_path_df.merge(adjust_port_unique,on='光路文本路由',how='left')
        temp_df = pon_path_df[['光交设施','PON口']]
        temp_grp = temp_df.groupby('光交设施').agg('、'.join)
        temp_grp = temp_grp.reset_index().rename(columns={'PON口':'弱光PON口清单'})
        dev_df = dev_df.merge(temp_grp,on='光交设施',how='left')
        dev_df.sort_values(by='光路数',ascending=False,inplace=True)

        return week_port_table,long_pon_up_link,adjust_port_df,dev_df

    def fixLongPonPort(self,pon_port):
        parts = pon_port.split('-')
        olt_name = '-'.join(parts[:-5])
        return olt_name + '-' + parts[-5] + '/' + parts[-4] + '/' + parts[-2]

    def fixPathPoint(self,pon_path):
        sites = re.findall('>(.*?)\([AB正反/面ODM0-9]+-\d+-\d+',pon_path)
        items = []
        # 倒序查询割接路径上的割接点,排除空字符串和NA值
        for site in sites:
            if site not in items:
                items.append(site)
        items = items[1:]
        df = pd.DataFrame(items,columns=['光交设施'])
        df['光路文本路由'] = pon_path
        return df


    def analyzePonModel(self,week_onu_df):
        '''
        分析更换光模块可解决的弱光PON口
        '''
        isOnuGoodm_vec = np.vectorize(self.isOnuDBmGood)
        week_onu_df['PON口发送光功率 (dBm)'] = pd.to_numeric(week_onu_df['PON口发送光功率 (dBm)'],errors='coerce')
        week_onu_df['RMS收光+软探针'] = pd.to_numeric(week_onu_df['RMS收光+软探针'],errors='coerce')
        week_onu_df['预估替换光模块可整治'] = isOnuGoodm_vec(week_onu_df['RMS收光+软探针'],week_onu_df['PON口发送光功率 (dBm)'],week_onu_df['PON口类型'],week_onu_df['PON口光模块子类型'])
        week_port_table = pd.pivot_table(week_onu_df,index=['PON'],columns=['预估替换光模块可整治'],aggfunc={'区域':'count'},fill_value=0)
        week_port_table.columns = week_port_table.columns.droplevel(0)
        week_port_table = week_port_table.reset_index()
        week_port_table['弱光ONU数'] = week_port_table['是'] + week_port_table['否']
        week_port_table.rename(columns={'是':'预估替换光模块可整治数'},inplace=True)
        week_port_table = week_port_table[['PON','弱光ONU数','预估替换光模块可整治数']]
        temp_df = week_onu_df[['区域','新网格','PON','PON口类型','PON口光模块子类型','PON口发送光功率 (dBm)']].copy()
        temp_df = temp_df.drop_duplicates(subset=['PON'],keep='first')
        week_port_table = pd.merge(week_port_table,temp_df,on='PON',how='left')
        install_opt_model_vec = np.vectorize(self.installOptModel)
        week_port_table['替换光模块类型'] = install_opt_model_vec(week_port_table['预估替换光模块可整治数'],week_port_table['PON口类型'])
        
        return week_onu_df,week_port_table

    def installOptModel(self,onu_num,port_type):
        '''
        判断更换光模块的类型
        '''
        if onu_num > 0:
            if port_type == 'GPON':
                return 'Class C++'
            else:
                return 'Class D'
        return '--'

    def isOnuDBmGood(self,onu_dbm,port_dbm,port_type,opt_type):
        '''
        判断弱光ONU收光是否可以通过更换光模块解决
        '''
        if port_type == '10GGPON' or port_type == 'XGPON+GPON' or port_type == 'XGSPON':
            if opt_type == 'CLASS C+' or opt_type == 'N2a' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7.8 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        if port_type == 'GPON':
            if opt_type == 'CLASS C+' or opt_type == 'CLASS B+':
                new_onu_dbm = onu_dbm + 7 - port_dbm
                if new_onu_dbm > -27:
                    return '是'
        return '否'


    def fixHwPort(self,port_name):
        regex = r'框:(\d+)/槽:(\d+)/端口:(\d+)'
        match = re.match(regex,port_name)
        if match:
            box = match.group(1)
            slot = match.group(2)
            port = match.group(3)
            return box,slot,port
        else:
            return '-','-','-'

# 分析零利用率的光缆段
class NotUseLineThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,parent=None,file_path=''):
        super().__init__(parent)
        self.file_path = file_path
    
    def run(self):
        self.state_signal.emit('正在校验数据库表格')
        needs_files = ['中继段至光缆段','中继段','光缆段']
        # 查看data\transportNetwork.db是否存在这些表
        conn = sqlite3.connect('data/transportNetwork.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        for table in needs_files:
            if table not in tables:
                self.error_signal.emit(f'数据库表格中不存在{table}表')
                return;
        relay_to_line_df = pd.read_sql_query(f'SELECT * FROM {needs_files[0]}',conn)
        relay_df = pd.read_sql_query(f'SELECT * FROM {needs_files[1]}',conn)
        line_df = pd.read_sql_query(f'SELECT * FROM {needs_files[2]}',conn)
        # 筛选清单
        line_df = line_df[line_df['红线范围']=='红线外']
        line_df = line_df[line_df['资源状态']=='在网']

        conn.close()
        self.state_signal.emit('正在分析零利用率的光缆段')
        table,not_use_line_df,sub_df_1,sub_df_2,sub_df_3 = self.analyzeNotUseLine(relay_to_line_df,relay_df,line_df)
        self.state_signal.emit('正在生成零利用率光缆段分析结果')
        with pd.ExcelWriter(self.file_path) as writer:
            table.to_excel(writer,sheet_name='零利用率光缆段统计结果',index=False)
            not_use_line_df.to_excel(writer,sheet_name='零利用率光缆段清单',index=False)
            sub_df_1.to_excel(writer,sheet_name='无中继段疑似垃圾数据清单',index=False)
            sub_df_2.to_excel(writer,sheet_name='实际有占用清单',index=False)
            sub_df_3.to_excel(writer,sheet_name='实际无占用清单',index=False)
        self.state_signal.emit('零利用率光缆段分析结果已生成！')
    
    def analyzeNotUseLine(self,relay_to_line_df,relay_df,line_df):
        line_df['初验时间'] = pd.to_datetime(line_df['初验时间'],errors='coerce')
        line_df['时间类型'] = line_df['初验时间'].apply(self.timeType)
        relay_df = relay_df[['名称','中继纤芯数量','占用数量']].rename(columns={'名称':'中继段'})
        relay_to_line_df = relay_to_line_df.merge(relay_df,on='中继段',how='left')
        relay_to_line_df = relay_to_line_df.drop_duplicates()
        line_table = pd.pivot_table(relay_to_line_df,index=['光缆段'],aggfunc={'中继段':'count','中继纤芯数量':'sum','占用数量':'sum'})
        line_table = line_table.reset_index().rename(columns={'光缆段':'名称','中继段':'中继段数','中继纤芯数量':'成端纤芯数','占用数量':'纤芯占用数'})
        line_df = line_df.merge(line_table,on='名称',how='left')
        # 聚合中继段详细情况
        relay_to_line_df = relay_to_line_df.astype('str')
        relay_to_line_df['详细'] = relay_to_line_df['中继段'] + '(' + relay_to_line_df['占用数量'] + '/' + relay_to_line_df['中继纤芯数量'] + ')'
        line_detail_df = relay_to_line_df[['光缆段','详细']]
        line_detail_df = line_detail_df.groupby('光缆段')['详细'].agg(lambda x: ','.join(x)).reset_index().rename(columns={'光缆段':'名称'})
        line_df = line_df.merge(line_detail_df,on='名称',how='left')

        line_df['中继段数'] = line_df['中继段数'].fillna(0).astype('int')
        not_use_line_df = line_df[line_df['纤芯占用率']==0]
        # 统计表
        table = pd.pivot_table(not_use_line_df,index=['维护部门'],aggfunc={'名称':'count'})
        table = table.reset_index().rename(columns={'名称':'零利用率光缆段数'})

        # 子表1 纤芯占用率为0 且 中继段数为0
        sub_df_1 = not_use_line_df[not_use_line_df['中继段数']==0]
        table1 = pd.pivot_table(sub_df_1,index=['维护部门'],aggfunc={'名称':'count'})
        table1 = table1.reset_index().rename(columns={'名称':'零利用率光缆段数-无中继段'})
        table = table.merge(table1,on='维护部门',how='left')
        # 子表2 纤芯占用率为0 且 纤芯占用数不为0
        sub_df_2 = not_use_line_df[not_use_line_df['纤芯占用数']>0]
        table2 = pd.pivot_table(sub_df_2,index=['维护部门'],aggfunc={'名称':'count'})
        table2 = table2.reset_index().rename(columns={'名称':'零利用率光缆段数-实际有占用'})
        table = table.merge(table2,on='维护部门',how='left')
        # 子表3 纤芯占用率为0 且 纤芯占用数确实为0 且 中继段数不为0
        sub_df_3 = not_use_line_df[(not_use_line_df['纤芯占用数']==0) & (not_use_line_df['中继段数']>0)]
        table3 = pd.pivot_table(sub_df_3,index=['维护部门'],columns=['时间类型'],aggfunc={'名称':'count'})
        table3.columns = table3.columns.droplevel(0)
        table3 = table3.reset_index().rename(columns={
            '未满1年':'实际无占用-未满1年',
            '满1年未满2年':'实际无占用-满1年未满2年',
            '满2年未满3年':'实际无占用-满2年未满3年',
            '满3年以上':'实际无占用-满3年以上'
        })
        table = table.merge(table3,on='维护部门',how='left')
        table4 = pd.pivot_table(sub_df_3,index=['维护部门'],aggfunc={'名称':'count'})
        table4 = table4.reset_index().rename(columns={'名称':'零利用率光缆段数-实际无占用'})
        table = table.merge(table4,on='维护部门',how='left')
        table = table.fillna(0)
        table.set_index('维护部门',inplace=True)
        table.loc['合计'] = table.sum()
        table = table.reset_index()
        return table,not_use_line_df,sub_df_1,sub_df_2,sub_df_3


    def timeType(self,inSys_time):
        if pd.isna(inSys_time):
            return "满3年以上"
        # 根据时间判别未满一年，满一年未满两年，满两年未满三年，满三年以上
        now = pd.Timestamp.now()
        one_year_ago = now - pd.DateOffset(years=1)  # 1年前
        two_years_ago = now - pd.DateOffset(years=2)  # 2年前
        three_years_ago = now - pd.DateOffset(years=3)  # 3年前
        # 按区间判断
        if inSys_time >= one_year_ago:
            return "未满1年"
        elif inSys_time >= two_years_ago:
            return "满1年未满2年"
        elif inSys_time >= three_years_ago:
            return "满2年未满3年"
        else:
            return "满3年以上"


# 机房箱体分纤点级别定义业务逻辑
'''直连纤芯需要12芯以上，二级分纤点机房为本地接入；
1、OLT机房、汇聚机房：一级分纤点
2、直达一级机房：288以上【光交箱】：一级分纤点
3、直达一级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点
4、直达二级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点；循环次数4次
5、集群光交箱：就高的箱体级别
6、归属机房的光交箱、分纤箱：按照机房的分纤点级别
'''
class BoxLevelThread(QThread):
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
        point_df = self.houseLevel(house_df,olt_df)
        line_df = readDataBase('中继段')
        box_df = readDataBase('光交箱')
        oBox_df = readDataBase('分纤箱')
        box_grp_df = readDataBase('集群管理')
        self.state_signal.emit(f'已完成一级机房分析，共{point_df.shape[0]}个分纤点')
        point_df = self.getLevel(house_df,point_df,line_df,box_df,oBox_df,box_grp_df)
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
        point_df = house_df[['机房名称','业务级别']].copy().rename(columns={'机房名称':'分纤点名称','业务级别':'细分'})
        olt_house_df = olt_df[['所属机房']].copy().rename(columns={'所属机房':'分纤点名称'}).drop_duplicates()
        olt_house_df['细分'] = 'OLT机房'
        point_df = pd.concat([point_df,olt_house_df],ignore_index=True)
        point_df = point_df.groupby('分纤点名称')['细分'].apply(lambda x: ','.join(x)).reset_index()
        point_df['类型'] = '机房'
        point_df['级别'] = 1
        return point_df

    def getLevel(self,house_df,point_df,line_df,box_df,oBox_df,box_grp_df):
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
        temp_df = point_df[['分纤点名称']].copy().rename(columns={'分纤点名称':'始端机房'})
        link_to_level1_house = line_df.merge(temp_df,on='始端机房')

        # 判断直达一级机房的288以上光交箱；
        box_288up_df = box_df[box_df['容量']>=288].copy()
        box_288up_df = box_288up_df[['设施名称','容量']].rename(columns={'设施名称':'终端设施'})
        first_box = link_to_level1_house.merge(box_288up_df,on='终端设施')
        first_box = first_box[['终端设施','始端机房']].drop_duplicates(subset=['终端设施'],keep='first').rename(columns={'终端设施':'分纤点名称'})
        first_box['级别'] = 1
        first_box['类型'] = '光交箱'
        first_box['细分'] = '直达一级机房:' + first_box['始端机房']
        step_1_box = first_box[['分纤点名称','级别','细分','类型']].drop_duplicates()
        point_df = pd.concat([point_df,step_1_box],ignore_index=True)
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
        temp_df = line_df[['分纤点名称','设施类型','始端']]
        temp_df = temp_df.drop_duplicates(subset=['分纤点名称'],keep='first')
        temp_df['级别'] = 2
        temp_df['细分'] = f'第{run_count}轮二级分纤点分析出，上联：'+temp_df['始端']
        temp_df['类型'] = temp_df['设施类型']
        temp_df = temp_df[['分纤点名称','级别','细分','类型']]
        point_df = pd.concat([point_df,temp_df],ignore_index=True)
        return point_df

    def notLevelDev(self,dev_df,point_df):
        '''分析未有级别的分纤点设施'''
        not_level_dev = dev_df.merge(point_df,on='分纤点名称',how='left')
        not_level_dev = not_level_dev[not_level_dev['级别'].isnull()][['分纤点名称','设施类型']]
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
        box_df = box_df[['设施名称','机房名称']].rename(columns={'设施名称':'分纤点名称'})
        box_df['设施类型'] = '光交箱'
        oBox_df = oBox_df[oBox_df['容量']>=96]
        oBox_df = oBox_df[['设施名称','机房名称']].rename(columns={'设施名称':'分纤点名称'})
        oBox_df['设施类型'] = '分纤箱'

        house_box_df = pd.concat([box_df,oBox_df],ignore_index=True)

        temp_df = house_box_df[['分纤点名称','设施类型']]
        dev_df = pd.concat([temp_df,house_df],ignore_index=True)
        dev_df = dev_df.drop_duplicates()

        house_box_df['机房名称'] = house_box_df['机房名称'].fillna('')
        house_box_df['机房名称'] = house_box_df['机房名称'].astype(str)
        house_box_df = house_box_df[house_box_df['机房名称']!='']

        return dev_df,house_box_df


# 机房箱体分纤点级别定义业务逻辑
'''直连纤芯需要12芯以上，二级分纤点机房为本地接入；
1、汇聚机房：一级分纤点
2、直达一级机房：576以上【光交箱】：一级分纤点
3、OLT机房：一级分纤点
3、直达一级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点
4、直达二级分纤点的设施【光交箱+96芯以上分纤箱+本地接入机房】：定义为二级分纤点；循环次数4次
5、集群光交箱：就高的箱体级别
6、归属机房的光交箱、分纤箱：按照机房的分纤点级别
'''
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
class OltKnowledgeThread(QThread):
    error_signal = Signal(str)
    state_signal = Signal(str)
    def __init__(self, parent=None,output_path=None):
        super().__init__(parent)
        self.output_path = output_path
    
    def run(self):
        '''
        运程函数，读取OLT表格，然后获取OLT的markdown格式文档
        '''
        if self.tableNotRequired():
            error_str =  '数据库不存在这些表格：' + '、'.join(self.tableNotRequired())
            self.error_signal.emit(f'OLT网元数据集表格{error_str}')
            return;
        olt_df = readDataBase('OLT网元数据集')
        detail_cols = ['用户数','PON口总数','PON口空闲数','XGPON口总数','XGPON口空闲数']
        for col in detail_cols:
            olt_df[col] = olt_df[col].astype(int).astype(str)
        olt_df['详细信息'] = '网元:' + olt_df['OLT网元'] + ' 设备型号:'+ olt_df['设备型号'] + ' '
        for col in detail_cols:
            olt_df['详细信息'] += col + ':' + olt_df[col] + ' '
        olt_df = olt_df[['所属站点','详细信息']]
        # 只布放100个点的测试数据
        # olt_df = olt_df.head(100)
        result = dfToMarkdownKnowledge(olt_df,self.output_path)
        if result[0]:
            self.state_signal.emit(f'OLT网元知识库已生成，路径：{self.output_path}')
        else:
            self.error_signal.emit(result[1])

    def tableNotRequired(self):
        '''
        校验数据库表格是否存在满足，一次返回不满足的表格清单
        '''
        check_tales = ['OLT网元数据集']
        conn = sqlite3.connect('data/TransportNetwork.db')
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]
        not_required_tables = [table for table in check_tales if table not in tables]
        return not_required_tables

'''
箱体及箱体上联方案的进程，读取箱体表、上联方案表，然后分别输出箱体及上联方案markdown知识库文档
'''
class BoxKnowledgeThread(QThread):
    error_signal = Signal(str)
    state_signal = Signal(str)
    def __init__(self, parent=None,output_dir=None):
        super().__init__(parent)
        self.output_dir = output_dir
    
    def run(self):
        '''
        运程函数，读取箱体表、上联方案表，然后分别输出箱体及上联方案markdown知识库文档
        '''
        if self.tableNotRequired():
            self.error_signal.emit('数据库不存在这些表格：' + '、'.join(self.tableNotRequired()))
            return;
        self.state_signal.emit('开始读取箱体清单...')
        all_dev = readBoxKnowledge()
        # 测试只取200数据测试，正式版全选
        # all_dev = all_dev.head(200)
        all_dev = self.getAllDev(all_dev)
        self.state_signal.emit('箱体清单读取完成')
        self.state_signal.emit('开始读取箱体上联方案...')
        grped = all_dev.groupby('所属区县')
        self.state_signal.emit('正在生成箱体知识库...')
        for area,group in grped:
            all_dev, uplink_df = self.getDevUplink(group)
            now = datetime.datetime.now().strftime('%Y%m%d%H%M')
            self.devToKnowledge(all_dev,now,area)
            self.uplinkToKnowledge(uplink_df,now,area)
        self.state_signal.emit('已完成')


    def uplinkToKnowledge(self,uplink_df,now,area):
        '''
        将箱体上联方案表转换为Dify知识库格式的Markdown文档
        '''
        uplink_df['跳纤路径'] = uplink_df['跳纤路径'].apply(self.fixPonLine)
        uplink_df['详细信息'] = '设施名称:' + uplink_df['设施名称'] + ' '
        uplink_df['最小空闲芯数'] = uplink_df['最小空闲芯数'].astype(int)

        uplink_df = uplink_df.astype(str)
        uplink_df['详细信息'] = uplink_df['详细信息'] + '上联机房:' + uplink_df['目标OLT机房'] + '【' + uplink_df['机房详细信息'] + '】 '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '上联路由:' + uplink_df['跳纤路径'] + ' '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '【空闲芯数:' + uplink_df['最小空闲芯数'] + '芯 | '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '跳纤距离:' + uplink_df['跳纤距离'] + 'km | '
        uplink_df['详细信息'] = uplink_df['详细信息'] + '光衰预算:' + uplink_df['光衰预算'] + 'dB】'

        uplink_df = uplink_df[['设施名称','详细信息']]
        uplink_df = uplink_df.drop_duplicates()
        flag,result = dfToMarkdownKnowledge(uplink_df,self.output_dir+'/箱体上联方案_'+area+'_'+now+'.md')
        if flag:
            self.state_signal.emit(result)
        else:
            self.error_signal.emit(result)

    def fixPonLine(self,path):
        '''
        修正跳纤路径，只保留跳纤信息
        '''
        path = '=>' + path + '<='
        points = re.findall('=>(.*?)<=',path)
        path = '《=》'.join(points)
        return path



    def devToKnowledge(self,all_dev,now,area):
        '''
        将箱体清单和上联方案表转换为Dify知识库格式的Markdown文档
        '''
        all_dev = all_dev[['设施名称','所属区县','所属镇街','经度','纬度','容量']]
        all_dev = all_dev.reset_index(drop=True)
        all_dev = all_dev.fillna('').astype(str)
        all_dev['详细信息'] = (
            '设施名称:' + all_dev['设施名称'] + ' ' +
            all_dev['所属区县'] + ' ' +
            all_dev['所属镇街'] + ' ' +
            '容量:' + all_dev['容量']
        )
        all_dev = all_dev[['设施名称','详细信息']]
        all_dev = all_dev.drop_duplicates()
        flag,result = dfToMarkdownKnowledge(all_dev,self.output_dir+'/箱体清单_'+area+'_'+now+'.md')
        if flag:
            self.state_signal.emit(result)
        else:
            self.error_signal.emit(result)


    def loadOltHouseCount(self):
        '''
        读取OLT网元数据集，统计每个OLT机房的情况
        '''
        df = readDataBase('OLT网元数据集')
        df_model_count = df.groupby(['所属机房', '设备型号']).size().reset_index(name='设备台数')
        # 把每个机房下的【型号: 台数】拼成字符串
        model_str = df_model_count.groupby('所属机房').apply(
            lambda x: '、'.join([f"{row['设备型号']}({row['设备台数']}台)" for _, row in x.iterrows()])
        ).reset_index(name='设备型号统计')
        # 2. 按机房汇总所有端口总数
        df_port = df.groupby('所属机房').agg(
            PON口总数汇总=('PON口总数', 'sum'),
            PON口空闲数汇总=('PON口空闲数', 'sum'),
            XGPON口总数汇总=('XGPON口总数', 'sum'),
            XGPON口空闲数汇总=('XGPON口空闲数', 'sum')
        ).reset_index()
        # 3. 合并统计结果
        result_df = pd.merge(model_str, df_port, on='所属机房')

        # 4. 拼接成【详细信息】列
        result_df['机房详细信息'] = (
            '设备情况：' + result_df['设备型号统计'] +
            ' | PON口数：' + result_df['PON口总数汇总'].astype(int).astype(str) +
            ' | PON口空闲数：' + result_df['PON口空闲数汇总'].astype(int).astype(str) +
            ' | XGPON口数：' + result_df['XGPON口总数汇总'].astype(int).astype(str) +
            ' | XGPON口空闲数：' + result_df['XGPON口空闲数汇总'].astype(int).astype(str)
        )
        # 5. 最终只保留 2 列
        house_df = result_df[['所属机房', '机房详细信息']].drop_duplicates().rename(columns={'所属机房':'目标OLT机房'})
        return house_df

    def getAllDev(self,all_dev):
        # 只提取72个PON口以上的箱体和已开主光路的箱体
        pon_line = readDataBase('主光路')[['OBD所属对象']].drop_duplicates().rename(columns={'OBD所属对象':'设施名称'})
        pon_line = pd.merge(all_dev,pon_line,on='设施名称')
        all_dev = all_dev[all_dev['容量']>=72]
        all_dev = pd.concat([all_dev,pon_line],ignore_index=True)
        all_dev = all_dev.drop_duplicates()
        return all_dev

    def getDevUplink(self,all_dev):
        # 读取箱体上联OLT跳纤路径表
        uplink_df = readDataBase('箱体上联OLT跳纤路径表')
        temp_df = all_dev[['设施名称']].copy().drop_duplicates()
        uplink_df = uplink_df[uplink_df['目标OLT机房']!='']
        uplink_df = uplink_df.groupby(['设施名称','目标OLT机房']).first().reset_index()
        uplink_df = uplink_df.merge(temp_df,on='设施名称')
        uplink_df = uplink_df.drop_duplicates()
        house_df = self.loadOltHouseCount()
        uplink_df = uplink_df.merge(house_df,on='目标OLT机房')
        uplink_df = uplink_df.drop_duplicates()
        temp_df = uplink_df[['设施名称']].copy().drop_duplicates()
        all_dev = all_dev.merge(temp_df,on='设施名称')
        all_dev = all_dev.drop_duplicates()
        return all_dev,uplink_df

    def tableNotRequired(self):
        '''
        校验数据库表格是否存在满足，一次返回不满足的表格清单
        '''
        check_tales = ['分纤箱','光交箱','ODF','箱体上联OLT跳纤路径表','OLT网元数据集']
        conn = sqlite3.connect('data/TransportNetwork.db')
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        tables = [table[0] for table in tables]
        not_required_tables = [table for table in check_tales if table not in tables]
        return not_required_tables


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
class UpdateOneKeyQThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)
    
    def __init__(self, folder_path=''):
        super().__init__()
        self.folder_path = folder_path
        self.file_type_cols = [
            'OLT网元', '主光路', 'PON端口', '中继段', '光缆段', '站点', '机房', '光交箱', '分纤箱', 'ODF', '集群管理', '华为PON单板','中兴PON单板'
        ]
        self.file_cols = [
            (['网元名称', '所属机房', '设备型号', '设备IP','生命周期状态'],['str','str','str','str','str']),
            (['OLT名称', 'PON口', 'PON下挂ONU数量', 'OBD所属对象', '光路名称', '光路长度','光路文本路由'],['str','str','int','str','str','float','str']),
            (['所属传输网元', '端口名称', 'PONID', '端口状态', 'PON口下挂用户数', '端口子类型'],['str','str','str','str','int','str']),
            (['名称', '长度', '空闲数量', '占用数量', '中继纤芯数量', '始端站点', '终端站点', '始端机房','终端机房', '始端设施', '终端设施'],['str','float','int','int','int','str','str','str','str','str','str']),
            (['名称','所属光缆','实际长度','纤芯占用率','光纤数目','业务级别','敷设方式','维护部门','红线范围','初验时间','资源状态'],['str','str','float','float','int','str','str','str','str','str','str']),
            (['站点名称', '所属区县', '乡镇街道'],['str','str','str']),
            (['所属站点', '机房类型', '机房名称', '业务级别', '生命周期状态'],['str','str','str','str','str']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设施名称', '机房名称', '所属综合业务区','所属区县', '所属镇街','分纤点级别', '容量','经度','纬度'],['str','str','str','str','str','str','int','float','float']),
            (['设备名称','集群列表'],['str','str']),
            (['所属网元','槽位号','单板类型','单板状态'],['str','str','str','str']),
            (['网元名称','板卡槽位','板卡类型','板卡状态'],['str','str','str','str']),
        ]
        self.file_rules = [
            {'keyword': 'OLT设备', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {'所属位置点/机房': '所属机房', '设备IP地址（省内系统：网管IP）': '设备IP'}},
            {'keyword': '主光路', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': 'PON端口', 'file_type': 'xlsx', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '中继段', 'file_type': 'CSV', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '光缆段', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '站点管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '机房管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '光交接箱', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '光分纤箱', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': 'ODF', 'file_type': 'CSV', 'single': False, 'header': 0, 'rename_cols': {}},
            {'keyword': '集群管理', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
            {'keyword': '单板报表', 'file_type': 'xlsx', 'single': True, 'header': 3, 'rename_cols': {}},
            {'keyword': 'card_query', 'file_type': 'xlsx', 'single': True, 'header': 0, 'rename_cols': {}},
        ]
    
    def run(self):
        try:
            self.state_signal.emit('开始检查需求文件...')
            missing_files = self.check_required_files()
            if missing_files:
                self.error_signal.emit('缺失以下必需文件：\n' + '\n'.join(missing_files))
                return
            
            self.state_signal.emit('文件检查通过，开始导入数据...')
            conn = sqlite3.connect('data/transportNetwork.db')
            cursor = conn.cursor()
            
            for i, table_name in enumerate(self.file_type_cols):
                self.state_signal.emit(f'正在导入 {table_name}...')
                df = self.read_table_data(i)
                if df.empty:
                    self.state_signal.emit(f'{table_name} 数据为空，跳过')
                    continue
                if table_name == '中继段':
                    self.convertLine(df, cursor)
                if table_name == 'OLT网元':
                    df = self.selectOLT(df)
                # 筛选数据    
                df = self.process_data(df, i)

                df.to_sql(table_name, conn, if_exists='replace', index=False)
                self.update_table_time(cursor, table_name)
                

                
                conn.commit()
                self.state_signal.emit(f'{table_name} 导入完成，共 {len(df)} 条记录')
            
            conn.close()
            self.state_signal.emit('一键更新数据库完成！')
        
        except Exception as e:
            self.error_signal.emit(f'一键更新数据库失败: {str(e)}')
    
    def update_table_time(self, cursor, table_name):
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M')
        cursor.execute("SELECT COUNT(*) FROM 表格更新时间 WHERE 表名=?", (table_name,))
        if cursor.fetchone()[0] > 0:
            cursor.execute("UPDATE 表格更新时间 SET 更新时间=? WHERE 表名=?", (now, table_name))
        else:
            cursor.execute("INSERT INTO 表格更新时间 (表名, 更新时间) VALUES (?, ?)", (table_name, now))
    
    def selectOLT(self, df):
        df = df.astype(str)
        df = df[~df['生命周期状态'].str.contains('退网')]
        df = df[df['生命周期状态']!='工程无业务']
        df = df[df['生命周期状态']!='工程在建']
        return df
    
    def convertLine(self, df, cursor):
        value_vars = df.columns.tolist()[16:]
        result = df.melt(id_vars=['名称'], value_vars=value_vars, value_name='光缆段').drop(columns=['variable'])
        result = result.reset_index(drop=True)
        result = result[result['光缆段'].notnull()]
        result.rename(columns={'名称': '中继段'}, inplace=True)
        result.to_sql('中继段至光缆段', cursor.connection, if_exists='replace', index=False)
        self.update_table_time(cursor, '中继段至光缆段')
        cursor.connection.commit()
        self.state_signal.emit('中继段至光缆段 导入完成')
    
    def check_required_files(self):
        missing_files = []
        files = os.listdir(self.folder_path)
        
        for i, rule in enumerate(self.file_rules):
            found = False
            for file in files:
                if rule['keyword'] in file and file.endswith('.' + rule['file_type']):
                    found = True
                    break
            if not found:
                missing_files.append(f"{self.file_type_cols[i]}: 需要包含'{rule['keyword']}'的{rule['file_type']}文件")
        
        return missing_files
    
    def read_table_data(self, index):
        rule = self.file_rules[index]
        files = os.listdir(self.folder_path)
        matched_files = [f for f in files if rule['keyword'] in f and f.endswith('.' + rule['file_type'])]
        
        dfs = []
        for file in matched_files:
            file_path = os.path.join(self.folder_path, file)
            if rule['file_type'] == 'xlsx':
                df = pd.read_excel(file_path, header=rule['header'])
            else:
                df = readCsvFile(file_path, header=rule['header'])
            dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        return pd.concat(dfs, ignore_index=True)
    
    def process_data(self, df, index):
        table_cols = self.file_cols[index][0]
        col_types = self.file_cols[index][1]
        rename_cols = self.file_rules[index]['rename_cols']
        
        df = df.rename(columns=rename_cols)
        
        df = df[[col for col in table_cols if col in df.columns]]
        
        for i, col in enumerate(table_cols):
            if col in df.columns:
                if col_types[i] == 'int':
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                elif col_types[i] == 'float':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.drop_duplicates()
        
        return df