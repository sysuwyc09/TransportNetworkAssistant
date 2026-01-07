# 存放公共函数的模块

import sqlite3
import os   
import pandas as pd
import datetime
import numpy as np
import math
import cchardet
import re


line2TableCols = ['中继段名称','A端','B端','长度','纤芯总数','空闲芯数']
dispatchOneToManyCols = ['A端','B端','最小空闲芯数','跳纤距离','跳数','光衰预算','跳纤路径','B端类型']


# 读取光设施的清单
def readDevs():
    sql = '''
        SELECT dev.设施名称, dev.机房名称, dev.所属综合业务区
        FROM (
            SELECT 设施名称,机房名称,所属综合业务区 FROM 光交箱
            UNION ALL
            SELECT 设施名称,机房名称,所属综合业务区 FROM 分纤箱 WHERE 容量 >= 72
            UNION ALL
            SELECT 设施名称,机房名称,所属综合业务区 FROM ODF
            
        ) as dev
    '''
    all_dev = queryDataBase(sql)
    return all_dev



# 分析跳纤至OLT的路径
def dispatchToOlt(obds,line_df):
    siteDf = pd.DataFrame({'第1跳':obds,'跳纤路径':obds})
    siteDf['最小空闲芯数'] = 300
    siteDf['跳纤距离'] = 0
    # 修改初始OBD算1跳
    siteDf['跳数'] = 1
    siteDf['光衰预算'] = 0
    resultDf = pd.DataFrame()
    #6条内达到 B站点的 全部路径,待修正跳数        
    for num in range(1,7):
        step = '第' + str(num) + '跳'
        siteDf.rename(columns={step:'A端'},inplace=True)
        siteDf = siteDf.merge(line_df,on='A端')
        if siteDf.shape[0] == 0:
            return resultDf
        else:
            nextStep = '第' + str(num+1) + '跳'
            lineName = '中继段' + str(num)
            leftName = '空闲芯数' + str(num)
            numName = '纤芯总数' + str(num)
            lenName = '长度' + str(num)
            siteDf.rename(columns={'A端':step,'B端':nextStep,'中继段名称':lineName,'空闲芯数':leftName,\
                '纤芯总数':numName,'长度':lenName},inplace=True)
            #杜绝跳纤回原来跳纤已经过站点
            for j in range(1,num):
                upStep = '第' + str(num-j) + '跳'
                siteDf = siteDf[siteDf[upStep] != siteDf[nextStep]]            
            #结算跳纤距离，跳数，光衰预算
            siteDf['跳纤距离'] = round(siteDf['跳纤距离'] + siteDf[lenName],2)
            siteDf['跳数'] = siteDf['跳数'] + 1
            siteDf['光衰预算'] = round(siteDf['跳纤距离'] * 0.35 + siteDf['跳数'] * 1,2)  # 按跳纤距离0.35dB 1跳 1dB估算
            # siteDf.to_csv(f'test{num}.csv',encoding='ANSI')
            siteDf = siteDf[siteDf['光衰预算'] < 9]
            if siteDf.shape[0] ==0:
                resultDf = resultDf.reset_index()
                if resultDf.shape[0] >0:
                    resultDf = resultDf[dispatchOneToManyCols]
                return resultDf

            #计算空闲纤芯
            siteDf['最小空闲芯数'] = CompareMin(siteDf[leftName],siteDf['最小空闲芯数'])                
            #统计跳纤路径
            siteDf = siteDf.astype({'最小空闲芯数':'str',numName:'str',leftName:'str'})
            siteDf['跳纤路径'] = siteDf['跳纤路径'] + '<={' + siteDf[lineName] + '}(' + siteDf[leftName] + '/' + siteDf[numName] +')=>' + siteDf[nextStep]
            siteDf = siteDf.astype({'最小空闲芯数':'int',numName:'int',leftName:'int'})
                            
            #保存跳纤结果
            #处理siteDf,只保留 每组A-最后纤芯最多的5项
            siteDf.sort_values(by=['第1跳',nextStep,'最小空闲芯数',leftName],ascending=[False,False,False,False],inplace=True)
            siteDf = siteDf.groupby(['第1跳',nextStep]).head()
            
            #按光功率排序
            siteDf.sort_values(by=['光衰预算'],ascending=[True],inplace=True)

            tempResultDf = siteDf[siteDf['B端类型'] == 'OLT'].copy()
            if tempResultDf.shape[0] > 0:
                tempResultDf.rename(columns={'第1跳':'A端',nextStep:'B端'},inplace=True)
                tempResultDf = tempResultDf[dispatchOneToManyCols]
                resultDf = pd.concat([resultDf,tempResultDf])
            siteDf = siteDf[siteDf['B端类型'] != 'OLT']
            #删除B端类型这一列
            siteDf = siteDf.drop(['B端类型'],axis=1)
            if siteDf.shape[0] == 0:
                break
    resultDf = resultDf.reset_index()
    if resultDf.shape[0] >0:
        resultDf = resultDf[dispatchOneToManyCols]
    return resultDf

