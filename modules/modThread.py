# 存放模块线程类
from PySide6.QtCore import QThread, Signal
import pandas as pd
import numpy as np
from modules.convertXY import convertXY
from modules.readKml import KmlLinePlace, KmlPointPlace, KmlPolygonPlace
from modules.modPublicFunc import *
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


class WriteKmlThread(QThread):
    stateSignal = Signal(str)
    def __init__(self, outFileName,dataDf,kmlFlag):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(WriteKmlThread, self).__init__()
        self.outFileName = outFileName
        self.dataDf = dataDf
        self.headStr = self.header()
        self.kmlFlag = kmlFlag
        self.colors = ['0000ff','ff0000','00ff00','ffff00','ff00ff','00ffff','4080ff']
    def run(self):
        try:
            if self.kmlFlag == 0:
                folders = self.pointKml()
            elif self.kmlFlag == 1:
                folders = self.lineResourceKml()
            elif self.kmlFlag == 2:
                folders = self.lineTwoPointKml()
            elif self.kmlFlag == 3:
                folders = self.lineCoordKml()
            elif self.kmlFlag == 4:
                folders = self.polygonCoordKml()

            outStr = self.writeDoc(folders)
            with open(f'结果/{self.outFileName}.kml','w',encoding='UTF-8') as f:
                f.write(outStr)
            self.stateSignal.emit("生成图层完成！")
        except Exception as e:
            self.stateSignal.emit(str(e))

    def pointKml(self):
        fstGrped = self.dataDf.groupby('目录')
        folders = []
        colorIndex = 0
        for fstGrp in fstGrped:
            places = []
            tempDf = fstGrp[1].copy()
            tempDf['描述'] = ''
            for col in tempDf.columns:
                if col != '描述':
                    tempDf['描述'] = tempDf['描述'] + col + ": " + tempDf[col] + '\n'
            names = list(tempDf['名称'])
            longitudes = list(tempDf['经度'])
            latitudes = list(tempDf['纬度'])
            descriptions = list(tempDf['描述'])
            for i in range(len(names)):
                places.append(self.writePoint(names[i],longitudes[i],latitudes[i],names[i],self.colors[colorIndex]))
            folders.append(self.writeFolder(fstGrp[0],places))
            colorIndex = colorIndex + 1
            if colorIndex == len(self.colors):
                colorIndex = 0
        return folders

    def lineResourceKml(self):
        fstGrped = self.dataDf.groupby('目录')
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
            tempDf['坐标'] = tempDf['坐标'].apply(fixResourseCoord)
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

    def lineTwoPointKml(self):
        fstGrped = self.dataDf.groupby('目录')
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

    def lineCoordKml(self):
        fstGrped = self.dataDf.groupby('目录')
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

    def polygonCoordKml(self):
        fstGrped = self.dataDf.groupby('目录')
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
                places.append(self.writePolygon(names[i],coords[i],descriptions[i],self.colors[colorIndex]))
            folders.append(self.writeFolder(fstGrp[0],places))
            colorIndex = colorIndex + 1
            if colorIndex == len(self.colors):
                colorIndex = 0						
        return folders

    def header(self):
        str = '<?xml version="1.0" encoding="UTF-8"?>'
        str = str + '\n' + '<kml xmlns=\"http://www.opengis.net/kml/2.2\" \n'
        str = str + '\t' + 'xmlns:atom=\"http://www.w3.org/2005/Atom\"  \n'
        str = str + '\t' + 'xmlns:gx="http://www.google.com/kml/ext/2.2"  \n'
        str = str + '\t>\n'
        str = str + '<Document>\n'
        str = str + '\t<name>' + self.outFileName + '</name>\n'
        return str

    def writeDoc(self,folders):
        doc = self.header()
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

    def writePolygon(self,name,coord,description,color):
        placeMark = '\t'*2 + '<Placemark>\n'
        placeMark = placeMark + '\t'*3 + '<name>' + name + '</name>\n'
        placeMark = placeMark + '\t'*3 + '<description>' + description + '</description>\n'
        placeMark = placeMark + '\t'*3 + '<Style>\n'
        placeMark = placeMark + '\t'*4 + f"<LineStyle><color>ff{color}</color><width>2</width></LineStyle>\n"
        placeMark = placeMark + '\t'*4 + f"<PolyStyle><color>4c{color}</color></PolyStyle>\n"
        placeMark = placeMark + '\t'*3 + '</Style>\n'
        placeMark = placeMark + '\t'*3 + '<Polygon>\n'
        placeMark = placeMark + '\t'*4 + '<outerBoundaryIs>\n'
        placeMark = placeMark + '\t'*5 + '<LinearRing>\n'
        placeMark = placeMark + '\t'*6 + '<coordinates>\n'
        placeMark = placeMark + '\t'*7 + coord + '\n'
        placeMark = placeMark + '\t'*6 + '</coordinates>\n'
        placeMark = placeMark + '\t'*5 + '</LinearRing>\n'
        placeMark = placeMark + '\t'*4 + '</outerBoundaryIs>\n'
        placeMark = placeMark + '\t'*3 + '</Polygon>\n'
        placeMark = placeMark + '\t'*2 + '</Placemark>\n'
        return placeMark



