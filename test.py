
import re
import sqlite3
from publicFunc import *

sql = '''
    SELECT z.*,c.跳数, c.光衰, o.所属机房, s.所属区县
    FROM 主光路 z
    LEFT JOIN 超长主光路清单 c ON c.PON口 = z.PON口
    JOIN OLT网元 o ON z.OLT名称 = o.网元名称
    JOIN 机房 j ON o.所属机房 = j.机房名称
    JOIN 站点 s ON s.站点名称 = j.所属站点
'''

df = queryDataBase(sql)
print(df.shape)
df.to_excel('主光路-分析-2026-05-09.xlsx')
