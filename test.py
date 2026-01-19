from publicFunc import *
import pandas as pd


sql = '''
    SELECT dev.设施名称, dev.机房名称, dev.经度, dev.纬度
    FROM (
        SELECT 设施名称,机房名称,经度,纬度 FROM 光交箱
        UNION ALL
        SELECT 设施名称,机房名称,经度,纬度 FROM 分纤箱 WHERE 容量 >= 72
        UNION ALL
        SELECT 设施名称,机房名称,经度,纬度 FROM ODF
        
    ) as dev
'''
all_dev = queryDataBase(sql)
sql = '''
    SELECT 
        f.设施名称,
        f.机房名称,
        f.经度,
        f.纬度
    FROM 分纤箱 f
    INNER JOIN 主光路 g
        ON g.OBD所属对象 = f.设施名称
    WHERE f.容量 < 72;
'''
oBox_df = queryDataBase(sql)
all_dev = pd.concat([all_dev,oBox_df],axis=0)
all_dev['机房名称'] = fixSite(all_dev['机房名称'],all_dev['设施名称'])
all_dev2 = all_dev.copy().drop(['设施名称'],axis=1).rename(columns={'机房名称':'OBD所属对象'})
all_dev = all_dev.drop(['机房名称'],axis=1).rename(columns={'设施名称':'OBD所属对象'})
all_dev = pd.concat([all_dev,all_dev2],axis=0).drop_duplicates()

df = pd.read_excel('ONU弱光PON口.xlsx')
df = df.merge(all_dev,on=['OBD所属对象'])
df.to_excel('PON口光数据/弱光ONU(含经纬度).xlsx',index=False)