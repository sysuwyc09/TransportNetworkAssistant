# 自定义widgets
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer, QTime,QPoint,QEvent
from PySide6.QtGui import *
from PySide6.QtCharts import QChart, QChartView, QPieSeries,QBarSet, QBarSeries, QChart, QChartView, QBarCategoryAxis,QPieSlice,QLegend
import math
import re


class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.target_value = 0
        self.min_value = 0
        self.max_value = 100
        self.progress_width = 50
        self.text_color = QColor(0, 170, 255)
        self.font_size = 20
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_duration = 100  # 2秒动画
        self.animation_start_time = 0
        self.animation_start_value = 0
        
    def setValue(self, value):
        self.target_value = min(max(value, self.min_value), self.max_value)
        self.animation_start_value = self.value
        self.animation_start_time = QTime.currentTime().msecsSinceStartOfDay()
        self.timer.start(16)  # 约60帧/秒
        
    def update_animation(self):
        current_time = QTime.currentTime().msecsSinceStartOfDay()
        elapsed = current_time - self.animation_start_time
        
        if elapsed >= self.animation_duration:
            self.value = self.target_value
            self.timer.stop()
        else:
            # 使用缓动函数使动画更平滑
            progress = elapsed / self.animation_duration
            self.value = int(self.animation_start_value + 
                           (self.target_value - self.animation_start_value) * 
                           (1 - (1 - progress) ** 3))  # 三次缓动
            
        self.update()
        
    def paintEvent(self, event):
        width = min(self.width(), self.height()) - self.progress_width
        progress = (self.value - self.min_value) / (self.max_value - self.min_value) * 360
        # 修正颜色逻辑
        if self.value >= 90:
            color = QColor(255, 0, 0)  # 红色
        elif self.value >= 70:
            color = QColor(255, 165, 0)  # 橙色
        elif self.value >= 50:
            color = QColor(255, 215, 0)  # 金色
        else:
            color = QColor(0, 255, 0)  # 绿色    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景圆
        pen = QPen()
        pen.setColor(QColor(200, 200, 200))
        pen.setWidth(self.progress_width)
        painter.setPen(pen)
        painter.drawEllipse(self.progress_width//2, self.progress_width//2, 
                           width, width)
        
        # 绘制进度圆
        pen.setColor(color)
        painter.setPen(pen)
        painter.drawArc(self.progress_width//2, self.progress_width//2, 
                       width, width, 90 * 16, -progress * 16)
        
        # 绘制百分比文本
        font = QFont()
        font.setPixelSize(self.font_size)
        painter.setFont(font)
        painter.setPen(QPen(self.text_color))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")


class PieChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        
        # 深色主题配色方案
        self.slice_colors = [
            QColor(50, 205, 50),   # 酸橙绿
            QColor(138, 43, 226),  # 紫罗兰
            QColor(0, 255, 255),   # 青色
            QColor(255, 0, 255)    # 洋红
        ]
        
        # 设置深色背景
        self.setDarkTheme()
        
    def setDarkTheme(self):
        """应用深色主题设置"""
        # 背景色
        self.chart.setBackgroundBrush(QBrush(QColor(28, 33, 44)))
        # 标题颜色
        self.chart.setTitleBrush(QBrush(QColor(68, 204, 136)))  # #44cc88
        # 图例颜色
        self.chart.legend().setLabelColor(QColor(68, 204, 136))
        
    def setData(self, data_dict,title):
        """设置数据，自动循环使用预设颜色"""
        series = QPieSeries()
        self.chart.setTitle(title)
        names = []
        # 添加数据切片并应用颜色
        for i, (name, value) in enumerate(data_dict.items()):
            names.append(name)
            slice = series.append(name, value)
            slice.setLabel(f"{value}")
            slice.setLabelVisible(True)  # 重新显示标签
            # 设置标签字体大小（缩小至10px）
            label_font = QFont()
            label_font.setPixelSize(10)  # 调整此值可改变标签大小
            slice.setLabelFont(label_font)
            slice.setLabelPosition(QPieSlice.LabelOutside)
            # 循环使用预设颜色
            color_index = i % len(self.slice_colors)
            slice.setBrush(self.slice_colors[color_index])
            slice.setLabelBrush(self.slice_colors[color_index])
            
        self.chart.removeAllSeries()
        self.chart.addSeries(series)
        legend = self.chart.legend()
        legend.setVisible(True)
        legend.setAlignment(Qt.AlignBottom)
        # 获取所有图例标记并设置为原始name
        markers = legend.markers(series)
        for i, marker in enumerate(markers):
            if i < len(names):
                marker.setLabel(names[i])
        