class HeatMapThread(QThread):  # 步骤1.创建一个线程实例
    stateSignal = Signal(str)
    def __init__(self, srcFileName,kmlFileName,heatNum): 
        super(HeatMapThread, self).__init__()
        self.srcFileName = srcFileName
        self.kmlFileName = kmlFileName
        self.heatNum = heatNum
        self.btAreas = {}
        self.areas = {}
        self.srcDf = pd.DataFrame()
        self.pointDf = pd.DataFrame()
    def run(self):
        try:
            self.stateSignal.emit('正在读取图层文件。。。')
            self.loadAreaCoord()
            self.stateSignal.emit('读取图层文件完成！')
            self.stateSignal.emit('正在读取热力值数据。。。')
            self.loadSrcFile()
            self.stateSignal.emit('读取热力值数据文件完成！')
            areaGrped = self.srcDf.groupby('归属区域')
            for areaGrp in areaGrped:
                area = areaGrp[0]
                tempPointDf = self.pointDf[self.pointDf['归属区域']==area]
                self.writeHeat(areaGrp[1],tempPointDf,area)
                self.stateSignal.emit(f'已生成区域【{area}】热力图！')
            self.stateSignal.emit('已生成所有热力图！')
        except:
            self.stateSignal.emit('读取热力值数据文件完成！')



    def loadAreaCoord(self):
        with open(self.kmlFileName,encoding='utf-8') as f:
            fileText = f.read()
        places = fileText.split('<Placemark>')
        coordRex = re.compile('<coordinates>(.*)</coordinates>',re.DOTALL)

        #字典，键为业务区名称，值为经纬度 list,为（经度，维度）元组
        for i in range(1,len(places)):
            if '<Polygon>' in places[i]:
                names = re.search('<name>(.*)</name>',places[i])
                coordinates = coordRex.search(places[i])
                if names and coordinates:
                    name = names.group(1)
                    coordinate = coordinates.group(1).strip()
                    points = coordinate.split(' ')
                    btPointList = []
                    pointList = []
                    for j in range(len(points)):
                        items = points[j].split(',')
                        try:
                            pointList.append((float(items[0]),float(items[1])))
                            tempX,tempY = wgs84_to_bd09(float(items[0]),float(items[1]))
                            btPointList.append('new BMap.Point(' + str(tempX) + ',' + str(tempY) + ')')
                        except ValueError:
                            pass
                    self.areas[name] = NetArea(pointList)
                    self.btAreas[name] = ',\n'.join(btPointList)

    def loadSrcFile(self):
        self.srcDf = pd.read_excel(self.srcFileName,sheet_name='热力数据')
        self.srcDf = self.srcDf[['热力点','经度','纬度','热力数据']]
        findArea_vec = np.vectorize(self.findArea)
        self.srcDf['归属区域'] = findArea_vec(self.srcDf['经度'],self.srcDf['纬度'])
        self.srcDf = self.srcDf[self.srcDf['归属区域'] != '-']
        self.pointDf = pd.read_excel(self.srcFileName,sheet_name='标记数据')
        if '备注' not in self.pointDf.columns:
            self.pointDf['备注'] = '无'
        self.pointDf = self.pointDf[['标记名称','经度','纬度','备注']]
        self.pointDf = self.pointDf.fillna('None')
        self.pointDf['归属区域'] = findArea_vec(self.pointDf['经度'],self.pointDf['纬度'])

    def findArea(self,lon,lat):
        for name,netArea in self.areas.items():
            if lon <= netArea.maxX and lon >= netArea.minX and lat <= netArea.maxY and lat >= netArea.minY:
                if IsPtInPoly(lon,lat,netArea.coordinates):
                    return name
                    break
        return '-'

    def writeHeat(self,heatDf,pointDf,area):
        heatDf['经度'] = heatDf['经度'].astype(float)
        heatDf['纬度'] = heatDf['纬度'].astype(float)
        vet_wsg_to_bd09 = np.vectorize(wgs84_to_bd09)
        heatDf['百度经度'],heatDf['百度纬度'] = vet_wsg_to_bd09(heatDf['经度'],heatDf['纬度'])
        heatDf['热力数据'] = heatDf['热力数据'].astype(int)
        Xmid = heatDf['百度经度'].mean()
        Ymid = heatDf['百度纬度'].mean()
        midPoint = str(Xmid) + ',' + str(Ymid)
        xyStr = self.xyPoints(list(heatDf['百度经度']),list(heatDf['百度纬度']),list(heatDf['热力数据']))
        radiusStr = str(int(self.heatNum/2))
        #画标记
        if pointDf.shape[0]>0:
            pointDf['经度'] = pointDf['经度'].astype(float)
            pointDf['纬度'] = pointDf['纬度'].astype(float)
            pointDf['百度经度'],pointDf['百度纬度'] = vet_wsg_to_bd09(pointDf['经度'],pointDf['纬度'])
            pointStr = self.markPoints(list(pointDf['百度经度']),list(pointDf['百度纬度']),list(pointDf['标记名称']),list(pointDf['备注']))
        else:
            pointStr = ''
        with open('assets/model.html','r', encoding='utf-8') as f:
            modStr = f.read()
        modStr = re.sub(r"<title>.*</title>",f"<title>{area}热力图</title>",modStr)
        modStr = re.sub("midPoint",midPoint,modStr)
        modStr = re.sub("userPointStr",xyStr,modStr)
        modStr = re.sub("pointStr",pointStr,modStr)
        modStr = re.sub("radiusStr",radiusStr,modStr)

        tempAreaCoord = self.btAreas[area]
        modStr = re.sub("AreaCoord",tempAreaCoord,modStr)
        with open(f'结果/{area}热力图.html','w',encoding='utf-8') as f:
            f.write(modStr)

    def xyPoints(self,x,y,num):
        heatPoints = []
        for i in range(len(x)):
            tempPoint = {'lat':y[i],'lng':x[i],'count':num[i]}
            heatPoints.append(str(tempPoint))
        xyStr = ',\n'.join(heatPoints)
        return xyStr

    def markPoints(self,x,y,name,description):
        points = []
        for i in range(len(x)):
            tempPoint = {'lng':x[i],'lat':y[i],'name':name[i],'description':description[i]}
            points.append(str(tempPoint))
        pointStr = ',\n'.join(points)
        return pointStr


