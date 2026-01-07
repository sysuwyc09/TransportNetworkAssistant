from publicFunc import *
import pandas as pd

box_df = readDataBase('光交箱')[['设施名称','机房名称']]
oBox_df = readDataBase('分纤箱')[['设施名称','机房名称']]
odf_df = readDataBase('ODF')[['设施名称','机房名称']]
all_site_df = pd.concat([box_df,oBox_df,odf_df],axis=0)

temp_df = all_site_df.head(10)
print(temp_df[temp_df['机房名称'].notnull()])