class BarChartView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        # 预定义16种颜色（可根据需要扩展）
        self.color_palette = [
            QColor(65, 105, 225),   # 皇家蓝
            QColor(220, 20, 60),    # 猩红
            QColor(50, 205, 50),    # 酸橙绿
            QColor(255, 165, 0),    # 橙色
            QColor(138, 43, 226),   # 紫罗兰
            QColor(0, 255, 255),    # 青色
            QColor(255, 0, 255),    # 洋红
            QColor(255, 215, 0),    # 金色
            QColor(0, 139, 139),    # 深青色
            QColor(148, 0, 211),    # 深紫罗兰
            QColor(255, 99, 71),    # 番茄色
            QColor(60, 179, 113),   # 海洋绿
            QColor(238, 130, 238),  # 紫罗兰
            QColor(255, 140, 0),    # 深橙色
            QColor(70, 130, 180),   # 钢蓝色
            QColor(205, 92, 92)     # 印度红
        ]
        # 设置深色主题
        self.setDarkTheme()
    def setDarkTheme(self):
        """应用深色主题设置"""
        self.chart.setBackgroundBrush(QBrush(QColor(13, 9, 36)))
        self.chart.setTitleBrush(QBrush(QColor(255, 255, 255)))
        self.chart.legend().setLabelColor(QColor(200, 200, 200))
    
    def setData(self, data_dict, title):
        self.chart.removeAllSeries()  
        # 获取所有分类
        categories = {category for class_data in data_dict.values() 
                           for category in class_data.keys()}
        # 为每个分类创建QBarSet并分配颜色
        bar_sets = {}
        for i, category in enumerate(categories):
            bar_set = QBarSet(category)
            bar_sets[category] = bar_set
            
            # 循环使用颜色调色板
            color_index = i % len(self.color_palette)
            bar_set.setColor(self.color_palette[color_index])
        
        # 填充数据
        class_names = []
        for class_name, class_data in data_dict.items():
            class_names.append(class_name)
            for category in categories:
                value = class_data.get(category, 0)
                bar_sets[category].append(value)
        
        # 创建柱状图系列并添加数据
        series = QBarSeries()
        for bar_set in bar_sets.values():
            series.append(bar_set)
            
        # 启用标签显示并设置格式
        series.setLabelsVisible(True)
        series.setLabelsFormat("@value")
        
        self.chart.addSeries(series)
        
        # 设置X轴
        axisX = QBarCategoryAxis()
        axisX.append(class_names)
        axisX.setLabelsColor(QColor(255, 255, 255))
        axisX.setLinePenColor(QColor(255, 255, 255))
        self.chart.setAxisX(axisX, series)
        
        # 设置图表标题和图例
        self.chart.setTitle(title)
        self.chart.legend().setVisible(True)
        # legend右侧
        self.chart.legend().setAlignment(Qt.AlignRight)