def selectBestPath(df):

    # 评估方案得分，算法如下：
    df['最小空闲芯数得分'] =  df['最小空闲芯数'].apply(lambda x: x if x<=10 else 10)
    df['方案得分'] = round(df['最小空闲芯数得分']/df['光衰预算'],2)
    df.drop(columns=['最小空闲芯数得分'],inplace=True)
    # 1. 芯数最多的前5行 (每组)
    df_max5_fiber = df.sort_values(['A端', '最小空闲芯数'], ascending=[True, False]).groupby('A端').head()
    # 2 光衰最低的前5行 (每组)
    df_min_attenuation = df.sort_values(['A端', '光衰预算'], ascending=[True, True]).groupby('A端').head()
    # 3. 评分最高的前5行 (每组)
    df_top5_score = df.sort_values(['A端', '方案得分'], ascending=[True, False]).groupby('A端').head()
    # 合并结果 (可选)
    result = pd.concat([
        df_max5_fiber,
        df_min_attenuation,
        df_top5_score
    ])
    result = result.drop_duplicates()
    return result

    
@np.vectorize
def CompareMin(x,y):
    if x < y:
        return x
    else:
        return y

@np.vectorize
def fixSite(x,y):
    if pd.isnull(x):
        return y
    else:
        if len(x) == 0:
            return y
        return x
    
def loadLine2Df():
    conn = sqlite3.connect('data/transportNetwork.db')
    sql = '''
    SELECT *
    FROM 中继段
    '''
    line2Df = pd.read_sql_query(sql,conn)
    line2Df['A端'] = fixSite(line2Df['始端机房'],line2Df['始端设施'])
    line2Df['B端'] = fixSite(line2Df['终端机房'],line2Df['终端设施'])
    line2Df = line2Df[line2Df['A端'] != line2Df['B端']]
    line2Df.rename(columns={'名称':'中继段名称','空闲数量':'空闲芯数','中继纤芯数量':'纤芯总数'},inplace=True)
    line2Df = line2Df[line2TableCols]
    line2Df = line2Df.dropna()
    line2Df['长度'] = round(line2Df['长度']/1000,3)
    line3Df = line2Df.copy()
    line3Df.rename(columns={'A端':'B端','B端':'A端'},inplace=True)
    line2Df = pd.concat([line2Df,line3Df])
    #减少内存
    line2Df['长度'] = pd.to_numeric(line2Df['长度'],errors='coerce',downcast='float')
    line2Df['纤芯总数'] = line2Df['纤芯总数'].astype('int16')
    line2Df = line2Df[line2Df['纤芯总数']>1]
    line2Df['空闲芯数'] = line2Df['空闲芯数'].astype('int16')
    sql = '''
    SELECT  所属机房 as B端
    FROM OLT网元
    WHERE 生命周期状态 == '现网有业务' OR 生命周期状态 == '现网无业务' OR 生命周期状态 == '工程有业务'
    '''
    oltDf = pd.read_sql_query(sql,conn)
    conn.close()
    oltDf['B端类型'] = 'OLT'
    line2Df = line2Df.merge(oltDf,how='left',on='B端')
    return line2Df


"""写文件"""
def writeDoc(name,folders):
    doc = header(name)
    for folder in folders:
        doc = doc + folder
    doc = doc + '</Document>\n</kml>\n'
    return doc
"""写文件夹"""
def writeFolder(name,places):
    folderStr = '\t<Folder>\n'
    folderStr = folderStr + '\t'*2 + '<name>' + name + '</name>\n'
    for place in places:
        folderStr = folderStr + place
    folderStr =  folderStr + '\t</Folder>\n'
    return folderStr

