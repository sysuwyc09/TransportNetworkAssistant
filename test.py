import pandas as pd
from publicFunc import *

def fixLongPonPort(pon_port):
    parts = pon_port.split('-')
    olt_name = '-'.join(parts[:-5])
    return olt_name + '-' + parts[-5] + '/' + parts[-4] + '/' + parts[-2]

def fixPathPoint(pon_path):
    sites = re.findall('>(.*?)\([AB正反/面ODM0-9]+-\d+-\d+',pon_path)
    items = []
    # 倒序查询割接路径上的割接点,排除空字符串和NA值
    for site in sites:
        if site not in items:
            items.append(site)
    items = items[::-1]
    df = pd.DataFrame({'光交设施':items})
    df['光路文本路由'] = pon_path
    return df

week_port_table = pd.read_excel('结果/7天内4天弱光清单匹配光模块信息202604221543.xlsx',sheet_name='弱光PON口替换光模块分析')

# 筛选可光模块替代的端口清单
opt_port_df = week_port_table[week_port_table['替换光模块类型']!='--']

# 分析可调优清单
not_opt_port_df = week_port_table[week_port_table['替换光模块类型']=='--']
long_pon_port = readDataBase('超长主光路清单')
long_pon_port['PON'] = long_pon_port['PON口'].apply(fixLongPonPort)

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
all_dev_df = readDevsWithCoord()
all_dev_df.rename(columns={'设施名称':'OBD所属对象'},inplace=True)
adjust_port_df = adjust_port_df.merge(all_dev_df,on='OBD所属对象',how='left')

# 分析弱光聚合情况
dfs = adjust_port_df['光路文本路由'].apply(fixPathPoint)
pon_path_df = pd.concat(dfs.tolist(),ignore_index=True)
dev_df = pd.pivot_table(pon_path_df,index='光交设施',aggfunc={'光路文本路由':'count'},fill_value=0)
dev_df = dev_df.reset_index()
dev_df.columns = ['光交设施','光路数']
pon_path_df = pon_path_df.merge(adjust_port_df[['光路文本路由','PON口']],on='光路文本路由',how='left')
temp_df = pon_path_df[['光交设施','PON口']]
temp_grp = temp_df.groupby('光交设施').agg('、'.join)
temp_grp = temp_grp.reset_index().rename(columns={'PON口':'弱光PON口清单'})
dev_df = dev_df.merge(temp_grp,on='光交设施',how='left')
dev_df.sort_values(by='光路数',ascending=False,inplace=True)

with pd.ExcelWriter('结果/7天内4天弱光清单匹配光模块信息202604221543.xlsx',engine='openpyxl') as writer:
    opt_port_df.to_excel(writer,sheet_name='可光模块替代的端口清单',index=False)
    not_opt_port_df.to_excel(writer,sheet_name='不可光模块替代的端口清单',index=False)
    long_pon_port.to_excel(writer,sheet_name='超长主光路清单',index=False)
    long_pon_up_link.to_excel(writer,sheet_name='超长主光路调优方案',index=False)
    temp_df.to_excel(writer,sheet_name='超长主光路调优方案-弱光PON口清单',index=False)
    dev_df.to_excel(writer,sheet_name='弱光聚合情况',index=False)
