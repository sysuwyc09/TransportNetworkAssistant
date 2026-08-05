'''
判定条件 
1.适用场景：室分站点核心判定要点：箱体仅承担室分成端功能，箱内仅敷设单条光缆，无光缆转接、分支外联作用。判定条件 
2.适用场景：集客类型，楼宇已部署 FAP核心判定要点：楼内公共区域已部署FAP，箱体属于面向客户侧的末端延伸分纤箱，箱内仅敷设单条光缆，不承担对外业务对接、光路中转节点职能。请各地市根据附件填报清单信息。再次强调，名称必须和资源系统一致，否则直接判定为分纤箱。
'''

from thread.publicFunc import *
import pandas as pd

import os

dir = r'文件范例/一键更新2026-07-21'
files = os.listdir(dir)
obox_files = [f for f in files if '分纤箱' in f]
line_files = [f for f in files if '光缆段' in f]
dfs = []
for obox_file in obox_files:
    df = readCsvFile(os.path.join(dir,obox_file))
    dfs.append(df)
line_dfs = []
for line_file in line_files:
    df = readCsvFile(os.path.join(dir,line_file))
    line_dfs.append(df)
line_df = pd.concat(line_dfs,ignore_index=True)
obox_df = pd.concat(dfs,ignore_index=True)

table = pd.pivot_table(line_df,index='A端设备',aggfunc={'名称':'count'})
table = table.reset_index().rename(columns={'A端设备':'设施名称','名称':'A段光缆段数'})
obox_df = pd.merge(obox_df,table,on='设施名称',how='left')
table = pd.pivot_table(line_df,index='Z端设备',aggfunc={'名称':'count'})
table = table.reset_index().rename(columns={'Z端设备':'设施名称','名称':'Z段光缆段数'})
obox_df = pd.merge(obox_df,table,on='设施名称',how='left')
obox_df['A段光缆段数'] = obox_df['A段光缆段数'].fillna(0)
obox_df['Z段光缆段数'] = obox_df['Z段光缆段数'].fillna(0)
obox_df['光缆段数'] = obox_df['A段光缆段数'] + obox_df['Z段光缆段数']

old_df = pd.read_excel(r'分析数据\湛江_筛选.xlsx',sheet_name='Sheet1')[['设施名称','集客/无线']]
old_df = pd.merge(old_df,obox_df,on='设施名称',how='left')

fap_df = readCsvFile(r'分析数据\FAP设备-1.CSV')
fap_df = fap_df[['FAPNAME']].rename(columns={'FAPNAME':'设施名称'})
fap_df['是否FAP'] = '是'

old_df = pd.merge(old_df,fap_df,on='设施名称',how='left')

old_df.to_excel(r'分析数据\分纤箱转终端盒分析2026-07-24.xlsx',index=False)