class OltBoardView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        
    def drawBoard(self, data_dict):
        self.scene.clear()
        if not data_dict:  # 空数据处理
            return
            
        # 颜色定义
        colors = {
            0: QColor(128, 128, 128),  # 灰色
            2: QColor(255, 165, 0),    # 橙色
            1: QColor(0, 255, 0)       # 绿色
        }
        
        # 视图尺寸（限制宽度440，高度使用视图实际高度）
        view_width = 448  # 整体宽度不超过450
        view_height = max(self.height(), 100)  # 取消固定高度限制，使用视图高度（最小100防过小）
        # 缩小边距（增加可用空间）
        margin = 5
        available_width = view_width - 2 * margin
        
        row_count = len(data_dict)
        if row_count == 0:
            return
        
        for row_idx, (key, values) in enumerate(data_dict.items()):
            row_y = margin + row_idx * 30  # 垂直分布
            # 1. 绘制Key文本（限制最大宽度）
            key_text = self.scene.addText(str(key))
            key_text.setPos(margin, row_y)
            key_text.adjustSize()
            # 文本颜色根据状态值设置
            key_text.setDefaultTextColor(colors[1])  # colors[1]对应绿色
            key_width = key_text.boundingRect().width()
            if key_width > available_width * 0.15:  # 文本最大占10%宽度
                key_text.setScale(0.8)  # 超宽时缩小文本
                key_width *= 0.8
            
            # 2. 图表区域宽度（压缩文本与图表间距）
            chart_area_width = available_width - key_width - 15  # 间距15
            if chart_area_width <= 0:
                continue
            
            # 3. 绘制矩形框（使用限制后的行高）
            rect_x = margin + key_width + 10
            rect_height = 20
            rect_pen = QPen(colors[1])
            rect = self.scene.addRect(rect_x, row_y + 2, chart_area_width, rect_height,rect_pen)
            
            # 4. 绘制圆形（直径固定18）
            if len(values) == 0:
                continue
            circle_diameter = 17  # 圆形直径固定18
            max_circles = 16  # 最多显示16个圆
            values = values[:max_circles]  # 截断超出的圆
            num_circles = len(values)
            spacing = 5  # 固定间距（可根据需要调整）
            
            # 绘制圆形（水平分布）
            start_x = rect_x + 8  # 矩形内左边距8
            for i, value in enumerate(values):
                x = start_x + i * (circle_diameter + spacing)
                y = row_y + 2 + (rect_height - circle_diameter) / 2  # 垂直居中
                # 绘制圆形
                circle = self.scene.addEllipse(x, y, circle_diameter, circle_diameter)
                circle.setBrush(QBrush(colors.get(value, QColor(0, 0, 0))))
                
                # 添加圆心编号（白色小字体）
                number_text = self.scene.addText(str(i))  # 编号从1开始
                number_text.setDefaultTextColor(QColor(0, 0, 0))  
                # 设置小字体（8px）并加粗
                font = QFont()
                font.setPixelSize(8)  # 缩小字体以适应圆内
                font.setBold(True)
                number_text.setFont(font)
                # 文本居中定位
                text_rect = number_text.boundingRect()
                text_x = x + (circle_diameter - text_rect.width()) / 2  # 水平居中
                text_y = y + (circle_diameter - text_rect.height()) / 2  # 垂直居中
                number_text.setPos(text_x, text_y)
        
        # 添加底部图例说明（居中显示）
        legend_text = self.scene.addText("绿色：占用，橙色：预占，灰色：空闲")
        legend_text.setDefaultTextColor(QColor(0, 255, 0))  # 绿色文本
        # 设置字体大小
        font = QFont()
        font.setPixelSize(10)
        legend_text.setFont(font)
        # 计算居中位置
        text_rect = legend_text.boundingRect()
        legend_x = (view_width - text_rect.width()) / 2  # 水平居中
        legend_y = row_y + 25  # 底部上方5px
        legend_text.setPos(legend_x, legend_y)

        self.scene.setSceneRect(0, 0, view_width, legend_y+30)
        
