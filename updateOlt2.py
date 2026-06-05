#!python
#更新OLT的工程态，ONU，流量，综资光路情况
#
import pandas as pd
import numpy as np
import sqlite3
import os
import re
from datetime import datetime

"""定义矢量函数，处理不完整分公司数据"""
@np.vectorize
def fixCompany(x,y):
    companyRex = re.compile('(赤坎|霞山|开发区|雷州|廉江|吴川|遂溪|徐闻)')
    if pd.isnull(x):
        try:
            x = companyRex.search(y).group()
        except: 
            if '坡头' in y:
                x = '霞山'
            elif '麻章' in y:
                x = '赤坎'
            else:
                x = '-'
    return x

#识别设备业务槽位数：
def srvBoardNum(devType):
    if 'MA5800-X17' in devType:
        return 17
    elif 'MA5680T' in devType:
        return 16
    elif 'MA5800-X7' in devType:
        return 7
    elif 'MA5683T' in devType:
        return 6
    elif 'C320' in devType:
        return 2        
    elif 'C300' in devType:
        return 14   
    elif 'C600' in devType:
        return 17
    else:
        return 999
#筛选PON口
def isPonPort(boardType):
    if boardType == 'GPON_XGPON' or boardType == 'GPON_XGSPON' or boardType == 'GPON' or boardType == 'EPON口' or boardType == 'GPON口' or boardType == 'XGPON':
        return '是'
    else:
        return '否'
#筛选XG-PON口
def isXgPonPort(boardType):
    if boardType == 'GPON_XGPON' or boardType == 'GPON_XGSPON' or boardType == 'XGPON':
        return '是'
    else:
        return '否'

def isXgPonPort2(boardType):
	if 'CG' in boardType:
		return '是'
	elif 'GFBT' in boardType or 'VSCP' in boardType:
		return '是'
	else:
		return '否'

#分析是否业务单板
def isSrvBoard(boardType):
    if '5800-X17' in boardType:
        board_ids = ['9', '10']
    elif '5800-X7' in boardType:
        board_ids = ['8', '9']
    elif '5680' in boardType:
        board_ids = ['9','10','19', '20']
    elif '600' in boardType:
        board_ids = ['10', '11']
    elif '320' in boardType:
        board_ids = ['3', '4']
    elif '300' in boardType:
        board_ids = ['10','11','19','20']
    elif '5683' in boardType:
        board_ids = ['6','7','8','9']
    else:
        board_ids = []
    match = re.search(' (\d+)槽',boardType)
    if match:
        board_id = match.group(1)
        if board_id in board_ids:
            return '否'
        else:
            return '是'
    return '是'
    


#转换为资管标准格式
@np.vectorize
def stardBoard(oltName,boardId):
    return oltName + ' ' + str(boardId) + '槽'
#重定义板卡状态
def fixState(state):
    if state == '正常':
        return '在位'
    elif state == '在线':
        return '在位'
    elif state == '离线':
        return '不在位'
    else:
        return state
#重定义板卡状态
@np.vectorize
def isNotUse(use,need):
    if use == 0 and need == 0:
        return '否'
    else:
        return '是'

@np.vectorize
def isNotUseOlt(ponNum,useNum):
    try:
        if ponNum == useNum:
            return '是'
        else:
            return '否'
    except Exception as e:
        str(e)


@np.vectorize
def oltType(name,type):
    if pd.isnull(type):
        return name.split('-')[-1]
    return type

def fixDevType(devType):
    if 'MA58' in devType:
        return 'MA58系列'
    elif 'MA56' in devType:
        return 'MA56系列'
    elif 'C600' in devType:
        return 'C600系列'
    elif 'C3' in devType:
        return 'C300系列'
    else:
        return '-'

@np.vectorize
def fixPonPath(ptype,eName,oName):
    if pd.isnull(eName) and pd.isnull(oName):
        if ptype == '尾纤直连':
            return '尾纤直连'
        else:
            return '录入缺失'
    else:
        if pd.isnull(eName):
            return oName + '(光路)'
        elif pd.isnull(oName):
            return eName + '(电路)'
        else:
            return '录入缺失'

def fixOltPort(portName):
    if pd.isnull(portName):
        return "OLT端口缺失"
    else:
        # portName.replace('-ETH','')
        # if "_" in portName:
        # 	portName = portName.replace("_","-")
        # if "." in portName:
        # 	portName = portName.replace(".","-")
        parts = portName.split("-")
        if len(parts) >=4:
            return "-".join(parts[-4:-1])
        else:
            return "OLT端口缺失"

