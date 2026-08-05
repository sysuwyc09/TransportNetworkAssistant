'''
大业务管道、杆路图层&分区县图层输出
'''
from PySide6.QtCore import QThread, Signal
import sqlite3
import pandas as pd
import numpy as np
import datetime
from .publicFunc import *
import time
import re


class LargePoleThread(QThread):
    state_signal = Signal(str)

    def __init__(self,file_dir):
        super().__init__()
        self.file_dir = file_dir
    
    def run(self):
        large_files,pole_files,pole_line_files, pipe_files, pipe_line_files= self.checkFiles()
        check_list = [
        (large_files, "未找到重载业务文件"),
        (pole_files, "未找到电杆文件"),
        (pole_line_files, "未找到杆路段文件"),
        (pipe_files, "未找到管道段文件"),
        (pipe_line_files, "未找到人手井文件"),
        ]
        for file_list, msg in check_list:
            if not file_list:
                self.state_signal.emit(msg)
                return
        self.state_signal.emit('文件检查通过，加载文件数据中，请稍后...')
        large_df = self.loadFile(large_files,'xlsx')
        pole_df = self.loadFile(pole_files,'CSV')
        pole_line_df = self.loadFile(pole_line_files,'CSV')
        pipe_df = self.loadFile(pipe_files,'CSV')
        pipe_line_df = self.loadFile(pipe_line_files,'CSV')
        pole_line_df,pipe_line_df = self.mergeCoord(pole_df,pole_line_df,pipe_df,pipe_line_df)
        large_df = large_df[['资源类型','资源名称','家宽用户数','集客用户数','AAA集客业务数','逻辑基站数']].rename(columns={'资源名称':'名称'})
        large_df = large_df.astypes({'家宽用户数':'int'})
        '''筛选超1000户的支撑段'''
        large_df = large_df[large_df['家宽用户数']>=1000]
        large_pole_df = large_df[large_df['资源类型']=='杆路段'].copy().drop(columns=['资源类型'])
        large_pipe_df = large_df[large_df['资源类型']=='管道段'].copy().drop(columns=['资源类型'])
        large_pole_df = pd.merge(large_pole_df,pole_line_df,on=['名称'])
        large_pipe_df = pd.merge(large_pipe_df,pipe_line_df,on=['名称'])
        dt = datetime.datetime.now().strftime('%Y-%m-%d')
        self.writeKml(large_pole_df,f'超千户杆路-{dt}')
        self.writeKml(large_pipe_df,f'超千户管道-{dt}')
        '''分区县输出所有管道、杆路的kml文件'''
        df_grped = pole_line_df.groupby('所属区县')
        for df_grp in df_grped:
            self.writeKml(df_grp[1],f'{df_grp[0]}杆路-{dt}')
        df_grped = pipe_line_df.groupby('所属区县')
        for df_grp in df_grped:
            self.writeKml(df_grp[1],f'{df_grp[0]}管道-{dt}')
        self.state_signal.emit('所有文件生成成功！')
        
    
    def writeKml(self,df,file_name):
        '''写入kml文件'''
        folders = self.lineTwoPointKml(df)
        outStr = self.writeDoc(folders,doc_name=file_name)
        with open(f'图层/{file_name}.kml','w',encoding='UTF-8') as f:
            f.write(outStr)
        self.state_signal.emit(f"{file_name}生成成功！")


    
    def mergeCoord(self,pole_df,pole_line_df,pipe_df,pipe_line_df):
        '''合并电杆和杆路段坐标,管道段和人手井坐标'''
        pole_df = pole_df[['电杆名称','经度','纬度']].rename(columns={'电杆名称':'A端名称','经度':'A端经度','纬度':'A端纬度'})
        pole_line_df = pole_line_df[['杆路段名称','所属区县','所属杆路','起始设施名称','终止设施名称','红线范围','挂缆条数','产权单位','资源状态']].rename(columns={'杆路段名称':'名称','起始设施名称':'A端名称','终止设施名称':'Z端名称'})
        pole_line_df = pd.merge(pole_line_df,pole_df,on=['A端名称'])
        pole_df = pole_df.rename(columns={'A端名称':'Z端名称','A端经度':'Z端经度','A端纬度':'Z端纬度'})
        pole_line_df = pd.merge(pole_line_df,pole_df,on=['Z端名称'])
        '''处理管道段坐标'''
        pipe_df = pipe_df[['人手井名称','经度','纬度']].rename(columns={'人手井名称':'A端名称','经度':'A端经度','纬度':'A端纬度'})
        pipe_line_df = pipe_line_df[['管道段名称','所属区县','所属管道','起始设施名称','终止设施名称','红线范围','挂缆条数','产权单位','资源状态','管孔数']].rename(columns={'管道段名称':'名称','起始设施名称':'A端名称','终止设施名称':'Z端名称'})
        pipe_line_df = pd.merge(pipe_line_df,pipe_df,on=['A端名称'])
        pipe_df = pipe_df.rename(columns={'A端名称':'Z端名称','A端经度':'Z端经度','A端纬度':'Z端纬度'})
        pipe_line_df = pd.merge(pipe_line_df,pipe_df,on=['Z端名称'])
        '''清洗杆路长度超过500米，管道长度超过1000米的行'''
        pole_line_df = pole_line_df.astype({'A端经度':float,'A端纬度':float,'Z端经度':float,'Z端纬度':float})
        pipe_line_df = pipe_line_df.astype({'A端经度':float,'A端纬度':float,'Z端经度':float,'Z端纬度':float})
        pole_line_df['长度'] = CalcDistance(pole_line_df['A端纬度'],pole_line_df['A端经度'],pole_line_df['Z端纬度'],pole_line_df['Z端经度'])
        pipe_line_df['长度'] = CalcDistance(pipe_line_df['A端纬度'],pipe_line_df['A端经度'],pipe_line_df['Z端纬度'],pipe_line_df['Z端经度'])
        pole_line_df = pole_line_df[pole_line_df['长度']<=500]
        pipe_line_df = pipe_line_df[pipe_line_df['长度']<=1000]
        return pole_line_df,pipe_line_df
    

    def loadFile(self,file_list,file_type):
        '''加载文件数据'''
        dfs = []
        for file in file_list:
            if file_type == 'CSV':
                dfs.append(readCsvFile(file))
            else:
                dfs.append(pd.read_excel(file))
            self.state_signal.emit('已加载文件:' + file_type)
        df = pd.concat(dfs,ignore_index=True)
        return df

    def checkFiles(self):
        '''检查文件是否存在'''
        pole_files = []
        pole_line_files = []
        pipe_files = []
        pipe_line_files = []
        large_files = []
        files = os.listdir(self.file_dir)
        for file in files:
            if '电杆' in file and 'CSV' not in file:
                pole_files.append(self.file_dir + '/' + file)
            elif '杆路段' in file and 'CSV' not in file:
                pole_line_files.append(self.file_dir + '/' + file)
            elif '管道段' in file and 'CSV' not in file:
                pipe_files.append(self.file_dir + '/' + file)
            elif '人手井' in file and 'CSV' not in file:
                pipe_line_files.append(self.file_dir + '/' + file)
            elif '重载业务' in file and 'xlsx' not in file:
                large_files.append(self.file_dir + '/' + file)
        return large_files,pole_files,pole_line_files, pipe_files, pipe_line_files
    

    def pointKml(self,dataDf):
        '''写入点kml文件'''
        fstGrped = dataDf.groupby('所属区县')
        folders = []
        colorIndex = 0
        for fstGrp in fstGrped:
            places = []
            tempDf = fstGrp[1].copy()
            tempDf['描述'] = ''
            for col in tempDf.columns:
                if col != '描述':
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('<',''))
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('>',''))
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('&',''))
                    tempDf['描述'] = tempDf['描述'] + col + ": " + tempDf[col] + '\n'
            names = list(tempDf['名称'])
            longitudes = list(tempDf['经度'])
            latitudes = list(tempDf['纬度'])
            descriptions = list(tempDf['描述'])
            for i in range(len(names)):
                places.append(self.writePoint(names[i],longitudes[i],latitudes[i],descriptions[i],self.colors[colorIndex]))
            folders.append(self.writeFolder(fstGrp[0],places))
            colorIndex = colorIndex + 1
            if colorIndex == len(self.colors):
                colorIndex = 0
        return folders

    def lineTwoPointKml(self,dataDf):
        '''写入线kml文件'''
        fstGrped = dataDf.groupby('所属区县')
        folders = []
        colorIndex = 0
        for fstGrp in fstGrped:
            places = []
            tempDf = fstGrp[1].copy()
            tempDf['描述'] = ''
            for col in tempDf.columns:
                if col != '描述':
                    '''剔除会引起kml文件异常字符<、>、&'''
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('<',''))
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('>',''))
                    tempDf[col] = tempDf[col].apply(lambda x: str(x).replace('&',''))
                    tempDf['描述'] = tempDf['描述'] + col + ": " + tempDf[col] + '\n'
            tempDf = tempDf.astype('str')
            tempDf['坐标'] = tempDf['A端经度'] + ',' + tempDf['A端纬度'] + ',0 ' + tempDf['Z端经度'] + \
                ',' + tempDf['Z端纬度'] + ',0 '
            names = list(tempDf['名称'])
            coords = list(tempDf['坐标'])
            descriptions = list(tempDf['描述'])			
            for i in range(len(names)):
                places.append(self.writeLine(names[i],coords[i],descriptions[i],self.colors[colorIndex]))
            folders.append(self.writeFolder(fstGrp[0],places))
            colorIndex = colorIndex + 1
            if colorIndex == len(self.colors):
                colorIndex = 0
        return folders

    def lineCoordKml(self,dataDf):
        fstGrped = dataDf.groupby('所属区县')
        folders = []
        colorIndex = 0
        for fstGrp in fstGrped:
            places = []
            tempDf = fstGrp[1].copy()
            tempDf['描述'] = ''
            for col in tempDf.columns:
                if col != '描述' and '坐标' not in col and '经度' not in col and '纬度' not in col:
                    tempDf['描述'] = tempDf['描述'] + col + ": " + tempDf[col] + '\n'
            tempDf = tempDf.astype('str')
            names = list(tempDf['名称'])
            coords = list(tempDf['坐标'])
            descriptions = list(tempDf['描述'])			
            for i in range(len(names)):
                places.append(self.writeLine(names[i],coords[i],descriptions[i],self.colors[colorIndex]))
            folders.append(self.writeFolder(fstGrp[0],places))
            colorIndex = colorIndex + 1
            if colorIndex == len(self.colors):
                colorIndex = 0	
        return folders


    def header(self,doc_name='目录'):
        str = '<?xml version="1.0" encoding="UTF-8"?>'
        str = str + '\n' + '<kml xmlns=\"http://www.opengis.net/kml/2.2\" \n'
        str = str + '\t' + 'xmlns:atom=\"http://www.w3.org/2005/Atom\"  \n'
        str = str + '\t' + 'xmlns:gx="http://www.google.com/kml/ext/2.2"  \n'
        str = str + '\t>\n'
        str = str + '<Document>\n'
        str = str + '\t<name>' + doc_name + '</name>\n'
        return str

    def writeDoc(self,folders,doc_name='目录'):
        doc = self.header(doc_name)
        for folder in folders:
            doc = doc + folder
        doc = doc + '</Document>\n</kml>\n'
        return doc

    def writeFolder(self,name,places):
        folderStr = '\t<Folder>\n'
        folderStr = folderStr + '\t'*2 + '<name>' + name + '</name>\n'
        for place in places:
            folderStr = folderStr + place
        folderStr =  folderStr + '\t</Folder>\n'
        return folderStr

    def writeLine(self,name,coordinate,description,color):
        placeMark = '\t'*2 + '<Placemark>\n'
        placeMark = placeMark + '\t'*3 + '<name>' + name + '</name>\n'
        placeMark = placeMark + '\t'*3 + '<description>' + description + '</description>\n'
        placeMark = placeMark + '\t'*3 + f'<Style><LineStyle><color>ff{color}</color><width>3</width></LineStyle></Style>\n'
        placeMark = placeMark + '\t'*3 + '<LineString>\n'
        placeMark = placeMark + '\t'*4 + '<coordinates>' + coordinate + '</coordinates>\n'
        placeMark = placeMark + '\t'*3 + '</LineString>\n'
        placeMark = placeMark + '\t'*2 + '</Placemark>\n'
        return placeMark

    def writePoint(self,name,longitude,latitude,description,color):
        placeMark = '\t'*2 + '<Placemark>\n'
        placeMark = placeMark + '\t'*3 + '<name>' + name + '</name>\n'
        placeMark = placeMark + '\t'*3 + '<description>' + description + '</description>\n'
        placeMark = placeMark + '\t'*3 + '<Style>\n'
        placeMark = placeMark + '\t'*3 + '<IconStyle>\n'
        placeMark = placeMark + '\t'*4 + '<Icon>\n'
        placeMark = placeMark + '\t'*5 + f'<href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>\n'
        placeMark = placeMark + '\t'*4 + '</Icon>\n'
        placeMark = placeMark + '\t'*4 + f'<color>ff{color}</color>\n'
        placeMark = placeMark + '\t'*4 + '<scale>1.0</scale>\n'
        placeMark = placeMark + '\t'*3 + '</IconStyle>\n'
        placeMark = placeMark + '\t'*3 + '</Style>\n'
        placeMark = placeMark + '\t'*3 + '<Point>\n'
        placeMark = placeMark + '\t'*4 + '<coordinates>' + longitude + ',' + latitude + ',0</coordinates>\n'
        placeMark = placeMark + '\t'*3 + '</Point>\n'
        placeMark = placeMark + '\t'*2 + '</Placemark>\n'
        return placeMark