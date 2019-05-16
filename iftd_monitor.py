# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Wang Xueliang
# Date: 2019/5/13

import sys

import pyqtgraph as pg
import numpy as np
import pandas as pd
import array

from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QSpacerItem,
                             QHBoxLayout, QSizePolicy, QPushButton, QApplication)
from pyqtgraph import GraphicsView


class IFTDMonitor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plot_item_row = 2
        self.plot_item_col = 3

        self.test_data = None
        self.data_list = []
        for i in range(self.plot_item_row * self.plot_item_col):
            self.data_list.append(array.array('d'))
        self.plot_item_list = []
        self.curve_list = []

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(1200, 600)
        self.setWindowIcon(QIcon('window.ico'))
        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.main_graphics = GraphicsView(self.centralwidget)
        self.verticalLayout.addWidget(self.main_graphics)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_start = QPushButton(self.centralwidget)
        self.horizontalLayout.addWidget(self.btn_start)
        self.btn_read_data = QPushButton(self.centralwidget)
        self.horizontalLayout.addWidget(self.btn_read_data)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        self.translate_lang()
        self.custom_graphics_view_layout()

        for pi in self.plot_item_list:
            self.curve_list.append(pi.plot(pen='g'))
        self.idx = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_data)
        self.btn_start.clicked.connect(self.start_plot)
        self.btn_read_data.clicked.connect(self.read_data)

    def custom_graphics_view_layout(self):
        self.main_graphics.setBackground('303030')
        # 创建布局器
        gra_layout = pg.GraphicsLayout()
        # 依次在布局器中添加2*3个坐标，并设置坐标属性
        y_label = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(self.plot_item_row):
            for j in range(self.plot_item_col):
                # 添加坐标
                pw = gra_layout.addPlot(row=i, col=j)
                # 隐藏自动缩放按钮
                pw.hideButtons()
                # 显示网格
                pw.showGrid(x=True, y=True)
                # 显示脊线
                pw.showAxis('right')
                r_axis = pw.getAxis('right')
                r_axis.setStyle(showValues=False)
                pw.showAxis('top')
                t_axis = pw.getAxis('top')
                t_axis.setStyle(showValues=False)
                # 设置范围
                pw.setRange(xRange=[0, 200], yRange=[-1.2, 1.2], padding=0)
                # 设置标注
                pw.setLabel('left', text=y_label[i + j])
                pw.setLabel('bottom', text='Time', units='s')
                # 设置自适应坐标范围
                pw.enableAutoRange(pg.ViewBox.YAxis, True)
                self.plot_item_list.append(pw)
        self.main_graphics.setCentralWidget(gra_layout)

    def plot_data(self):
        for i, data in enumerate(self.data_list):
            # tmp = np.sin(np.pi / 50 * self.idx + 2 * np.pi * i / self.plot_item_col / self.plot_item_row)
            tmp = self.test_data.iloc[self.idx, i]
            if len(data) < 200:
                data.append(tmp)
            else:
                data[:-1] = data[1:]
                data[-1] = tmp

        for i, curve in enumerate(self.curve_list):
            curve.setData(self.data_list[i])

        self.idx += 1

    def read_data(self):
        self.test_data = pd.read_csv('E:\\FTD\\FTPD-C919-10102-DY-190115-F-01-FTECAOWEN-ANA001-32.txt', sep='\s+',
                         usecols=[1, 2, 3, 4, 5, 6], index_col=False, engine='c',
                         skip_blank_lines=True)
        print('Read Done.')

    def start_plot(self):
        self.timer.start(20)

    def translate_lang(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', 'IFTD MONITOR'))
        self.btn_start.setText(_translate('MainWindow', 'Start'))
        self.btn_read_data.setText(_translate('MainWindow', 'Read Data'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = IFTDMonitor()
    mw.show()
    sys.exit(app.exec_())

# app = pg.mkQApp()
#
# data = array.array('d')
# N = 200
# win = pg.GraphicsWindow()
# win.setWindowTitle(u'WaveGraph')
# win.resize(500, 300)
#
# p = win.addPlot()
# p.showGrid(x=True, y=True)
# p.setRange(xRange=[0, N-1], yRange=[-1.2, 1.2], padding=0)
# p.setLabels(left='y / V', bottom='x / point', title='y = sin(x)')
#
# curve = p.plot(pen='y')
# idx = 0
#
#
# def plot_data():
#     global idx
#     tmp = np.sin(np.pi / 50 * idx)
#     if len(data) < N:
#         data.append(tmp)
#     else:
#         data[:-1] = data[1:]
#         data[-1] = tmp
#
#     curve.setData(data)
#     idx += 1
#
#
# timer = pg.QtCore.QTimer()
# timer.timeout.connect(plot_data)
# timer.start(30)
#
# app.exec_()