#返回PON口统计
def ponCount(hwBoardFile,zteBoardFile):
    ponDf = pd.read_csv('全量PON口数据（修正）.csv',encoding='ANSI')
    # ponDf = pd.DataFrame()
    # for key,value in df1.items():
    # 	ponDf = ponDf.append(value)
    ponDf.rename(columns={'OLT名称':'OLT'},inplace=True)
    # ponDf['板卡'] = ponDf['端口名称'].apply(lambda x: '-'.join(x.split('-')[-3:-1]))
    # ponDf['板卡名称'] = ponDf['OLT'] + '-' + ponDf['板卡']
    zteDf = pd.read_excel(zteBoardFile)
    zteDf['槽位'] = zteDf['板卡槽位'].apply(lambda x: int(x.split('-')[2]))
    zteDf['板卡名称'] = stardBoard(zteDf['网元名称'],zteDf['槽位'])
    zteDf = zteDf[['板卡名称','板卡状态','板卡类型']]
    hwDf = pd.read_excel(hwBoardFile,header=3)
    hwDf['板卡名称'] = stardBoard(hwDf['所属网元'],hwDf['槽位号'])
    hwDf = hwDf[['板卡名称','单板状态','单板类型']]
    hwDf.rename(columns={'单板状态':'板卡状态','单板类型':'板卡类型'},inplace=True)
    hwDf = pd.concat([hwDf,zteDf])
    hwDf['板卡状态'] = hwDf['板卡状态'].apply(fixState)
    ponDf = ponDf.merge(hwDf,on='板卡名称',how='left')
    ponDf.to_csv('全量PON（匹配网管状态）.csv',encoding='ANSI',index=False)
    ponDf = ponDf[ponDf['板卡状态']=='在位']
    #查OLT实际占用业务槽位数
    boardDf = ponDf[['OLT','板卡名称','端口类型']].copy()
    boardDf = boardDf.drop_duplicates(subset=['板卡名称'])
    boardDf['是否业务板'] = boardDf['板卡名称'].apply(isSrvBoard)
    boardDf = boardDf[boardDf['是否业务板']=='是']
    boardTable = pd.pivot_table(boardDf,index=['OLT'],aggfunc={'板卡名称':'count'})
    boardTable = boardTable.reset_index()
    boardTable.rename(columns={'OLT':'本地名称','板卡名称':'业务槽占用数'},inplace=True)
    boardTable = boardTable[['本地名称','业务槽占用数']]

    #筛选PON口
    ponDf['是否PON口'] = ponDf['端口类型'].apply(isPonPort)
    ponDf = ponDf[ponDf['是否PON口']=='是']

    ponDf['是否千兆PON口'] = ponDf['端口类型'].apply(isXgPonPort)
    xgPonDf = ponDf[ponDf['是否千兆PON口']=='是'].copy()
    #数据透视表统计PON口数量
    ponTable = pd.pivot_table(ponDf,index=['OLT'],columns=['端口状态'],aggfunc={'端口名称':'count'},fill_value=0)
    ponTable.columns = ponTable.columns.droplevel()
    ponTable = ponTable.reset_index()
    ponTable['PON口总数'] = ponTable['占用'] + ponTable['预占'] + ponTable['空闲']
    ponTable.rename(columns={'OLT':'本地名称','空闲':'PON口空闲数'},inplace=True)
    ponTable = ponTable[['本地名称','PON口总数','PON口空闲数']]
    ponTable['闲置OLT'] = isNotUseOlt(ponTable['PON口总数'],ponTable['PON口空闲数'])
    #数据透视表统计千兆PON口数量
    xgPonTable = pd.pivot_table(xgPonDf,index=['OLT'],columns=['端口状态'],aggfunc={'端口名称':'count'},fill_value=0)
    xgPonTable.columns = xgPonTable.columns.droplevel()
    xgPonTable = xgPonTable.reset_index()
    xgPonTable['千兆PON口总数'] = xgPonTable['占用'] + xgPonTable['预占'] + xgPonTable['空闲']
    xgPonTable.rename(columns={'OLT':'本地名称','空闲':'千兆PON口空闲数'},inplace=True)
    xgPonTable = xgPonTable[['本地名称','千兆PON口总数','千兆PON口空闲数']]    

    #分析PON板空闲情况占用情况：

    notUseTable = pd.pivot_table(ponDf,index=['OLT','板卡名称'],columns=['端口状态'],aggfunc={'端口名称':'count'},fill_value=0)
    notUseTable.columns = notUseTable.columns.droplevel()
    notUseTable = notUseTable.reset_index()
    notUseTable = notUseTable.merge(hwDf,on='板卡名称')
    notUseTable['是否千兆'] = notUseTable['板卡类型'].apply(isXgPonPort2)
    notUseTable['是否在用'] = isNotUse(notUseTable['占用'],notUseTable['预占'])
    notUseTable['端口数量'] = notUseTable['占用'] + notUseTable['预占'] + notUseTable['空闲']
    notUseTable['在用端口数'] = notUseTable['占用'] + notUseTable['预占']
    notUseTable['设备系列'] = notUseTable['OLT'].apply(fixDevType)
    notUseTable.rename(columns={'OLT':'本地名称'},inplace=True)
    # notUseTable = notUseTable[notUseTable['是否在用']=='否']


    return ponTable,xgPonTable,boardTable,notUseTable