"""写机房位置"""
def writePoint(name,longitude,latitude):
    placeMark = '\t'*2 + '<Placemark>\n'
    placeMark = placeMark + '\t'*3 + '<name>' + name + '</name>\n'
    placeMark = placeMark + '\t'*3 + '<Style>\n'
    placeMark = placeMark + '\t'*3 + '<IconStyle>\n'
    placeMark = placeMark + '\t'*4 + '<Icon>\n'
    placeMark = placeMark + '\t'*5 + '<href>http://maps.google.com/mapfiles/kml/shapes/ranger_station.png</href>\n'
    placeMark = placeMark + '\t'*4 + '</Icon>\n'
    placeMark = placeMark + '\t'*4 + '<color>ffffffff</color>\n'
    placeMark = placeMark + '\t'*4 + '<scale>1.0</scale>\n'
    placeMark = placeMark + '\t'*3 + '</IconStyle>\n'
    placeMark = placeMark + '\t'*3 + '<LabelStyle><color>00ffff00</color></LabelStyle>\n'
    placeMark = placeMark + '\t'*3 + '</Style>\n'
    placeMark = placeMark + '\t'*3 + '<Point>\n'
    placeMark = placeMark + '\t'*4 + '<coordinates>' + str(longitude) + ',' + str(latitude) + ',0</coordinates>\n'
    placeMark = placeMark + '\t'*3 + '</Point>\n'
    placeMark = placeMark + '\t'*2 + '</Placemark>\n'
    return placeMark

'''写机房覆盖范围'''
def writePolygon(name,coord,description=''):
    placeMark = '\t'*2 + '<Placemark>\n'
    placeMark = placeMark + '\t'*3 + '<name>' + name + '</name>\n'
    placeMark = placeMark + '\t'*3 + '<description>' + description + '</description>\n'
    placeMark = placeMark + '\t'*3 + '<Style>\n'
    placeMark = placeMark + '\t'*4 + "<LineStyle><color>ffff0000</color><width>3</width></LineStyle>\n"
    placeMark = placeMark + '\t'*4 + "<PolyStyle><color>80ff0000</color></PolyStyle>\n"
    placeMark = placeMark + '\t'*3 + '</Style>\n'
    placeMark = placeMark + '\t'*3 + '<Polygon>\n'
    placeMark = placeMark + '\t'*4 + '<outerBoundaryIs>\n'
    placeMark = placeMark + '\t'*5 + '<LinearRing>\n'
    placeMark = placeMark + '\t'*6 + '<coordinates>\n'
    placeMark = placeMark + '\t'*7 + coord + '\n'
    placeMark = placeMark + '\t'*6 + '</coordinates>\n'
    placeMark = placeMark + '\t'*5 + '</LinearRing>\n'
    placeMark = placeMark + '\t'*4 + '</outerBoundaryIs>\n'
    placeMark = placeMark + '\t'*3 + '</Polygon>\n'
    placeMark = placeMark + '\t'*2 + '</Placemark>\n'
    return placeMark

#kml文件头
def header(name):
    str = '<?xml version="1.0" encoding="UTF-8"?>'
    str = str + '\n' + '<kml xmlns=\"http://www.opengis.net/kml/2.2\" \n'
    str = str + '\t' + 'xmlns:atom=\"http://www.w3.org/2005/Atom\"  \n'
    str = str + '\t' + 'xmlns:gx="http://www.google.com/kml/ext/2.2"  \n'
    str = str + '\t>\n'
    str = str + '<Document>\n'
    str = str + '\t<name>' + name + '</name>\n'
    return str

#输出文件
def writeAggrHouseKml(file_path):
    """
    写汇聚机房kml文件
    :param polyDf: 汇聚机房数据框
    :return: None
    """
    sql ='''
        select j.*,o.经度, o.纬度
        from 机房 j 
        join ODF o on o.机房名称 = j.机房名称
    '''
    poly_df = queryDataBase(sql)
    poly_df['是否退网'] = poly_df['生命周期状态'].apply(lambda x: '是' if '退网' in str(x) else '否')
    poly_df = poly_df[poly_df['是否退网'] == '否']
    poly_df['是否汇聚'] = poly_df['业务级别'].apply(lambda x: '是' if '汇聚' in str(x) else '否')
    poly_df = poly_df[poly_df['是否汇聚'] == '是']
    poly_df = poly_df[['所属站点','经度','纬度']].drop_duplicates()
    places = []
    names = list(poly_df['所属站点'])
    lons = list(poly_df['经度'])
    lats = list(poly_df['纬度'])
    for i in range(len(names)):
        poly_coord = kml_circle_coord(lons[i],lats[i],7)
        places.append(writePolygon(names[i],poly_coord))
        places.append(writePoint(names[i],lons[i],lats[i]))
    folders = [writeFolder('汇聚机房覆盖',places)]
    outStr = writeDoc('汇聚机房覆盖',folders)
    with open(file_path,'w',encoding='UTF-8') as outFile:
        outFile.write(outStr)