class SiteLocationThread(QThread):
    stateSignal = Signal(str)
    def __init__(self, kmlFileName,objFileName):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(SiteLocationThread, self).__init__()
        self.kmlFileName = kmlFileName
        self.objFileName = objFileName
        self.areas = {}
    def run(self):
        try:
            self.stateSignal.emit('正在读取图层文件.')
            self.readAreas()
            self.stateSignal.emit('读取图层文件完成.')
            self.stateSignal.emit('正在读取需求文件.')
            pointDf = pd.read_excel(self.objFileName)
            self.stateSignal.emit('读取需求文件完成.')
            findArea_vec = np.vectorize(self.findArea)
            self.stateSignal.emit('分析需求点归属区域中，请稍后...')
            pointDf['归属区域'] = findArea_vec(pointDf['经度'],pointDf['纬度'])
            outFileName = self.objFileName.split('/')[-1].split('.')[0] + '【归属区域分析】.xlsx'
            pointDf.to_excel(f'结果/{outFileName}',index=False)
            self.stateSignal.emit(f'分析完成，具体看《结果》文件夹的{outFileName}')
        except Exception as e:
            self.stateSignal.emit(str(e))

    def readAreas(self):
        with open(self.kmlFileName,encoding='utf-8') as f:
            fileText = f.read()
        places = fileText.split('<Placemark>')
        coordRex = re.compile('<coordinates>(.*)</coordinates>',re.DOTALL)
        for i in range(1,len(places)):
            if '<Polygon>' in places[i]:
                names = re.search('<name>(.*)</name>',places[i])
                coordinates = coordRex.search(places[i])
                if names and coordinates:
                    name = names.group(1)
                    coordinate = coordinates.group(1).strip()
                    points = coordinate.split(' ')
                    pointList = []
                    for j in range(len(points)):
                        items = points[j].split(',')
                        pointList.append((float(items[0]),float(items[1])))
                    self.areas[name] = NetArea(pointList)

    def findArea(self,lon,lat):
        for name,netArea in self.areas.items():
            if lon <= netArea.maxX and lon >= netArea.minX and lat <= netArea.maxY and lat >= netArea.minY:
                if IsPtInPoly(lon,lat,netArea.coordinates):
                    return name
                    break
        return '-'