#主函数
if __name__ == '__main__':

    files = os.listdir()
    for file in files:
        if 'OLT设备_' in file and '$' not in file:
            oltFileName = file
        # if 'OLT上联口流量报表' in file:
        #   zteFlowFileName = file
        # if 'OLT上行端口流量报表' in file:
        #   hwFlowFileName = file
        if 'OLT上联链路_' in file and '$' not in file:
            oltLinkFileName = file
        if 'OLT下带用户数统计' in file and '$' not in file:
            onuNumFileName = file
        if 'OLT管理一张表' in file and '$' not in file:
            oldFileName = file
        if 'card_query' in file and '$' not in file:
            zteBoardFile = file
        if '单板报表' in file and '$' not in file:
            hwBoardFile = file
            
    #规范输出列顺序
    outCols = ['分公司','区域归属','网格','网管IP', '本地名称', '生命周期状态', '所属站点', '所属机房/位置点', '级别','产权单位','机房状态',\
        '设备型号', '是否千兆','站点ONU数量', 'ONU数量','闲置OLT','PON口总数','PON口空闲数','千兆PON口总数','千兆PON口空闲数','空闲业务槽数量',\
         '综资上联BNG','综资关联链路','城域网数据', '是否同路由', '同路由长度', '>300或者>800m', '是否整改',\
        '（跳纤整改）现有资源满足', '问题','汇聚机房比例提升策略','附近汇聚距离','目标搬迁机房']

    #读取新资源
    newDf = pd.read_excel(oltFileName)
    newDf = newDf[['所属位置点/机房','本地名称','设备型号','设备IP地址（省内系统：网管IP）','生命周期状态']]
    newDf.rename(columns={'所属位置点/机房':'所属机房/位置点','设备IP地址（省内系统：网管IP）':'网管IP'},inplace=True)


    newDf['设备型号'] = oltType(newDf['本地名称'],newDf['设备型号'])
    newDf['是否千兆'] = newDf['设备型号'].apply(lambda x: '是' if 'MA5800' in x or 'C600' in x else '否')

    newDf['业务槽数量'] = newDf['本地名称'].apply(srvBoardNum)

    #机房，匹配到具体分公司
    conn = sqlite3.connect('E:/工作文档/支撑系统/数据库/资源中心数据表.db')
    query = 'SELECT * FROM 机房表'
    houseDf = pd.read_sql(query, conn)
    conn.close()
    # houseDf = houseDf[['所属区域','机房名称','级别','产权单位','生命周期状态','业务区','站点']]
    houseDf = houseDf[['所属区县','机房名称','业务级别','产权单位','生命周期状态','所属站点']]
    houseDf.rename(columns={'机房名称':'所属机房/位置点','业务级别':'级别','生命周期状态':'机房状态'},inplace=True)
    houseDf = houseDf[['所属机房/位置点','所属站点','级别','产权单位','机房状态']]
    newDf = newDf.merge(houseDf,how='left',on='所属机房/位置点')
    # newDf['分公司'] = fixCompany(newDf['分公司'],newDf['本地名称'])
    #梳理ONU数量
    onuDf = pd.read_excel(onuNumFileName)
    onuDf = onuDf[['设备名称','下挂用户数']]
    onuDf.rename(columns={'设备名称':'本地名称','下挂用户数':'ONU数量'},inplace=True)
    newDf = newDf.merge(onuDf,how='left',on='本地名称')
    onuTable = pd.pivot_table(newDf,index=['所属站点'],aggfunc={'ONU数量':'sum'})
    onuTable = onuTable.reset_index()
    onuTable.rename(columns={'ONU数量':'站点ONU数量'},inplace=True)
    newDf = newDf.merge(onuTable,how='left',on='所属站点')

    #梳理PON口情况：
    ponTable,xgPonTable,boardTable,notUseTable = ponCount(hwBoardFile,zteBoardFile)
    newDf = newDf.merge(ponTable,how='left',on='本地名称')
    newDf = newDf.merge(xgPonTable,how='left',on='本地名称')
    newDf = newDf.merge(boardTable,how='left',on='本地名称')
    newDf['千兆PON口总数'] = newDf['千兆PON口总数'].fillna(0)
    newDf['千兆PON口空闲数'] = newDf['千兆PON口空闲数'].fillna(0)
    newDf['业务槽占用数'] = newDf['业务槽占用数'].fillna(0)
    newDf['空闲业务槽数量'] = newDf['业务槽数量'] - newDf['业务槽占用数']

    tempDf = newDf[['本地名称','设备型号','所属站点','所属机房/位置点','生命周期状态']]
    notUseTable = notUseTable.merge(tempDf,how='left',on='本地名称')
    #梳理综资链路情况
    linkDf = pd.read_excel(oltLinkFileName)
    # linkDf = linkDf[linkDf['A端设备类型']=='BNG']
    # linkDf = linkDf[linkDf['电路带宽']=='10G']
    linkDf['电路名称'] = fixPonPath(linkDf['连接方式'],linkDf['传输电路名称'],linkDf['光纤光路名称']) 
    linkDf["OLTPort"] = linkDf["OLT端口"].apply(fixOltPort)
    linkDf['电路名称'] = linkDf['电路名称'] + '{' + linkDf['A端设备名称'] + ':' + linkDf['A端端口名称'] + '<=>' + linkDf['OLTPort'] + '}'

    linkDf = linkDf[['OLT设备','电路名称','电路带宽']]
    linkDf.fillna('None',inplace=True)
    linkTable = pd.pivot_table(linkDf,index=['OLT设备'],aggfunc={'电路带宽':'count'})
    linkTable = linkTable.reset_index()
    linkTable.rename(columns={'OLT设备':'本地名称','电路带宽':'综资上联BNG'},inplace=True)
    newDf = newDf.merge(linkTable,how='left',on='本地名称')
    linkDf = linkDf.astype('str')
    linkGroup = linkDf.groupby('OLT设备').agg('//'.join)
    linkGroup = linkGroup.reset_index()
    linkGroup.rename(columns={'OLT设备':'本地名称','电路名称':'综资关联链路'},inplace=True)
    newDf = newDf.merge(linkGroup,how='left',on='本地名称')

    # #梳理流量系统链路情况
    # hwFlowDf = pd.read_excel(hwFlowFileName)
    # hwFlowDf = hwFlowDf[hwFlowDf['端口速率(Mb/s)']==10000]
    # hwFlowDf = hwFlowDf.astype('str')
    # hwFlowDf = hwFlowDf[hwFlowDf['下行峰值速率(Mb/s)']!='0']
    # hwFlowDf = hwFlowDf[hwFlowDf['下行峰值速率(Mb/s)']!='--']
    # hwFlowDf = hwFlowDf[['网元名称','端口名称']]

    # zteFlowDf = pd.read_excel(zteFlowFileName)
    # zteFlowDf = zteFlowDf[zteFlowDf['端口速率峰值(Mb/s)']==10000]
    # zteFlowDf = zteFlowDf[zteFlowDf['接收流速峰值(Mb/s)']!=0]
    # zteFlowDf = zteFlowDf[['OLT名称','线路标识']]
    # zteFlowDf.rename(columns={'OLT名称':'网元名称','线路标识':'端口名称'},inplace=True)
    # flowDf = pd.concat([hwFlowDf,zteFlowDf])
    # flowTable = pd.pivot_table(flowDf,index=['网元名称'],aggfunc={'端口名称':'count'})
    # flowTable = flowTable.reset_index()
    # flowTable.rename(columns={'网元名称':'本地名称','端口名称':'OLT流量（10G）'},inplace=True)
    # newDf = newDf.merge(flowTable,how='left',on='本地名称')

    #筛选在网态OLT
    newDf['筛选'] = newDf['生命周期状态'].apply(lambda x: '否' if '退网' in x else '是')
    newDf = newDf[newDf['筛选']=='是']
    # newDf['筛选'] = newDf['设备型号'].apply(lambda x: '否' if 'AN' in x else '是')
    # newDf = newDf[newDf['筛选']=='是']
    newDf.drop(['筛选'],axis=1,inplace=True)

    #提取人工填写字段，网管IP来匹配
    oldDf = pd.read_excel(oldFileName)
    oldDf = oldDf[['分公司','网管IP','区域归属','网格','城域网数据', '是否同路由', '同路由长度', '>300或者>800m', '是否整改',\
        '（跳纤整改）现有资源满足', '问题','汇聚机房比例提升策略','附近汇聚距离','目标搬迁机房']]
    newDf = newDf.merge(oldDf,how='left',on='网管IP')
    newDf = newDf[outCols]
    newDf.sort_values(by=['站点ONU数量','所属站点','ONU数量'],ascending=[False,True,False],inplace=True)
    
    dt=datetime.now().strftime('%Y-%m-%d')
    newDf.to_excel(f'【OLT管理一张表】{dt}.xlsx',index=False)
    notUseTable.to_excel(f'pon板分析{dt}.xlsx',index=False)
    