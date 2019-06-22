# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Wang Xueliang
# Date: 2019/5/13

import sys
import threading
import time

import pyqtgraph as pg
import numpy as np
import pandas as pd
# import array

from PyQt5.QtCore import Qt, QTimer, QObject
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication,
                             QToolBar, QAction, QStackedWidget, QDialog,
                             QMessageBox)

from pyqtgraph import GraphicsView

from para_info import (PARA_LIST, TIME_PARA_LEFT, TIME_PARA_RIGHT, TIME_RANGE_PARA_LEFT,
                       TIME_RANGE_PARA_RIGHT)
from setting_dialog import SettingDialog
from DataConnection import DataConnection


class IFTDMonitor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # UI界面
        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(1200, 600)
        self.setWindowIcon(QIcon('window.ico'))

        # 创建工具栏
        self.toolBar = QToolBar(self)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.action_start = QAction(self)
        self.action_start.setText('Start')
        # self.action_start.setIcon(QIcon('window.ico'))
        # self.action_start.setIconText('Start')
        self.action_read_data = QAction(self)
        self.action_read_data.setText('Read Data')
        self.action_show_left_engine = QAction(self)
        self.action_show_left_engine.setText('Left Engine')
        self.action_show_left_engine.setCheckable(True)
        self.action_show_left_engine.setChecked(True)
        self.action_show_right_engine = QAction(self)
        self.action_show_right_engine.setText('Right Engine')
        self.action_show_right_engine.setCheckable(True)
        self.action_setting = QAction(self)
        self.action_setting.setText('Setting')
        self.action_connect_udp = QAction(self)
        self.action_connect_udp.setText('Connect')
        self.action_disconnect_udp = QAction(self)
        self.action_disconnect_udp.setText('Disconnect')
        self.toolBar.addActions([self.action_show_left_engine,
                                 self.action_show_right_engine,
                                 self.action_connect_udp,
                                 self.action_disconnect_udp,
                                 self.action_start,
                                 self.action_read_data,
                                 self.action_setting])

        # 创建信息栏
        self.status_bar = self.statusBar()

        self.centralwidget = QWidget(self, flags=Qt.Widget)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.stack_window = QStackedWidget(self.centralwidget)

        self.left_eng_win = QWidget(self.stack_window, flags=Qt.Widget)
        self.vlayout_left_eng = QVBoxLayout(self.left_eng_win)
        self.aux_graphics_left_eng = GraphicsView(self.left_eng_win)
        self.vlayout_left_eng.addWidget(self.aux_graphics_left_eng)
        self.main_graphics_left_eng = GraphicsView(self.left_eng_win)
        self.vlayout_left_eng.addWidget(self.main_graphics_left_eng)
        self.left_eng_win.setLayout(self.vlayout_left_eng)
        self.stack_window.addWidget(self.left_eng_win)

        self.right_eng_win = QWidget(self.stack_window, flags=Qt.Widget)
        self.vlayout_right_eng = QVBoxLayout(self.right_eng_win)
        self.aux_graphics_right_eng = GraphicsView(self.right_eng_win)
        self.vlayout_right_eng.addWidget(self.aux_graphics_right_eng)
        self.main_graphics_right_eng = GraphicsView(self.right_eng_win)
        self.vlayout_right_eng.addWidget(self.main_graphics_right_eng)
        self.right_eng_win.setLayout(self.vlayout_right_eng)
        self.stack_window.addWidget(self.right_eng_win)

        self.stack_window.setCurrentIndex(0)
        self.verticalLayout.addWidget(self.stack_window)
        self.setCentralWidget(self.centralwidget)

        # 汉化
        self.translate_lang()

        # ============以下初始化数据============
        #
        self.plot_item_row = 2
        self.plot_item_col = 3
        self.aux_plot_item_row = 8

        # 需读取数据的参数
        self.para_list = PARA_LIST
        self.time_range_paras_left = TIME_RANGE_PARA_LEFT
        self.time_paras_left = TIME_PARA_LEFT
        self.time_range_paras_right = TIME_RANGE_PARA_RIGHT
        self.time_paras_right = TIME_PARA_RIGHT
        # 存储参数数据
        self.data_list = dict(PT_15R1_L=list(), PT_15R2_L=list(), PT_15R3_L=list(), PT_15R4_L=list(),
                              PT_15R5_L=list(), PT_15R6_L=list(), PT_15R7_L=list(), PT_15R8_L=list(),
                              PF_UPST_L=list(), PF_DNST_L=list(), TF_UPST_L=list(),
                              TF_DNST_L=list(), QF_UPS_L=list(), QF_DNS_L=list(),
                              PT_15R1_R=list(), PT_15R2_R=list(), PT_15R3_R=list(), PT_15R4_R=list(),
                              PT_15R5_R=list(), PT_15R6_R=list(), PT_15R7_R=list(), PT_15R8_R=list(),
                              PF_UPST_R=list(), PF_DNST_R=list(), TF_UPST_R=list(),
                              TF_DNST_R=list(), QF_UPS_R=list(), QF_DNS_R=list()
                              )
        # 对应参数的坐标轴
        self.plot_item_list = dict(PT_15R1_L=None, PT_15R2_L=None, PT_15R3_L=None, PT_15R4_L=None,
                                   PT_15R5_L=None, PT_15R6_L=None, PT_15R7_L=None, PT_15R8_L=None,
                                   PF_UPST_L=None, PF_DNST_L=None, TF_UPST_L=None,
                                   TF_DNST_L=None, QF_UPS_L=None, QF_DNS_L=None,
                                   PT_15R1_R=None, PT_15R2_R=None, PT_15R3_R=None, PT_15R4_R=None,
                                   PT_15R5_R=None, PT_15R6_R=None, PT_15R7_R=None, PT_15R8_R=None,
                                   PF_UPST_R=None, PF_DNST_R=None, TF_UPST_R=None,
                                   TF_DNST_R=None, QF_UPS_R=None, QF_DNS_R=None
                                   )
        # 对应参数的曲线
        self.curve_dict = dict(PT_15R1_L=None, PT_15R2_L=None, PT_15R3_L=None, PT_15R4_L=None,
                               PT_15R5_L=None, PT_15R6_L=None, PT_15R7_L=None, PT_15R8_L=None,
                               PF_UPST_L=None, PF_DNST_L=None, TF_UPST_L=None,
                               TF_DNST_L=None, QF_UPS_L=None, QF_DNS_L=None,
                               PT_15R1_R=None, PT_15R2_R=None, PT_15R3_R=None, PT_15R4_R=None,
                               PT_15R5_R=None, PT_15R6_R=None, PT_15R7_R=None, PT_15R8_R=None,
                               PF_UPST_R=None, PF_DNST_R=None, TF_UPST_R=None,
                               TF_DNST_R=None, QF_UPS_R=None, QF_DNS_R=None
                               )

        # 数据的采样频率
        self.sample_fre = 32
        # 显示的时间范围，单位秒
        self.show_time_range = 30
        # UDP端口号
        self.udp_port = 18334
        # UDP连接
        self.udp_connect = DataConnection(self.udp_port)
        # 线程
        self.plot_thread = None
        self.stop_plot_thread = False
        # 缓冲数据
        self.buffer_data = list()

        # 测试数据
        self.test_data = None

        # ============以下初始化应用============
        #
        # 创建坐标布局
        aux_label = [lab for lab in self.time_paras_left]
        self.custom_graphics_view_layout(self.aux_graphics_left_eng, aux_label,
                                         self.main_graphics_left_eng, self.time_range_paras_left)
        aux_label = [lab for lab in self.time_paras_right]
        self.custom_graphics_view_layout(self.aux_graphics_right_eng, aux_label,
                                         self.main_graphics_right_eng, self.time_range_paras_right)

        # 创建曲线对象
        for pi in self.time_paras_left:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        for pi in self.time_paras_right:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        for pi in self.time_range_paras_left:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen='g')
        for pi in self.time_range_paras_right:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen='g')
        self.idx = 0

        # 连接信号与槽
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_and_plot_data_in_time)
        self.action_read_data.triggered.connect(self.read_data)
        self.action_start.triggered.connect(self.start_plot)
        self.action_show_right_engine.triggered.connect(self.release_engine_view_btn)
        self.action_show_left_engine.triggered.connect(self.release_engine_view_btn)
        self.action_setting.triggered.connect(self.setting)
        self.action_connect_udp.triggered.connect(self.connect_udp)
        self.action_disconnect_udp.triggered.connect(self.disconnect_udp)

    def closeEvent(self, event):
        message = QMessageBox.warning(self, 'Exit', 'Are you sure you want to exit IFTD MONITOR?',
                                      QMessageBox.Yes | QMessageBox.No)
        if message == QMessageBox.Yes:
            self.disconnect_udp()
            event.accept()
        else:
            event.ignore()

    def connect_udp(self):
        self.disconnect_udp()
        try:
            self.udp_connect.connection()
            if self.plot_thread is None:
                self.stop_plot_thread = False
                self.plot_thread = threading.Thread(target=self.get_and_plot_data_in_time)
                self.plot_thread.start()
        except ConnectionRefusedError:
            QMessageBox.information(self, 'Connect Tip', 'Connection is refused!')
        finally:
            pass

    @staticmethod
    def custom_axis_style(plot_axes, **kwargs):
        # 设置X轴不可缩放，Y轴可以缩放
        pw_vb = plot_axes.getViewBox()
        pw_vb.setMouseEnabled(x=kwargs['x_mouse_enable'], y=kwargs['y_mouse_enable'])
        # 隐藏自动缩放按钮
        plot_axes.hideButtons()
        # 显示网格
        plot_axes.showGrid(x=True, y=True, alpha=0.6)
        # 显示脊线
        plot_axes.showAxis('right')
        plot_axes.showAxis('top')
        # 设置坐标轴样式
        font = QFont()
        font.setFamily('Times New Roman')
        l_axis = plot_axes.getAxis('left')
        l_axis.setPen('w')
        l_axis.setTickFont(font)
        b_axis = plot_axes.getAxis('bottom')
        b_axis.setPen('w')
        b_axis.setTickFont(font)
        r_axis = plot_axes.getAxis('right')
        r_axis.setPen('w')
        r_axis.setStyle(showValues=False)
        t_axis = plot_axes.getAxis('top')
        t_axis.setPen('w')
        t_axis.setStyle(showValues=False)
        # 设置初始范围
        if kwargs['x_range'] is not None:
            plot_axes.setRange(xRange=kwargs['x_range'], padding=0)
        if kwargs['y_range'] is not None:
            plot_axes.setRange(yRange=kwargs['y_range'], padding=0)

        # 设置标注样式
        label_style = {'font-size': '10pt', 'font-family': 'Times New Roman',
                       'color': '#0F0', 'font-weight': 'bold'}
        plot_axes.setLabel(kwargs['label_pos'], text=kwargs['label'], **label_style)
        # plot_axes.setLabel('bottom', text='Time', units='s', **label_style)

    def custom_graphics_view_layout(self, aux_graph, aux_label, main_graph, main_label):

        aux_graph.setBackground('303030')
        # 创建布局器
        aux_gra_layout = pg.GraphicsLayout()
        for i in range(self.aux_plot_item_row):
            y_label = aux_label[i]
            # 添加坐标
            pw = aux_gra_layout.addPlot(row=0, col=i)
            self.custom_axis_style(pw, label=y_label, label_pos='top',
                                   x_mouse_enable=True, y_mouse_enable=False,
                                   x_range=None, y_range=[0, 9])
            if y_label in self.plot_item_list:
                self.plot_item_list[y_label] = pw
        aux_graph.setCentralWidget(aux_gra_layout)

        main_graph.setBackground('303030')
        # 创建布局器
        gra_layout = pg.GraphicsLayout()
        # 依次在布局器中添加2*3个坐标，并设置坐标属性
        for i in range(self.plot_item_row):
            for j in range(self.plot_item_col):
                y_label = main_label[i * self.plot_item_col + j]
                # 添加坐标
                pw = gra_layout.addPlot(row=i, col=j)
                self.custom_axis_style(pw, label=y_label, label_pos='left',
                                       x_mouse_enable=False, y_mouse_enable=True,
                                       x_range=[0, self.show_time_range], y_range=None)
                if y_label in self.plot_item_list:
                    self.plot_item_list[y_label] = pw
        main_graph.setCentralWidget(gra_layout)

    def disconnect_udp(self):
        self.stop_plot_thread = True
        self.plot_thread = None
        self.buffer_data = list()
        self.udp_connect.close_connect()

    def get_and_plot_data_in_time(self):
        tmp = self.test_data.iloc[self.idx]
        start_t = time.time()
        self.plot_data(tmp)
        end_t = time.time()
        print('Waste Time: ', end_t - start_t)
        self.idx += 1
        # while not self.stop_plot_thread:
        #     para_data = self.udp_connect.recv_data()
        #     start_t = time.time()
        #     if para_data:
        #         self.buffer_data.append(para_data)
        #         print('buffer length : ', len(self.buffer_data))
        #     if len(self.buffer_data) > 1:
        #         data = dict()
        #         str_dict_data = self.buffer_data.pop(0)
        #         for key in self.para_list:
        #             if key in str_dict_data:
        #                 try:
        #                     data[key] = float(str_dict_data[key])
        #                 except ValueError:
        #                     data[key] = str_dict_data[key]
        #             else:
        #                 data[key] = 0
        #         end_t = time.time()
        #         print('Process Data Waste Time: ', end_t - start_t)
        #         self.plot_data(data)
        #     end_t = time.time()
        #     print('Waste Time: ', end_t - start_t)

    def plot_data(self, data_in_time):
        data_length = 0
        # 读取时间范围的数据
        for para_name in self.time_range_paras_left:
            # tmp = np.sin(np.pi / 50 * self.idx + 2 * np.pi * i / self.plot_item_col / self.plot_item_row)
            if len(self.data_list[para_name]) < self.show_time_range * self.sample_fre:
                self.data_list[para_name].append(data_in_time[para_name])
            else:
                self.data_list[para_name][:-1] = self.data_list[para_name][1:]
                self.data_list[para_name][-1] = data_in_time[para_name]
            data_length = len(self.data_list[para_name])

        # 读取时刻的数据
        for plot_name in self.time_paras_left:
            plot_data = list()
            for pn in self.time_paras_left[plot_name]:
                plot_data.append(data_in_time[pn])
            self.data_list[plot_name] = plot_data

        # 显示时间
        self.status_bar.showMessage(data_in_time['Time'])

        # 时间范围的曲线显示
        x_data = np.linspace(0, data_length / self.sample_fre, data_length)
        for curve_name in self.time_range_paras_left:
            self.curve_dict[curve_name].setData(x_data, self.data_list[curve_name])

        # 时刻的曲线显示
        y_data = np.linspace(1, 8, 8)
        for curve_name in self.time_paras_left:
            self.curve_dict[curve_name].setData(self.data_list[curve_name], y_data)

    def read_data(self):
        try:
            self.test_data = pd.read_csv('E:\\FTPD-C919-10102-PD-190617-G-02-00CFM-FTI01L-32.txt', sep=r'\s+',
                                         usecols=self.para_list, index_col=False, engine='c', skip_blank_lines=True)
        except ValueError:
            print('Error info: read_data: ValueError.')
        print('done')

    def release_engine_view_btn(self):
        # 接收发出信号的那个对象
        sender = QObject.sender(self)
        if sender == self.action_show_left_engine:
            if self.action_show_right_engine.isChecked():
                self.action_show_right_engine.setChecked(False)
            self.action_show_left_engine.setChecked(True)
            self.stack_window.setCurrentIndex(0)
        if sender == self.action_show_right_engine:
            if self.action_show_left_engine.isChecked():
                self.action_show_left_engine.setChecked(False)
            self.action_show_right_engine.setChecked(True)
            self.stack_window.setCurrentIndex(1)

    def setting(self):
        dialog = SettingDialog(parent=None, time_range=self.show_time_range,
                               fre=self.sample_fre, port=self.udp_port)
        siganl_return = dialog.exec_()
        if siganl_return == QDialog.Accepted:
            if self.show_time_range != dialog.spin_box_time_range.value():
                self.show_time_range = dialog.spin_box_time_range.value()
                for pi in self.time_range_paras_left:
                    self.plot_item_list[pi].setRange(xRange=[0, self.show_time_range], padding=0)
                for pi in self.time_range_paras_right:
                    self.plot_item_list[pi].setRange(xRange=[0, self.show_time_range], padding=0)
            if self.sample_fre != dialog.spin_box_fre.value():
                self.sample_fre = dialog.spin_box_fre.value()
            if self.udp_port != dialog.spin_box_port.value():
                self.udp_port = dialog.spin_box_port.value()
                self.disconnect_udp()
                self.udp_connect = DataConnection(self.udp_port)

    def start_plot(self):
        self.timer.start(5)

    def translate_lang(self):
        self.setWindowTitle('IFTD MONITOR')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = IFTDMonitor()
    mw.show()
    # timer = pg.QtCore.QTimer()
    # timer.timeout.connect(mw.plot_data)
    # timer.start(5)
    sys.exit(app.exec_())
