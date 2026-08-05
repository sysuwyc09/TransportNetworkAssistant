from thread.publicFunc import *
import pandas as pd


# 读取汇聚机房清单+经纬度,OLT+经纬度
sql = '''
SELECT J.*,O.经度,O.纬度
FROM 机房 J
JOIN ODF O ON J.机房名称 = O.机房名称
WHERE J.机房类型 = '传输机房' AND J.业务级别 != '本地接入' AND J.业务级别 != '用户' AND (J.生命周期状态 = '现网在用' OR J.生命周期状态 = '在建' OR J.生命周期状态 = '基础交维')
'''
house_df = queryDataBase(sql)

house_df = house_df[['机房名称','经度','纬度','业务级别']].rename(columns={'机房名称':'标记名称','业务级别':'备注'})
# 读取OLT网元+经纬度
olt_sql = '''
SELECT d.*,O.经度,O.纬度
FROM OLT网元 d
JOIN ODF O ON d.所属机房 = O.机房名称
'''
olt_df = queryDataBase(olt_sql)
olt_df = olt_df[['所属机房','经度','纬度','设备型号']].rename(columns={'所属机房':'标记名称','设备型号':'备注'})

        
house_df = pd.concat([house_df, olt_df], axis=0)
house_df = house_df[house_df['经度'].notnull()]
house_df = house_df.drop_duplicates(subset=['标记名称'], keep='first')
point_df = house_df.copy().rename(columns={'标记名称':'点名称','备注':'目录'})

# 提取超长主光路清单超10公里的光路
# long_sql = '''
# SELECT *
# FROM 主光路 
# WHERE 光路长度 >= 10000
# '''
# long_df = queryDataBase(long_sql)
long_df = pd.read_excel(r'E:\工作文档\OLT优化\整体布局分析2026-07-08\超长主光路分析2026-07-10.xlsx', sheet_name='全量主光路')
long_df = long_df[long_df['超长主光路'] == '是']
all_df= readDevsWithCoord().rename(columns={'设施名称':'OBD所属对象'})
long_df = long_df[long_df['OBD所属对象'].notnull()]
long_df = pd.merge(long_df, all_df, on='OBD所属对象', how='left')
long_df = long_df[long_df['经度'].notnull()]
temp_df = long_df[['PON口名称','经度','纬度']].copy().rename(columns={'PON口名称':'点名称'})
temp_df['目录'] = '超长主光路'
point_df = pd.concat([point_df, temp_df])

long_df = long_df[['OBD所属对象','经度','纬度','PON下挂ONU数量']].rename(columns={'OBD所属对象':'热力点','PON下挂ONU数量':'热力数据'})
long_df['热力数据'] = long_df['热力数据'] + 1

with pd.ExcelWriter('超长主光路热力图数据.xlsx') as writer:
    long_df.to_excel(writer, sheet_name='热力数据', index=False)
    house_df.to_excel(writer, sheet_name='标记数据', index=False)
point_df.to_excel('超长主光路点资源.xlsx', index=False)