class NetArea():
    """docstring for NetArea"""
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.maxX = max(coordinates,key=itemgetter(0))[0]
        self.minX = min(coordinates,key=itemgetter(0))[0]
        self.maxY = max(coordinates,key=itemgetter(1))[1]
        self.minY = min(coordinates,key=itemgetter(1))[1]


class SearchThread(QThread):
    stateSignal = Signal(str)
    def __init__(self, srcFileName,objFileName,distance):  #通过初始化赋值的方式实现UI主线程传递值给子线程
        super(SearchThread, self).__init__()
        self.srcFileName = srcFileName
        self.objFileName = objFileName
        self.distance = distance
        self.objDf = pd.DataFrame()
        self.srcDf = pd.DataFrame()
        self.CalcDistance_vec = np.vectorize(CalcDistance)
    def run(self):
        try:
            self.stateSignal.emit('正在读取需求文件。。。')
            self.srcDf = pd.read_excel(self.srcFileName)
            self.srcDf = self.srcDf[['需求名称','经度','纬度']]
            self.stateSignal.emit('读取需求文件完成！')
            self.stateSignal.emit('正在读取资源文件。。。')
            self.objDf = pd.read_excel(self.objFileName)
            self.objDf = self.objDf[['资源名称','经度','纬度']]
            self.stateSignal.emit('读取资源文件完成！')
            lons = list(self.srcDf['经度'])
            lats = list(self.srcDf['纬度'])
            sites = list(self.srcDf['需求名称'])
            result = pd.DataFrame()
            siteNum = len(sites)
            for i in range(siteNum):
                tempResultDf = self.NearbySite(lons[i],lats[i])
                if tempResultDf.shape[0]==0:
                    tempResultDf = pd.DataFrame({'需求名称':[sites[i]],
                        '需求点经度':[lons[i]],
                        '需求点纬度':[lats[i]],
                        '经度':[''],'纬度':[''],'距离':[f'{self.distance}km附近无接入点']})
                else:
                    tempResultDf['需求名称'] = sites[i]
                result = pd.concat([result,tempResultDf])
                self.stateSignal.emit(f'需求分析中：{i}/{siteNum}')
            outFileName = self.srcFileName.split('/')[-1].split('.')[0] + f'{self.distance}km周边资源情况.xlsx'
            result = result[['需求名称','需求点经度','需求点纬度','资源名称','经度','纬度','距离']]
            nearest = result.groupby('需求名称').head(1)
            self.stateSignal.emit(f'周边资源情况分析完成,生成结果表格中。。。')
            with pd.ExcelWriter(f'结果/{outFileName}',engine='xlsxwriter') as writer:
                result.to_excel(writer,sheet_name=f'{self.distance}km周边资源总表',index=False)
                nearest.to_excel(writer,sheet_name='最近资源',index=False)
            self.stateSignal.emit(f'分析结果详细见《结果》文件夹的{outFileName}表格！')
        except Exception as e:
            self.stateSignal.emit(str(e))

    def NearbySite(self,alon,alat):
        lonUpLimit = alon + self.distance/100
        lonDownLimit = alon - self.distance/100
        latUpLimit = alat + self.distance/100
        latDownLimit = alat - self.distance/100
        resultDf = pd.DataFrame()
        tempAllDf = self.objDf.copy()
        tempDf = tempAllDf[tempAllDf['经度'] <lonUpLimit].copy()
        if tempDf.shape[0] == 0:
            return resultDf
        tempDf = tempDf[tempDf['经度'] >lonDownLimit]
        if tempDf.shape[0] == 0:
            return resultDf
        tempDf = tempDf[tempDf['纬度'] >latDownLimit]
        if tempDf.shape[0] == 0:
            return resultDf
        tempDf = tempDf[tempDf['纬度'] <latUpLimit]
        if tempDf.shape[0] == 0:
            return resultDf
        tempDf['需求点经度'] = alon
        tempDf['需求点纬度'] = alat
        tempDf['距离'] = self.CalcDistance_vec(tempDf['需求点纬度'],tempDf['需求点经度'],tempDf['纬度'],tempDf['经度'])
        resultDf = tempDf.copy() 
        resultDf.sort_values(by=['距离'],ascending=[True],inplace=True)
        resultDf = resultDf[resultDf['距离']<=self.distance]
        return resultDf