class TopologyView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置场景
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        # 设置视图属性
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 初始化数据
        self.data = []
        
        # # 设置场景大小
        # self.scene.setSceneRect(0, 0, 854, 125)
    
    def setData(self, topology_string):
        """设置拓扑数据（接受字符串格式）并重新绘制视图"""
        # 解析字符串为内部数据结构
        self.data = self.parseTopologyString(topology_string)
        self.drawTopology()  # 重新绘制拓扑图
    
    def parseTopologyString(self, topology_string):
        """解析拓扑字符串为内部数据结构，修复多站点解析问题"""
        data = []
        remaining = topology_string.strip()
        
        # 提取第一个站点
        match = re.match(r"^([^<]+)", remaining)
        if not match:
            return data
            
        first_station = match.group(1).strip()
        data.append({"name": first_station})
        remaining = remaining[len(match.group(0)):].strip()
        
        # 循环解析连接和后续站点
        pattern = r"^<=\{([^}]+)\}\((\d+)/(\d+)\)=>([^<]+)"
        while remaining:
            match = re.match(pattern, remaining)
            if not match:
                break
                
            # 连接信息
            conn_name = match.group(1).strip()
            used = int(match.group(2))
            total = int(match.group(3))
            next_station = match.group(4).strip()
            
            # 添加连接和下一个站点
            data.append({"name": conn_name, "total": total, "used": used})
            data.append({"name": next_station})
            
            # 更新剩余字符串
            remaining = remaining[len(match.group(0)):].strip()
        
        return data
    
    def drawTopology(self):
        """绘制拓扑结构，先清除现有内容"""
        # 清除场景中所有项目
        self.scene.clear()
        
        if not self.data:  # 如果没有数据，直接返回
            return
        
        # 初始位置和间距
        start_x = 50
        y = 40
        station_spacing = 160
        
        # 计算总长度，动态调整场景宽度
        stations_count = sum(1 for item in self.data if "total" not in item)
        total_width = 50 + (stations_count - 1) * station_spacing + 50
        self.scene.setSceneRect(0, 0, max(total_width, 600), 125)
        
        # 绘制站点和连接
        for item in self.data:
            if "total" not in item:  # 站点
                # 绘制站点
                self.drawStation(item["name"], start_x, y)
                start_x += station_spacing
            else:  # 连接
                # 绘制连接
                self.drawConnection(
                    item["name"], 
                    item["total"], 
                    item["used"], 
                    start_x - station_spacing + 30,  # 从上个站点右侧开始
                    y,
                    start_x - 30  # 到当前站点左侧结束
                )
    
    def drawStation(self, name, x, y):
        """绘制站点，名称过长时自动换行"""
        # 站点圆形
        station = self.scene.addEllipse(
            x - 15, y - 15, 30, 30,
            QPen(QColor(0, 0, 0)),
            QBrush(QColor(100, 149, 237))  # CornflowerBlue
        )
        station.setZValue(2)  # 确保站点在连接线上面
        
        # 站点名称 - 支持自动换行
        text = self.scene.addText(name)
        font = QFont()
        font.setFamily("SimHei")
        text.setFont(font)
        text.setDefaultTextColor(QColor(0, 255, 0))
        
        # 设置最大宽度，超过则自动换行
        max_text_width = 100  # 可根据需要调整
        text.setTextWidth(max_text_width)
        
        # # 计算文本位置，使其居中显示在站点下方
        # text_rect = text.boundingRect()
        text_x = x - max_text_width / 2 + 5
        text_y = y + 20  # 站点下方20像素处
        text.setPos(text_x, text_y)
        text.setZValue(3)
    
    def drawConnection(self, name, total_width, used_width, start_x, y, end_x):
        """绘制连接线路，已删除连接线名称"""
        # 背景线（总带宽）- 绿色
        if used_width > 6:
            color = QColor(0, 255, 0)  # ForestGreen
        else:
            color = QColor(255, 0, 0)  # Red
        total_pen = QPen(color)
        total_pen.setWidth(total_width/10)
        total_line = self.scene.addLine(start_x, y, end_x, y, total_pen)
        total_line.setZValue(0)

        # 带宽信息
        bandwidth_text = self.scene.addText(f"{used_width}/{total_width}")
        mid_x = (start_x + end_x) / 2
        bandwidth_text.setPos(mid_x - bandwidth_text.boundingRect().width() / 2, y + 15)
        bandwidth_text.setZValue(3)
        
        # 设置字体确保中文显示
        font = QFont()
        font.setFamily("SimHei")
        bandwidth_text.setFont(font)
        bandwidth_text.setDefaultTextColor(color)