def generate_circle_points(center_lon, center_lat, radius_km, num_points=100):
    """
    生成圆周上平均分布的点
    :param center_lon: 圆心经度
    :param center_lat: 圆心纬度
    :param radius_km: 半径(公里)
    :param num_points: 点的数量(默认100)
    :return: 包含所有点坐标的列表 [(lon1, lat1), (lon2, lat2), ...]
    """
    points = []
    earth_radius = 6371.0  # 地球半径(公里)
    
    for i in range(num_points):
        # 计算当前角度(弧度)
        angle = 2 * math.pi * i / num_points
        
        # 计算偏移量(使用Haversine公式)
        delta_lat = (radius_km / earth_radius) * math.cos(angle)
        delta_lon = (radius_km / (earth_radius * math.cos(math.radians(center_lat)))) * math.sin(angle)
        
        # 计算新点的坐标
        new_lat = center_lat + math.degrees(delta_lat)
        new_lon = center_lon + math.degrees(delta_lon)
        
        points.append((new_lon, new_lat))
    
    return points

def kml_circle_coord(center_lon,center_lat,radius_km):
    """"
    生成kml格式的圆坐标
    :param points: 包含所有点坐标的列表 [(lon1, lat1), (lon2, lat2),...]
    :return: kml格式的圆坐标字符串
    """
    points = generate_circle_points(center_lon,center_lat,radius_km)
    coord_str = ""
    for lon, lat in points:
        coord_str += f"{lon},{lat},0 "
    # 闭合圆
    coord_str += f"{points[0][0]},{points[0][1]},0 "
    return coord_str










# 根据sql查询数据库
def queryDataBase(sql,params=None):
    conn = sqlite3.connect('data/transportNetwork.db')
    df = pd.read_sql(sql, conn,params=params)
    conn.close()
    return df

# 划面板图数据
def drawOltBoard(olt_name):
    sql = '''SELECT * FROM PON口数据集 WHERE OLT网元 = ?'''
    params = (olt_name,)
    df = queryDataBase(sql,params)
    #OLT网元(TEXT), 端口名称(TEXT), 端口状态(TEXT), PON口下挂用户数(INTEGER), 槽位号(INTEGER), 端口号(INTEGER), 板卡名称(TEXT), 板卡类型(TEXT), PON口类型(TEXT)
    df = df[df['PON口类型']!='非PON口']
    df['端口状态值'] = df['端口状态'].apply(stateValue)
    df = df.sort_values(by=['槽位号','端口号'],ascending=[True,True])
    df['槽位号'] = df['槽位号'].astype(str)
    df['槽位板卡'] = standardBoardData(df['槽位号'],df['板卡类型'])
    dfgrp = df.groupby('槽位板卡')
    dict = {}
    for name,group in dfgrp:
        dict[name] = group['端口状态值'].to_list()

    return dict

@np.vectorize
def standardBoardData(board_id,board_type):
    # 标准板卡数据
    if len(board_id) == 1:
        return '0' + board_id + '-'+ board_type[-4:]
    else:
        return board_id + '-' + board_type[-4:]


def stateValue(value):
    if value == '空闲':
        return 0
    elif value == '占用':
        return 1
    else:
        return 2


