
import re
import sqlite3
import pandas as pd
from publicFunc import *


def analyze_fiber_cable_segments():
    """
    分析光缆段与中继段的关联关系，输出包含以下列的结果表：
    - 光缆段
    - 包含中继段明细
    - 中继纤芯数量总数
    """
    try:
        # 读取中继段至光缆段表
        relay_to_fiber_df = readDataBase('中继段至光缆段')
        if relay_to_fiber_df.empty:
            print('中继段至光缆段表为空')
            return pd.DataFrame()
        
        # 读取中继段表
        relay_df = readDataBase('中继段')
        if relay_df.empty:
            print('中继段表为空')
            return pd.DataFrame()
        
        # 合并两个表，中继段至光缆段的"中继段"对应中继段表的"名称"
        merged_df = relay_to_fiber_df.merge(relay_df, left_on='中继段', right_on='名称', how='left')
        
        # 按光缆段分组，汇总中继段明细和中继纤芯数量
        result_df = merged_df.groupby('光缆段').agg(
            包含中继段明细=('中继段', lambda x: ','.join(x.dropna().unique())),
            中继纤芯数量总数=('中继纤芯数量', 'sum')
        ).reset_index()
        
        # 重命名列
        result_df = result_df[['光缆段', '包含中继段明细', '中继纤芯数量总数']]
        
        print('分析完成，共 {} 个光缆段'.format(len(result_df)))
        return result_df
    
    except Exception as e:
        print(f'分析失败: {str(e)}')
        return pd.DataFrame()


if __name__ == '__main__':
    result = analyze_fiber_cable_segments()
    if not result.empty:
        # print(result)
        # 可选：保存到文件
        result.to_excel('光缆段分析结果.xlsx', index=False)
        print('结果已保存到 光缆段分析结果.xlsx')