class FuzzyThread(QThread):
	stateSignal = Signal(str)
	def __init__(self, srcFileName,objFileName,typeIndex,notMatchStr):  #通过初始化赋值的方式实现UI主线程传递值给子线程
		super(FuzzyThread, self).__init__()
		self.srcFileName = srcFileName
		self.objFileName = objFileName
		self.typeIndex = typeIndex
		self.notMatchStr = notMatchStr

	def run(self):
		self.stateSignal.emit('正在读取需求文件。。。')
		try:
			with open(self.srcFileName,'r',encoding='UTF-8') as f:
				srcStrs = f.read().splitlines()
			self.stateSignal.emit('读取需求文件完成！')
			with open(self.objFileName,'r',encoding='UTF-8') as f:
				objStrs = f.read().splitlines()
		except:
			self.stateSignal.emit('请核查选择文件是否为UTF-8编码！')
			return;
		try:
			self.stateSignal.emit('读取匹配库文件完成！')
			self.srcDf = pd.DataFrame({'匹配需求':srcStrs})
			self.fixSrc()
			self.stateSignal.emit('正在匹配中，请稍后....')
			outFileName = self.srcFileName.split('/')[-1].split('.')[0]
			if self.typeIndex == 0:
				self.srcDf['匹配结果'],self.srcDf['匹配双字符数量'],self.srcDf['相同双字符'] = zip(*self.srcDf['匹配列'].apply(lambda x: mostTwoLike(x,objStrs)))
				outFileName = outFileName + '双字符匹配结果.xlsx'
				self.srcDf.to_excel(f'结果/{outFileName}',index=False)
			elif self.typeIndex == 1:
				self.srcDf['匹配结果'],self.srcDf['匹配最长字符数量'],self.srcDf['相同字符段'] = zip(*self.srcDf['匹配列'].apply(lambda x: mostLongestLike(x,objStrs)))
				outFileName = outFileName + '最长字符匹配结果.xlsx'
				self.srcDf.to_excel(f'结果/{outFileName}',index=False)
			else:
				self.srcDf['匹配结果'],self.srcDf['匹配单字符数量'],self.srcDf['相同单字符'] = zip(*self.srcDf['匹配列'].apply(lambda x: mostOneLike(x,objStrs)))
				outFileName = outFileName + '单字符匹配结果.xlsx'
				self.srcDf.to_excel(f'结果/{outFileName}',index=False)					
			self.stateSignal.emit(f'匹配完成，具体《结果》文件夹{outFileName}')
		except Exception as e:
			self.stateSignal.emit(str(e))
            
	def fixSrc(self):
		notMatchKeys = self.notMatchStr.split('、')
		self.srcDf['匹配列'] = self.srcDf['匹配需求'].apply(lambda x: re.sub(notMatchKeys[0],'',x))
		for i in range(1,len(notMatchKeys),1):
			self.srcDf['匹配列'] = self.srcDf['匹配列'].apply(lambda x: re.sub(notMatchKeys[i],'',x))