# 自定义个窗体包含QTableWidget，用于显示查找中继段资源的结果,自动弹出并居中显示
class RelayLineResultDialog(QWidget):
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("中继段资源查询结果")
        # 启用最小化按钮
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)
        self.resize(800, 400)  # 设置合适的初始大小
        self.initUI(df)
        # 添加关闭回调函数
        self.close_callback = None

    def setCloseCallback(self, callback):
        """设置窗口关闭时的回调函数"""
        self.close_callback = callback

    def closeEvent(self, event):
        """重写关闭事件，确保回调函数被调用"""
        if self.close_callback:
            self.close_callback(self)
        super().closeEvent(event)

    def initUI(self,df):
        self.layout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.layout.addWidget(self.tableWidget)
        # 添加是否复制标题行的复选框
        self.copyHeaderCheckbox = QCheckBox("复制时包含标题行")
        self.copyHeaderCheckbox.setChecked(False)  # 默认不复制标题行
        self.layout.addWidget(self.copyHeaderCheckbox)
        self.setLayout(self.layout)
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setHorizontalHeaderLabels(df.columns.tolist())
        for i,row in df.iterrows():
            for j,val in enumerate(row):
                self.tableWidget.setItem(i,j,QTableWidgetItem(str(val)))
        # 自动调整列宽
        self.tableWidget.resizeColumnsToContents()
        # 根据总列宽调整对话框宽度
        total_width = self.tableWidget.horizontalHeader().length()
        self.resize(total_width + 70, self.height())  # 增加一些边距
        # 启用多选和扩展选择模式
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        
        # 安装事件过滤器以捕获键盘事件
        self.tableWidget.installEventFilter(self)

    def eventFilter(self, obj, event):
        """事件过滤器，用于捕获Ctrl+C快捷键"""
        if obj == self.tableWidget and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                self.copySelectedCells()
                return True
        return super().eventFilter(obj, event)

    def copySelectedCells(self):
        """复制选中的单元格内容到剪贴板"""
        selection = self.tableWidget.selectedRanges()
        if not selection:
            return
        # 获取选中的单元格范围
        selected_range = selection[0]
        top_row = selected_range.topRow()
        bottom_row = selected_range.bottomRow()
        left_col = selected_range.leftColumn()
        right_col = selected_range.rightColumn()
        # 构建复制文本
        clipboard_text = ""
        # 复制表头（根据复选框状态决定）
        if self.copyHeaderCheckbox.isChecked():
            headers = []
            for col in range(left_col, right_col + 1):
                header_item = self.tableWidget.horizontalHeaderItem(col)
                if header_item:
                    headers.append(header_item.text())
                else:
                    headers.append("")
            if headers:
                clipboard_text += "\t".join(headers) + "\n"
        # 复制单元格内容
        for row in range(top_row, bottom_row + 1):
            row_data = []
            for col in range(left_col, right_col + 1):
                item = self.tableWidget.item(row, col)
                if item and item.text():
                    row_data.append(item.text())
                else:
                    row_data.append("")
            clipboard_text += "\t".join(row_data) + "\n"
        
        # 复制到剪贴板
        if clipboard_text.strip():
            QApplication.clipboard().setText(clipboard_text.strip())
        





