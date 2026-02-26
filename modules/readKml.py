#！python
#读取谷歌kml图层点、线资源名称、经纬度
#
import re
from math import asin,cos,sin,sqrt,pi,fabs

class KmlLinePlace():
	"""定义一个线资源的类"""
	def __init__(self,name,coordinate):
		self.name = name
		self.coordinate = ''.join(coordinate.split())
		self.length = 0
		points=self.coordinate.split(",0")
		for i in range(0,len(points)-2):
			lon1 = float(re.search('(.*),',points[i]).group(1))
			lat1 = float(re.search(',(.*)',points[i]).group(1))
			lon2 = float(re.search('(.*),',points[i+1]).group(1))
			lat2 = float(re.search(',(.*)',points[i+1]).group(1))
			self.length += self.CalcDistance(lat1,lon1,lat2,lon2)
		self.length = round(self.length/1000,2)
		self.coordinate = ',0 '.join(points[:-1]) + ',0 '
	def CalcDistance(self,lat1,lon1,lat2,lon2):
		"""计算先两点之间距离"""
		Distance = 6378137 * 2 * asin(sqrt(self.SumSq(sin((self.Radians(lat1) - self.Radians(lat2)) / 2)) + cos(self.Radians(lat1)) * \
			cos(self.Radians(lat2)) * self.SumSq(sin((self.Radians(lon1) - self.Radians(lon2)) / 2))))
		return Distance
	def Radians(self,latORlon):
		PI14 = 3.14159265358979
		Radian = latORlon * PI14 / 180
		return Radian
	def SumSq(self,xx):
		SumS = xx * xx
		return SumS

class KmlPointPlace():
	"""定义一个点资源的类"""
	def __init__(self,name,latitude,longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

class KmlPolygonPlace():
	"""定义一个点资源的类"""
	def __init__(self,name,coordinate):
		self.name = name
		self.coordinate = coordinate
		self.area = self.CalculatePolygonArea(coordinate)
	def  ConvertToRadian(self,input):
		return input * pi / 180
	def CalculatePolygonArea(self,coordinate):
		area = 0
		arr = coordinate.split(',0 ')
		arr_len = len(arr)-1
		if arr_len < 3:
			return 0.0
		temp = []
		for i in range(0, arr_len):
			temp.append([float(x) for x in arr[i].split(',')])
		for i in range(0, arr_len):
			area += self.ConvertToRadian(temp[(i + 1) % arr_len][0] - temp[(i) % arr_len][0]) * \
				(2 + sin(self.ConvertToRadian(temp[(i) % arr_len][1])) + sin(self.ConvertToRadian(temp[(i + 1) % arr_len][1])))
		area = area * 6378137.0 * 6378137.0 / 2.0/1000000
		return round(fabs(area),6)