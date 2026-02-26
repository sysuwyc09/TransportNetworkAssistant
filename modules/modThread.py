# 存放模块线程类
from PySide6.QtCore import QThread, Signal
import pandas as pd
from modules.convertXY import convertXY
from modules.readKml import KmlLinePlace, KmlPointPlace, KmlPolygonPlace
import re

# 转换坐标线程类
class ConvertCoordThread(QThread):
    """
    转换坐标线程类
    """
    # 定义信号，用于线程结束时传递结果
    state_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, file_path, oldType, newType):
        super().__init__()
        self.file_path = file_path
        self.oldType = oldType
        self.newType = newType
    
    def run(self):
        """
        线程运行函数
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(self.file_path)
            if '经度' not in df.columns or '纬度' not in df.columns:
                self.error_signal.emit('Excel文件，首行中必须包含经度和纬度列')
                return;
            df['转换后经度'] = None
            df['转换后纬度'] = None
            df['转换状态'] = None
            for index, row in df.iterrows():
                try:
                    lon, lat = convertXY(row['经度'], row['纬度'], self.oldType, self.newType)
                    df.loc[index, '转换状态'] = '成功'
                except Exception as e:
                    self.state_signal.emit(f'第{index+1}行坐标转换失败：{str(e)}')
                    df.loc[index, '转换状态'] = '失败：' + str(e)
                    lon = None
                    lat = None
                df.loc[index, '转换后经度'] = lon
                df.loc[index, '转换后纬度'] = lat
                self.state_signal.emit(f'第{index+1}行坐标转换完成')
            
            # 保存到新文件
            out_file_path = self.file_path.replace('.xls', '_转换后.xls')
            df.to_excel(out_file_path, index=False)
            self.state_signal.emit(f'坐标转换完成，已保存到{out_file_path}')
        except Exception as e:
            self.error_signal.emit(f'坐标转换失败：{str(e)}')

# open读取kml文件线程类   
class readKmlThread(QThread):  # 步骤1.创建一个线程实例
    proSignal = Signal(tuple)
    stateSignal = Signal(str)
    def __init__(self, kmlFileName,pointFlag,lineFlag,polyFlag):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(readKmlThread, self).__init__()
        self.kmlFileName = kmlFileName
        self.pointFlag = pointFlag
        self.lineFlag = lineFlag
        self.polyFlag = polyFlag
    def run(self):
        # try:
        self.proSignal.emit((True,0))
        self.stateSignal.emit('正在读取kml文件...')
        with open(self.kmlFileName,encoding='UTF-8') as f:
            text = f.read()
        self.readKmlOut(text)
        # except Exception as e:
        #     self.stateSignal.emit(str(e))

    def readKmlOut(self,text):
        folders = text.split('<Folder>')
        linePlaces = {}
        pointPlaces = {}
        polygonPlace = {}
        lineRegex = re.compile('<coordinates>(.*)</coordinates>',re.DOTALL)
        for j in range(len(folders)): 
            lines = folders[j].split('<Placemark>')
            folderName = re.search('<name>(.*)</name>',lines[0]).group(1)
            linePlaces.setdefault(folderName,[])
            pointPlaces.setdefault(folderName,[])
            polygonPlace.setdefault(folderName,[])
            for i in range(1,len(lines)):
                """处理线资源"""
                if '<LineString>' in lines[i]:
                    names = re.search('<name>(.*)</name>',lines[i])
                    coordinates = lineRegex.search(lines[i])
                    if names and coordinates:
                        name = names.group(1)
                        coordinate = coordinates.group(1)
                        linePlaces[folderName].append(KmlLinePlace(name,coordinate))
                """处理点资源"""
                if '<Point>' in lines[i]:
                    names = re.search('<name>(.*)</name>',lines[i])
                    longitudes = re.search('<coordinates>(\d*\\.\d*)',lines[i])
                    latitudes = re.search('(\d*\\.\d*),0</coordinates>',lines[i])
                    if names and longitudes and latitudes:
                        name = names.group(1)
                        longitude = longitudes.group(1)
                        latitude = latitudes.group(1)
                        pointPlaces[folderName].append(KmlPointPlace(name,latitude,longitude))
                """处理面资源"""
                if '<Polygon>' in lines[i]:
                    names = re.search('<name>(.*)</name>',lines[i])
                    coordinates = lineRegex.search(lines[i])
                    if names and coordinates:
                        name = names.group(1)
                        coordinate = coordinates.group(1).strip()
                        coordinate = re.sub(',0',',0 ',coordinate)
                        polygonPlace[folderName].append(KmlPolygonPlace(name,coordinate))
                proNum = int(round(80*(j-1)/len(folders)+80/len(folders)*i/len(lines),0))
                self.proSignal.emit((True,proNum))
        self.proSignal.emit((True,80))
        self.stateSignal.emit('读取完成，制作表格中...')		
        #输出点资源DataFrame
        if self.pointFlag:
            pointDf = pd.DataFrame({"文件夹":[],"标记资源名称":[],"经度":[],"纬度":[]})
            for folder,places in pointPlaces.items():
                for i in range(len(places)):
                    pointDf.loc[len(pointDf)]=[folder,places[i].name,places[i].longitude,places[i].latitude]
        #输出线资源DataFrame
        if self.lineFlag:
            lineDf = pd.DataFrame({"文件夹":[],"路径资源名称":[],"坐标":[],"长度/km":[]})
            for folder,places in linePlaces.items():
                for i in range(len(places)):
                    lineDf.loc[len(lineDf)]=[folder,places[i].name,places[i].coordinate,places[i].length]
        #输出面资源DataFrame
        if self.polyFlag:
            polygonDf = pd.DataFrame({"文件夹":[],'多边形资源名称':[],'坐标':[],'面积/平方公里':[]})
            for folder,places in polygonPlace.items():
                for i in range(len(places)):
                    polygonDf.loc[len(polygonDf)]= [folder,places[i].name,places[i].coordinate,places[i].area]

        outFileName = self.kmlFileName.split('/')[-1].split('.')[-2]
        self.proSignal.emit((True,90))
        self.stateSignal.emit('制作完成，生成表格中...')
        with pd.ExcelWriter(f'结果/{outFileName}图层解析结果.xlsx',engine='xlsxwriter') as writer:
            if self.pointFlag:
                pointDf.to_excel(writer,sheet_name='标记资源',index=False)
            if self.lineFlag:
                lineDf.to_excel(writer,sheet_name='线资源',index=False)
            if self.polyFlag:
                polygonDf.to_excel(writer,sheet_name='多边形资源',index=False)
        self.proSignal.emit((True,100))
        self.stateSignal.emit(f'Kml文件已解析，详细请见结果文件夹《{outFileName}.xlsx》')		

# 使用geopandas读取kml文件
class GeoReadKmlThread(QThread):
    """
    使用geopandas读取kml文件线程类
    """
    # 定义信号，用于线程结束时传递结果
    proSignal = Signal(tuple)
    stateSignal = Signal(str)
    error_signal = Signal(str)
    def __init__(self,kmlFileName,pointFlag,lineFlag,polyFlag):
        super().__init__()
        self.kmlFileName = kmlFileName
        self.pointFlag = pointFlag
        self.lineFlag = lineFlag
        self.polyFlag = polyFlag
    def run(self):
        pass