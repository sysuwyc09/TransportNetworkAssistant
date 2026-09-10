# -*- coding: utf-8 -*-
"""
主入口 - MainWindow
含 1 个按钮，点击调用 TransportPredict 模块窗口。
运行：python mainwindow.py
"""
import sys

from PySide6 import QtCore, QtGui, QtWidgets

import resources_rc  # noqa: F401  注册 Qt 图标资源
from TransportPredict import TransportPredict


class MainWindow(QtWidgets.QMainWindow):
    """主窗口 - 一个按钮启动传输资源预测模块。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('传输资源预测 - 主入口')
        self.resize(420, 240)
        self.setWindowIcon(QtGui.QIcon(":/icons/assets/olt.svg"))

        # 中央 widget
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        # 垂直布局：标题 + 按钮
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QtWidgets.QLabel(
            '<h2>传输资源预测系统</h2>'
            '<p style="color:#666;">基于 OBD 端子数据预测 OLT 站点 PON 口需求</p>',
            central
        )
        title.setTextFormat(QtCore.Qt.RichText)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.btnLaunch = QtWidgets.QPushButton('启动传输资源预测', central)
        self.btnLaunch.setIcon(QtGui.QIcon(":/icons/assets/run.svg"))
        self.btnLaunch.setMinimumHeight(48)
        # 按钮样式
        self.btnLaunch.setStyleSheet(
            'QPushButton {'
            '  font-size: 14px;'
            '  padding: 8px 16px;'
            '  background-color: #4A90E2;'
            '  color: white;'
            '  border: none;'
            '  border-radius: 4px;'
            '}'
            'QPushButton:hover { background-color: #357ABD; }'
            'QPushButton:pressed { background-color: #2A5F94; }'
        )
        self.btnLaunch.clicked.connect(self.on_launch)
        layout.addWidget(self.btnLaunch)

        # 子窗口引用（防止被 GC）
        self._child_window = None

    def on_launch(self):
        """启动 TransportPredict 模块窗口。"""
        if self._child_window is not None:
            # 已存在则前置
            self._child_window.show()
            self._child_window.raise_()
            self._child_window.activateWindow()
            return
        self._child_window = TransportPredict(self)
        self._child_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # 子窗口关闭时清空引用
        self._child_window.destroyed.connect(self._on_child_destroyed)
        self._child_window.show()

    def _on_child_destroyed(self, *args):
        self._child_window = None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
