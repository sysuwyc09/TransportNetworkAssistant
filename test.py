import pandas as pd
import sqlite3
import re
# conn = sqlite3.connect('data/transportNetwork.db')
# df = pd.read_sql("SELECT * FROM OLT表格该", conn)
# conn.close()

text = '上外田村村口光交箱(288芯)<={上外田村村口光交箱(288芯)-雷州外田村村口288芯/GJ}(11/12)=>雷州外田村村口288芯/GJ<={湛江市雷州豪郎传输机房AB列06B架-雷州外田村村口288芯/GJ/A}(5/12)=>湛江雷州市纪家豪郎一楼机房传输1<={湛江市雷州豪郎传输机房AA列08A-雷州豪郎综合机柜01/A}(131/144)=>湛江雷州豪郎一楼机房无线1'
lines = re.findall(r'{(.*?)}\((\d+)\/(\d+)\)', text)
for line in lines:
    print(line)
# 转换为DataFrame
df = pd.DataFrame(lines, columns=['设备名称', '占用', '总数'])
df['占用'] = df['占用'].astype(int)
df['总数'] = df['总数'].astype(int)
df['占用率'] = df['占用'] / df['总数']
print(df)