import pandas as pd
from publicFunc import *
# ----------------------
# 1. 按机房 + 设备型号 统计每型号的设备台数
# ----------------------
df = readDataBase('OLT网元数据集')
df_model_count = df.groupby(['所属机房', '设备型号']).size().reset_index(name='设备台数')

# 把每个机房下的【型号: 台数】拼成字符串
model_str = df_model_count.groupby('所属机房').apply(
    lambda x: '、'.join([f"{row['设备型号']}({row['设备台数']}台)" for _, row in x.iterrows()])
).reset_index(name='设备型号统计')

# ----------------------
# 2. 按机房汇总所有端口总数
# ----------------------
df_port = df.groupby('所属机房').agg(
    PON口总数汇总=('PON口总数', 'sum'),
    PON口空闲数汇总=('PON口空闲数', 'sum'),
    XGPON口总数汇总=('XGPON口总数', 'sum'),
    XGPON口空闲数汇总=('XGPON口空闲数', 'sum')
).reset_index()

# ----------------------
# 3. 合并统计结果
# ----------------------
result_df = pd.merge(model_str, df_port, on='所属机房')

# ----------------------
# 4. 拼接成【详细信息】列
# ----------------------
result_df['详细信息'] = (
    '设备情况:' + result_df['设备型号统计'] +
    ' PON口数:' + result_df['PON口总数汇总'].astype(int).astype(str) +
    ' PON口空闲数:' + result_df['PON口空闲数汇总'].astype(int).astype(str) +
    ' XGPON口数:' + result_df['XGPON口总数汇总'].astype(int).astype(str) +
    ' XGPON口空闲数:' + result_df['XGPON口空闲数汇总'].astype(int).astype(str)
)
# ----------------------
# 5. 最终只保留 2 列
# ----------------------
final_result = result_df[['所属机房', '详细信息']]
print(final_result.head())