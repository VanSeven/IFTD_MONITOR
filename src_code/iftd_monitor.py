# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Wang Xueliang
# Date: 2019/5/13

import sys
import threading
# import time

import pyqtgraph as pg
import numpy as np
import pandas as pd
# import array

from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QAction, QDialog, QMessageBox)

from para_info import (PARA_LIST, TIME_PARA_LEFT, TIME_PARA_RIGHT, TIME_RANGE_PARA_LEFT,
                       TIME_RANGE_PARA_RIGHT)
from setting_dialog import SettingDialog
from DataConnection import DataConnection
from iftd_monitor_view import IFTDMonitorView
import forzen_dir


class IFTDMonitor(IFTDMonitorView):
    def __init__(self, parent=None):
        super().__init__(parent)

        soft_dir = forzen_dir.app_path()
        self.setWindowIcon(QIcon(soft_dir + r'\icons\window.ico'))
        # 创建动作
        # self.action_start = QAction(self)
        # self.action_start.setText('Start')
        # self.action_start.setIcon(QIcon('window.ico'))
        # self.action_start.setIconText('Start')
        # self.action_read_data = QAction(self)
        # self.action_read_data.setText('Read Data')
        self.action_show_left_engine = QAction(self)
        self.action_show_left_engine.setText('Left Engine')
        self.action_show_left_engine.setCheckable(True)
        self.action_show_left_engine.setChecked(True)
        self.action_show_left_engine.setIcon(QIcon(soft_dir + r'\icons\left_engine.ico'))
        self.action_show_right_engine = QAction(self)
        self.action_show_right_engine.setText('Right Engine')
        self.action_show_right_engine.setCheckable(True)
        self.action_show_right_engine.setIcon(QIcon(soft_dir + r'\icons\right_engine.ico'))
        self.action_setting = QAction(self)
        self.action_setting.setText('Setting')
        self.action_setting.setIcon(QIcon(soft_dir + r'\icons\setting.ico'))
        self.action_connect_udp = QAction(self)
        self.action_connect_udp.setText('Connect')
        self.action_connect_udp.setIcon(QIcon(soft_dir + r'\icons\connect.ico'))
        self.action_disconnect_udp = QAction(self)
        self.action_disconnect_udp.setText('Disconnect')
        self.action_disconnect_udp.setIcon(QIcon(soft_dir + r'\icons\disconnect.ico'))
        self.toolBar.addActions([self.action_show_left_engine,
                                 self.action_show_right_engine,
                                 self.action_connect_udp,
                                 self.action_disconnect_udp,
                                 # self.action_start,
                                 # self.action_read_data,
                                 self.action_setting])

        # ============以下初始化数据============
        #
        self.aux_plot_item_row = 8
        self.main_plot_item_row = 5

        # 需读取数据的参数
        self.para_list = PARA_LIST
        self.time_range_paras_left = TIME_RANGE_PARA_LEFT
        self.time_paras_left = TIME_PARA_LEFT
        self.time_range_paras_right = TIME_RANGE_PARA_RIGHT
        self.time_paras_right = TIME_PARA_RIGHT
        # 存储参数数据
        self.data_list = dict(PT_15R1_L=list(), PT_15R2_L=list(), PT_15R3_L=list(), PT_15R4_L=list(),
                              PT_15R5_L=list(), PT_15R6_L=list(), PT_15R7_L=list(), PT_15R8_L=list(),
                              PT_50R1_L=list(), PT_50R2_L=list(), PT_50R3_L=list(), PT_50R4_L=list(), PT_50R5_L=list(),
                              PF_UPST_L=list(), PF_DNST_L=list(), TF_UPST_L=list(),
                              TF_DNST_L=list(), QF_UPS_L=list(), QF_DNS_L=list(),
                              PT_15R1_R=list(), PT_15R2_R=list(), PT_15R3_R=list(), PT_15R4_R=list(),
                              PT_15R5_R=list(), PT_15R6_R=list(), PT_15R7_R=list(), PT_15R8_R=list(),
                              PT_50R1_R=list(), PT_50R2_R=list(), PT_50R3_R=list(), PT_50R4_R=list(), PT_50R5_R=list(),
                              PF_UPST_R=list(), PF_DNST_R=list(), TF_UPST_R=list(),
                              TF_DNST_R=list(), QF_UPS_R=list(), QF_DNS_R=list()
                              )
        # 对应参数的坐标轴
        self.plot_item_list = dict(PT_15R1_L=None, PT_15R2_L=None, PT_15R3_L=None, PT_15R4_L=None,
                                   PT_15R5_L=None, PT_15R6_L=None, PT_15R7_L=None, PT_15R8_L=None,
                                   PT_50R1_L=None, PT_50R2_L=None, PT_50R3_L=None, PT_50R4_L=None, PT_50R5_L=None,
                                   PF_UPST_L=None, PF_DNST_L=None, TF_UPST_L=None,
                                   TF_DNST_L=None, QF_UPS_L=None, QF_DNS_L=None,
                                   PT_15R1_R=None, PT_15R2_R=None, PT_15R3_R=None, PT_15R4_R=None,
                                   PT_15R5_R=None, PT_15R6_R=None, PT_15R7_R=None, PT_15R8_R=None,
                                   PT_50R1_R=None, PT_50R2_R=None, PT_50R3_R=None, PT_50R4_R=None, PT_50R5_R=None,
                                   PF_UPST_R=None, PF_DNST_R=None, TF_UPST_R=None,
                                   TF_DNST_R=None, QF_UPS_R=None, QF_DNS_R=None
                                   )
        # 对应参数的曲线
        self.curve_dict = dict(PT_15R1_L=None, PT_15R2_L=None, PT_15R3_L=None, PT_15R4_L=None,
                               PT_15R5_L=None, PT_15R6_L=None, PT_15R7_L=None, PT_15R8_L=None,
                               PT_50R1_L=None, PT_50R2_L=None, PT_50R3_L=None, PT_50R4_L=None, PT_50R5_L=None,
                               PF_UPST_L=None, PF_DNST_L=None, TF_UPST_L=None,
                               TF_DNST_L=None, QF_UPS_L=None, QF_DNS_L=None,
                               PT_15R1_R=None, PT_15R2_R=None, PT_15R3_R=None, PT_15R4_R=None,
                               PT_15R5_R=None, PT_15R6_R=None, PT_15R7_R=None, PT_15R8_R=None,
                               PT_50R1_R=None, PT_50R2_R=None, PT_50R3_R=None, PT_50R4_R=None, PT_50R5_R=None,
                               PF_UPST_R=None, PF_DNST_R=None, TF_UPST_R=None,
                               TF_DNST_R=None, QF_UPS_R=None, QF_DNS_R=None
                               )

        # 数据的采样频率
        self.sample_fre = 32
        # 显示的时间范围，单位秒
        self.show_time_range = 30
        # UDP端口号
        self.udp_port = 9291
        # 数据的解码方式
        self.udp_decode_method = 'gbk'
        # UDP连接
        self.udp_connect = DataConnection(self.udp_port, self.udp_decode_method)
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
        aux_label_up = [lab for lab in self.time_paras_left]
        aux_label_bottom = [lab for lab in self.time_range_paras_left]
        self.custom_graphics_view_layout(self.aux_graphics_left_eng, aux_label_up,
                                         self.main_graphics_left_eng, aux_label_bottom)
        aux_label_up = [lab for lab in self.time_paras_right]
        aux_label_bottom = [lab for lab in self.time_range_paras_right]
        self.custom_graphics_view_layout(self.aux_graphics_right_eng, aux_label_up,
                                         self.main_graphics_right_eng, aux_label_bottom)

        # 创建曲线对象
        for pi in self.time_paras_left:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        for pi in self.time_paras_right:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        for pi in self.time_range_paras_left:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        for pi in self.time_range_paras_right:
            self.curve_dict[pi] = self.plot_item_list[pi].plot(pen=None, symbol='o')
        self.idx = 0

        # 连接信号与槽
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_data_show)
        # self.action_read_data.triggered.connect(self.read_data)
        # self.action_start.triggered.connect(self.start_plot)
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
        except (OSError, ConnectionRefusedError):
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
        for i in range(self.main_plot_item_row):
            y_label = main_label[i]
            # 添加坐标
            pw = gra_layout.addPlot(row=0, col=i)
            self.custom_axis_style(pw, label=y_label, label_pos='top',
                                   x_mouse_enable=True, y_mouse_enable=False,
                                   x_range=None, y_range=[0, 9])
            if y_label in self.plot_item_list:
                self.plot_item_list[y_label] = pw
        main_graph.setCentralWidget(gra_layout)

    def disconnect_udp(self):
        self.stop_plot_thread = True
        self.plot_thread = None
        self.buffer_data = list()
        self.udp_connect.close_connect()

    def get_and_plot_data_in_time(self):
        while not self.stop_plot_thread:
            para_data = self.udp_connect.recv_data()
            # start_t = time.time()
            if para_data:
                self.buffer_data.append(para_data)
                # print('buffer length : ', len(self.buffer_data))
            if len(self.buffer_data) > 1:
                data = dict()
                str_dict_data = self.buffer_data.pop(0)
                # print('str_dict_data', str_dict_data)
                for key in self.para_list:
                    if key in str_dict_data:
                        try:
                            data[key] = float(str_dict_data[key])
                        except ValueError:
                            data[key] = str_dict_data[key]
                    else:
                        data[key] = 0
                # end_t = time.time()
                # print('Process Data Waste Time: ', end_t - start_t)
                # print('data', data)
                self.update_data_view(data)
            # end_t = time.time()
            # print('Waste Time: ', end_t - start_t)

    def read_data(self):
        try:
            self.test_data = pd.read_csv('E:\\FPSoftTestData\\FTPD-C919-10102-PD-190617-G-02-00CFM-FTI01L-32.txt', sep=r'\s+',
                                         usecols=self.para_list, index_col=False, engine='c', skip_blank_lines=True)
        except ValueError:
            print('Error info: read_data: ValueError.')
        print('done')

    def read_data_show(self):
        tmp = self.test_data.iloc[self.idx]
        self.update_data_view(tmp)
        self.idx += 1

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
            # print(dialog.cb_decode.currentText())
            if self.show_time_range != dialog.spin_box_time_range.value():
                self.show_time_range = dialog.spin_box_time_range.value()
                for pi in self.time_range_paras_left:
                    self.plot_item_list[pi].setRange(xRange=[0, self.show_time_range], padding=0)
                for pi in self.time_range_paras_right:
                    self.plot_item_list[pi].setRange(xRange=[0, self.show_time_range], padding=0)
            if self.sample_fre != dialog.spin_box_fre.value():
                self.sample_fre = dialog.spin_box_fre.value()
            if self.udp_port != dialog.spin_box_port.value() or \
                    self.udp_decode_method != dialog.cb_decode.currentText():
                self.udp_port = dialog.spin_box_port.value()
                self.udp_decode_method = dialog.cb_decode.currentText()
                self.disconnect_udp()
                self.udp_connect = DataConnection(self.udp_port, self.udp_decode_method)

    def start_plot(self):
        self.timer.start(30)

    # 更新曲线显示
    def update_curve(self):

        # 时刻的曲线显示
        y_data = np.linspace(1, 8, 8)
        for curve_name in self.time_paras_left:
            self.curve_dict[curve_name].setData(self.data_list[curve_name], y_data)

        for curve_name in self.time_paras_right:
            self.curve_dict[curve_name].setData(self.data_list[curve_name], y_data)

        for curve_name in self.time_range_paras_left:
            self.curve_dict[curve_name].setData(self.data_list[curve_name], y_data)

        for curve_name in self.time_range_paras_right:
            self.curve_dict[curve_name].setData(self.data_list[curve_name], y_data)

    # 更新数据
    def update_data_list(self, data_in_time):

        # 读取时刻的数据
        for plot_name in self.time_paras_left:
            plot_data = list()
            for pn in self.time_paras_left[plot_name]:
                plot_data.append(data_in_time[pn])
            self.data_list[plot_name] = plot_data

        for plot_name in self.time_paras_right:
            plot_data = list()
            for pn in self.time_paras_right[plot_name]:
                plot_data.append(data_in_time[pn])
            self.data_list[plot_name] = plot_data

        for plot_name in self.time_range_paras_left:
            plot_data = list()
            for pn in self.time_range_paras_left[plot_name]:
                plot_data.append(data_in_time[pn])
            self.data_list[plot_name] = plot_data

        for plot_name in self.time_range_paras_right:
            plot_data = list()
            for pn in self.time_range_paras_right[plot_name]:
                plot_data.append(data_in_time[pn])
            self.data_list[plot_name] = plot_data

    # 更新数据的显示
    def update_data_view(self, data_in_time):

        self.update_data_list(data_in_time)
        self.update_num(data_in_time)
        self.update_curve()

    # 更新数值显示
    def update_num(self, data_in_time):
        # 显示时间
        self.status_bar.showMessage(str(data_in_time['Time']))
        self.qf_upst_l_l.setText(str(data_in_time['QF_UPS_L']))
        self.qf_upst_l_r.setText(str(data_in_time['QF_UPS_L']))
        self.qf_upst_r_l.setText(str(data_in_time['QF_UPS_R']))
        self.qf_upst_r_r.setText(str(data_in_time['QF_UPS_R']))
        self.qf_dnst_l_l.setText(str(data_in_time['QF_DNS_L']))
        self.qf_dnst_l_r.setText(str(data_in_time['QF_DNS_L']))
        self.qf_dnst_r_l.setText(str(data_in_time['QF_DNS_R']))
        self.qf_dnst_r_r.setText(str(data_in_time['QF_DNS_R']))

        self.pf_upst_l_l.setText(str(data_in_time['PF_UPST_L']))
        self.pf_upst_l_r.setText(str(data_in_time['PF_UPST_L']))
        self.pf_upst_r_l.setText(str(data_in_time['PF_UPST_R']))
        self.pf_upst_r_r.setText(str(data_in_time['PF_UPST_R']))
        self.pf_dnst_l_l.setText(str(data_in_time['PF_DNST_L']))
        self.pf_dnst_l_r.setText(str(data_in_time['PF_DNST_L']))
        self.pf_dnst_r_l.setText(str(data_in_time['PF_DNST_R']))
        self.pf_dnst_r_r.setText(str(data_in_time['PF_DNST_R']))

        self.tf_upst_l_l.setText(str(data_in_time['TF_UPST_L']))
        self.tf_upst_l_r.setText(str(data_in_time['TF_UPST_L']))
        self.tf_upst_r_l.setText(str(data_in_time['TF_UPST_R']))
        self.tf_upst_r_r.setText(str(data_in_time['TF_UPST_R']))
        self.tf_dnst_l_l.setText(str(data_in_time['TF_DNST_L']))
        self.tf_dnst_l_r.setText(str(data_in_time['TF_DNST_L']))
        self.tf_dnst_r_l.setText(str(data_in_time['TF_DNST_R']))
        self.tf_dnst_r_r.setText(str(data_in_time['TF_DNST_R']))

        self.pt_25_a_l.setText(str(data_in_time['PT_25R1A_L']))
        self.pt_25_a_r.setText(str(data_in_time['PT_25R1A_R']))
        self.pt_25_b_l.setText(str(data_in_time['PT_25R1B_L']))
        self.pt_25_b_r.setText(str(data_in_time['PT_25R1B_R']))
        self.pt_25_c_l.setText(str(data_in_time['PT_25R1C_L']))
        self.pt_25_c_r.setText(str(data_in_time['PT_25R1C_R']))
        self.pt_25_d_l.setText(str(data_in_time['PT_25R1D_L']))
        self.pt_25_d_r.setText(str(data_in_time['PT_25R1D_R']))
        self.pt_25_e_l.setText(str(data_in_time['PT_25R1E_L']))
        self.pt_25_e_r.setText(str(data_in_time['PT_25R1E_R']))
        self.pt_25_f_l.setText(str(data_in_time['PT_25R1F_L']))
        self.pt_25_f_r.setText(str(data_in_time['PT_25R1F_R']))

        self.pt_31_a_l.setText(str(data_in_time['PT_31R1A_L']))
        self.pt_31_a_r.setText(str(data_in_time['PT_31R1A_R']))
        self.pt_31_b_l.setText(str(data_in_time['PT_31R1B_L']))
        self.pt_31_b_r.setText(str(data_in_time['PT_31R1B_R']))
        self.pt_31_c_l.setText(str(data_in_time['PT_31R1C_L']))
        self.pt_31_c_r.setText(str(data_in_time['PT_31R1C_R']))
        self.pt_31_d_l.setText(str(data_in_time['PT_31R1D_L']))
        self.pt_31_d_r.setText(str(data_in_time['PT_31R1D_R']))
        self.pt_31_e_l.setText(str(data_in_time['PT_31R1E_L']))
        self.pt_31_e_r.setText(str(data_in_time['PT_31R1E_R']))

        self.tt_25_a_l.setText(str(data_in_time['TT_25R1A_L']))
        self.tt_25_a_r.setText(str(data_in_time['TT_25R1A_R']))
        self.tt_25_b_l.setText(str(data_in_time['TT_25R1B_L']))
        self.tt_25_b_r.setText(str(data_in_time['TT_25R1B_R']))
        self.tt_25_c_l.setText(str(data_in_time['TT_25R1C_L']))
        self.tt_25_c_r.setText(str(data_in_time['TT_25R1C_R']))
        self.tt_25_d_l.setText(str(data_in_time['TT_25R1D_L']))
        self.tt_25_d_r.setText(str(data_in_time['TT_25R1D_R']))
        self.tt_25_e_l.setText(str(data_in_time['TT_25R1E_L']))
        self.tt_25_e_r.setText(str(data_in_time['TT_25R1E_R']))
        self.tt_25_f_l.setText(str(data_in_time['TT_25R1F_L']))
        self.tt_25_f_r.setText(str(data_in_time['TT_25R1F_R']))

        self.tt_31_a_l.setText(str(data_in_time['TT_31R1A_L']))
        self.tt_31_a_r.setText(str(data_in_time['TT_31R1A_R']))
        self.tt_31_b_l.setText(str(data_in_time['TT_31R1B_L']))
        self.tt_31_b_r.setText(str(data_in_time['TT_31R1B_R']))
        self.tt_31_c_l.setText(str(data_in_time['TT_31R1C_L']))
        self.tt_31_c_r.setText(str(data_in_time['TT_31R1C_R']))
        self.tt_31_d_l.setText(str(data_in_time['TT_31R1D_L']))
        self.tt_31_d_r.setText(str(data_in_time['TT_31R1D_R']))
        self.tt_31_e_l.setText(str(data_in_time['TT_31R1E_L']))
        self.tt_31_e_r.setText(str(data_in_time['TT_31R1E_R']))

        self.pt_79_a_l.setText(str(data_in_time['PT_79VNP1_L']))
        self.pt_79_a_r.setText(str(data_in_time['PT_79VNP1_R']))
        self.pt_79_b_l.setText(str(data_in_time['PT_79VNP2_L']))
        self.pt_79_b_r.setText(str(data_in_time['PT_79VNP2_R']))
        self.pt_79_c_l.setText(str(data_in_time['PT_79VNP3_L']))
        self.pt_79_c_r.setText(str(data_in_time['PT_79VNP3_R']))
        self.pt_79_d_l.setText(str(data_in_time['PT_79VNP4_L']))
        self.pt_79_d_r.setText(str(data_in_time['PT_79VNP4_R']))

        self.tt_79_a_l.setText(str(data_in_time['TT_79VNP1_L']))
        self.tt_79_a_r.setText(str(data_in_time['TT_79VNP1_R']))
        self.tt_79_b_l.setText(str(data_in_time['TT_79VNP2_L']))
        self.tt_79_b_r.setText(str(data_in_time['TT_79VNP2_R']))
        self.tt_79_c_l.setText(str(data_in_time['TT_79VNP3_L']))
        self.tt_79_c_r.setText(str(data_in_time['TT_79VNP3_R']))
        self.tt_79_d_l.setText(str(data_in_time['TT_79VNP4_L']))
        self.tt_79_d_r.setText(str(data_in_time['TT_79VNP4_R']))

        self.ps_79_a_l.setText(str(data_in_time['PS_79VNP1_L']))
        self.ps_79_a_r.setText(str(data_in_time['PS_79VNP1_R']))
        self.ps_79_b_l.setText(str(data_in_time['PS_79VNP2_L']))
        self.ps_79_b_r.setText(str(data_in_time['PS_79VNP2_R']))
        self.ps_79_c_l.setText(str(data_in_time['PS_79VNP3_L']))
        self.ps_79_c_r.setText(str(data_in_time['PS_79VNP3_R']))
        self.ps_79_d_l.setText(str(data_in_time['PS_79VNP4_L']))
        self.ps_79_d_r.setText(str(data_in_time['PS_79VNP4_R']))

        self.tat_l.setText(str(data_in_time['FCM1_Voted_Total_Air_Temperature']))
        self.tat_r.setText(str(data_in_time['FCM1_Voted_Total_Air_Temperature']))
        self.tt1_l.setText(str(data_in_time['TT_1']))
        self.tt1_r.setText(str(data_in_time['TT_1']))
        self.tt2_l.setText(str(data_in_time['TT_2']))
        self.tt2_r.setText(str(data_in_time['TT_2']))
        self.tt3_l.setText(str(data_in_time['TT_3']))
        self.tt3_r.setText(str(data_in_time['TT_3']))
        self.tt4_l.setText(str(data_in_time['TT_4']))
        self.tt4_r.setText(str(data_in_time['TT_4']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = IFTDMonitor()
    mw.show()
    # timer = pg.QtCore.QTimer()
    # timer.timeout.connect(mw.plot_data)
    # timer.start(5)
    sys.exit(app.exec_())
