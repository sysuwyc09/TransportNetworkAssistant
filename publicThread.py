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
        # 按500一组进行分组，如果最后一组不足500则为剩余值
        obds_groups = [obds[i:i+500] for i in range(0, len(obds), 500)]
        result_dfs = []
        start_time = time.time()
        for i,obds_group in enumerate(obds_groups):
            temp_df = dispatchToMany(obds_group,line2Df,oltDf)
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
                    out_file_name = f'结果\\{self.a_name}_{self.b_name}_跳纤路径{dt}.xlsx'
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