def searchOltNeFunc(olt_name):
    # 搜索OLT网元
    sql = '''SELECT * FROM OLT网元数据集 WHERE 所属站点 = ?'''
    params = (olt_name,)
    df = queryDataBase(sql,params)
    # OLT网元(TEXT), 所属机房(TEXT), 设备型号(TEXT), 生命周期状态(TEXT), 所属站点(TEXT), 机房类型(TEXT), 机房状态(TEXT), PON口总数(REAL), PON口使用数(REAL), PON口空闲数(REAL), XGPON口总数(REAL), XGPON口使用数(REAL), XGPON口空闲数(REAL), 用户数(REAL)
    df = df[['OLT网元','设备型号','PON口使用数','PON口空闲数','XGPON口使用数','XGPON口空闲数','用户数']]
    # 'PON口使用数','PON口空闲数','XGPON口使用数','XGPON口空闲数','用户数'设置为 int类型
    df[['PON口使用数','PON口空闲数','XGPON口使用数','XGPON口空闲数','用户数']] = df[['PON口使用数','PON口空闲数','XGPON口使用数','XGPON口空闲数','用户数']].astype(int)
    df = df.rename(columns={'PON口使用数':'普通口使用数','PON口空闲数':'普通口空闲数','XGPON口使用数':'千兆口使用数','XGPON口空闲数':'千兆口空闲数'})
    pon_use_num = int(df['普通口使用数'].sum())
    xgpon_use_num = int(df['千兆口使用数'].sum())
    pon_left_num = int(df['普通口空闲数'].sum())
    xgpon_left_num = int(df['千兆口空闲数'].sum())
    pon_dict = {
        '使用数':pon_use_num,
        '空闲数':pon_left_num,
    }
    xgpon_dict = {
        '使用数':xgpon_use_num,
        '空闲数':xgpon_left_num,
    }
    return df,pon_dict,xgpon_dict

def searchOdevNameFunc(keyword):
    keys = keyword.split(' ')
    conditions = " AND ".join([f"设施名称 LIKE '%{key}%'" for key in keys])
    query = f"SELECT * FROM 箱体上联OLT跳纤路径表 WHERE {conditions}"
    df = queryDataBase(query)
    return df['设施名称'].unique()

def searchOdevUplinkFunc(odev_name):
    # 搜索光交设施上联路径
    sql = '''SELECT * FROM 箱体上联OLT跳纤路径表 WHERE 设施名称 = ?'''
    params = (odev_name,)
    df = queryDataBase(sql,params)
    # 设施名称(TEXT), 设施所属位置(TEXT), 目标OLT机房(TEXT), 最小空闲芯数(REAL), 跳纤距离(REAL), 跳数(REAL), 光衰预算(REAL), 跳纤路径(TEXT), 方案得分(REAL)
    df = df[['设施名称','目标OLT机房', '最小空闲芯数', '跳纤距离', '跳数', '光衰预算', '跳纤路径', '方案得分']]
    df = df.sort_values(by=['方案得分'],ascending=False)
    return df


def searchOltSiteFunc(keyword):
    # 搜索OLT站点
    conn = sqlite3.connect('data/transportNetwork.db')
    cursor = conn.cursor()
    # 判断数据库是否有 OLT网元数据集 表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='OLT网元数据集'")
    if cursor.fetchone() is None:
        return [],'OLT网元数据集表不存在'
    keys = keyword.split(' ')
    conditions = " AND ".join([f"所属站点 LIKE '%{key}%'" for key in keys])
    query = f"SELECT * FROM OLT网元数据集 WHERE {conditions}"
    df = pd.read_sql(query, conn)
    sites = df['所属站点'].unique()
    conn.close()
    return sites,'搜索成功'


def writeDataBase(table_name,df):
    conn = sqlite3.connect('data/transportNetwork.db')
    cursor = conn.cursor()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    # 更新 表格更新时间 表 table_name的更新时间 为当前时间
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M')
    # 判断表格是否存在并执行更新或插入操作
    cursor.execute("SELECT COUNT(*) FROM 表格更新时间 WHERE 表名=?", (table_name,))
    if cursor.fetchone()[0] > 0:
        cursor.execute("UPDATE 表格更新时间 SET 更新时间=? WHERE 表名=?", (now, table_name))
    else:
        cursor.execute("INSERT INTO 表格更新时间 (表名, 更新时间) VALUES (?, ?)", (table_name, now))
    conn.commit()

    conn.close()


def readDataBase(table_name):
    conn = sqlite3.connect('data/transportNetwork.db')
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    except Exception as e:
        df = pd.DataFrame()
    conn.close()
    return df

def clearDataBase(table_name):
    try:
        conn = sqlite3.connect('data/transportNetwork.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name}")
        conn.commit()
        conn.close()
        return "清除成功"
    except Exception as e:
        return f"清除失败: {str(e)}"


def initDB():
    # 判断数据库是否存在
    if not os.path.exists('data/transportNetwork.db'):
        # 如果不存在，则创建数据库
        conn = sqlite3.connect('data/transportNetwork.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE 表格更新时间(表ID INTEGER PRIMARY KEY, 表名 TEXT, 更新时间 TEXT)''')
        conn.commit()
        conn.close()


def get_list(str,lists):
    for i in range(0,len(str)-1):
        lists.append(str[i:i+2])


#从objs列表模糊匹配sourse最相似的字符串
def mostLike(sourse,objs):
    same = 0
    mark = ""
    for obj in objs:
        sourse_lists = []
        len_min = min(len(sourse),len(obj))
        if same < len_min:
            get_list(sourse,sourse_lists)
            tempsame=0
            for sourse_list in sourse_lists:
                if sourse_list in obj:
                    tempsame = tempsame + 1
            if tempsame > same:
                same = tempsame
                mark = obj
    return mark


def getCsvEncoding(file_path, sample_size=10240):
    """
    判别CSV文件的编码格式
    :param file_path: CSV文件路径
    :param sample_size: 读取的样本字节数（默认10KB，足够覆盖编码特征）
    :return: 编码名称（如utf-8、gbk）、置信度
    """
    # 校验文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV文件不存在：{file_path}")
    with open(file_path, 'rb') as f:
            # 读取指定大小的样本数据，若文件更小则读取全部
            raw_data = f.read(sample_size)
            # 若文件为空，返回默认编码utf-8
            if not raw_data:
                return "utf-8", 1.0
            
            # 分析编码
            result = cchardet.detect(raw_data)
            encoding = result['encoding']
            if encoding == 'GB2312':
                encoding = 'GB18030'
            confidence = result['confidence']
            
            return encoding, confidence

def readCsvFile(file_path, header=0,sample_size=10240):
    """
    读取CSV文件，自动判别编码格式
    :param file_path: CSV文件路径
    :param header: 表头行数（默认0，第一行）
    :param sample_size: 读取的样本字节数（默认10KB）
    :return: 包含数据的DataFrame
    """
    encoding, confidence = getCsvEncoding(file_path, sample_size)
    try:
        df = pd.read_csv(file_path, header=header, encoding=encoding)
    except Exception as e:
        # 按pd.read_csv出错，则逐行读取加入dataframe
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            lines = file.readlines()
        max_len = max(len(lines[i].strip().split(',')) for i in range(header,len(lines)))
        first_len = len(lines[header].strip().split(','))
        if first_len < max_len:
            columns = lines[header].strip().split(',') + [f'extra_{i}' for i in range(max_len - first_len)]
        else:
            columns = lines[header].strip().split(',')
        df = pd.DataFrame([line.strip().split(',') for line in lines[header+1:]], columns=columns)
    return df


def findJumpNum(route):
    # 使用正则表达式查找所有匹配项
    matches = re.findall('<==>', route)
    return len(matches)


def findKeyPoint(currentPath,objPath,site_dict):
    if pd.isnull(objPath):
        return "None","None",0
    sites = re.findall('>(.*?)\([AB正反/面ODM0-9]+-\d+-\d+',currentPath)
    if len(sites)==0:
        return "0","0",0
    if '-POS' in sites[-1]:
        sites[-1] = re.findall('(.*)-POS',sites[-1])[0]
    items = []
    # 倒序查询割接路径上的割接点,排除空字符串和NA值
    for site in sites:
        item = site_dict.get(site,site)
        if item == '':
            if site not in items:
                items.append(site)
        if item not in items:
            items.append(item)

    items = items[::-1]
    objPath = '=>' + objPath + '<='
    parts = re.findall('=>(.*?)<=',objPath)
    for i in range(len(parts)):
        if parts[i] != items[i] or i > len(items)-1:
            index = objPath.index('=>' + parts[i-1])
            path = objPath[index+2:-2]
            min_num = 300
            if '=>' in path:

                use_nums = re.findall('\((\d+)/\d+\)',path)
                if use_nums:
                    min_num = min(int(use_num) for use_num in use_nums)
            return parts[i-1],path,min_num
    return parts[-1],'-','300'

def fixSrcPoNPort(port_name):
    regex = r'-(\d+)-[A-Z0-9]+-(\d+)-GPON'
    match = re.search(regex,port_name)
    if match:
        slot = match.group(1)
        port = match.group(2)
        return slot,port
    else:
        return '-','-'