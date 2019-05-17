# -*- coding: utf-8 -*-

# Name: braker_monitor
# Description: 刹车系统实时监控软件
# Author: 试飞工程软件开发团队
# Date: 2019/5/16

import sys
import pandas as pd
import array

from PyQt5.QtCore import QCoreApplication, QTimer, QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPalette
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QSpacerItem,
                             QHBoxLayout, QSizePolicy, QLabel, QApplication,
                             QFrame, QPushButton)
from PyQt5.Qt import QSound


class BrakeMonitor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(450, 270)
        self.setWindowIcon(QIcon('window.ico'))
        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.hlayout_time = QHBoxLayout()
        self.label_time = QLabel(self.centralwidget)
        self.label_time.setMinimumSize(QSize(300, 30))
        self.label_time.setMaximumSize(QSize(300, 30))
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_time.setFont(font)
        self.hlayout_time.addWidget(self.label_time)
        self.btn_check_fault = QPushButton(self.centralwidget)
        self.btn_check_fault.setMinimumSize(QSize(120, 50))
        self.btn_check_fault.setMaximumSize(QSize(120, 50))
        self.btn_check_fault.setFont(font)
        # 记住默认的样式
        self.btn_default_stylesheet = self.btn_check_fault.styleSheet()
        self.hlayout_time.addWidget(self.btn_check_fault)
        self.verticalLayout.addLayout(self.hlayout_time)
        self.horizontalLayout = QHBoxLayout()
        self.label_left_out = QLabel(self.centralwidget)
        self.label_left_out.setMinimumSize(QSize(75, 150))
        self.label_left_out.setMaximumSize(QSize(75, 150))
        self.label_left_out.setFrameShape(QFrame.Box)
        self.label_left_out.setText('左\n外\n机\n轮')
        self.label_left_out.setFont(font)
        self.label_left_out.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_left_out.setStyleSheet('QLabel {background-color: white}')
        self.horizontalLayout.addWidget(self.label_left_out)
        self.label_left_in = QLabel(self.centralwidget)
        self.label_left_in.setMinimumSize(QSize(75, 150))
        self.label_left_in.setMaximumSize(QSize(75, 150))
        self.label_left_in.setFrameShape(QFrame.Box)
        self.label_left_in.setText('左\n内\n机\n轮')
        self.label_left_in.setFont(font)
        self.label_left_in.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_left_in.setStyleSheet('QLabel {background-color: white}')
        self.horizontalLayout.addWidget(self.label_left_in)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_right_in = QLabel(self.centralwidget)
        self.label_right_in.setMinimumSize(QSize(75, 150))
        self.label_right_in.setMaximumSize(QSize(75, 150))
        self.label_right_in.setFrameShape(QFrame.Box)
        self.label_right_in.setText('右\n内\n机\n轮')
        self.label_right_in.setFont(font)
        self.label_right_in.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_right_in.setStyleSheet('QLabel {background-color: white}')
        self.horizontalLayout.addWidget(self.label_right_in)
        self.label_right_out = QLabel(self.centralwidget)
        self.label_right_out.setMinimumSize(QSize(75, 150))
        self.label_right_out.setMaximumSize(QSize(75, 150))
        self.label_right_out.setFrameShape(QFrame.Box)
        self.label_right_out.setText('右\n外\n机\n轮')
        self.label_right_out.setFont(font)
        self.label_right_out.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_right_out.setStyleSheet('QLabel {background-color: white}')
        self.horizontalLayout.addWidget(self.label_right_out)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.hlayout_btn = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout_btn.addItem(spacerItem)
        self.btn_start = QPushButton(self.centralwidget)
        self.hlayout_btn.addWidget(self.btn_start)
        self.btn_read_data = QPushButton(self.centralwidget)
        self.hlayout_btn.addWidget(self.btn_read_data)
        self.verticalLayout.addLayout(self.hlayout_btn)
        self.setCentralWidget(self.centralwidget)

        # 汉化
        self.translate_lang()

        # 存储模拟播报数据
        self.test_data = None
        # 要处理参数的个数
        self.count_paras = 4
        # 数据点个数
        self.idx = 0
        # 记录数据
        self.data_list = []
        for i in range(self.count_paras):
            self.data_list.append(array.array('d'))
        # 告警音
        self.warning_sound = QSound('brake_warning.wav')
        # 告警阶段的数据
        self.warning_phase_data = {}
        # 告警次数
        self.count_warning = 0
        # 是否存在新的故障数据
        self.raise_new_warning = False

        # 计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_data)
        self.btn_start.clicked.connect(self.start_plot)
        self.btn_read_data.clicked.connect(self.read_data)
        self.btn_check_fault.clicked.connect(self.check_fault)

    # 查看告警清单
    def check_fault(self):
        # 停止告警音
        if not self.warning_sound.isFinished():
            self.ctrl_warning_sound(False)
        self.raise_new_warning = False
        self.btn_check_fault.setStyleSheet(self.btn_default_stylesheet)

    # 播放告警音
    def ctrl_warning_sound(self, status):
        # 如果为真则播放
        if status:
            # 循环播放
            if self.warning_sound.loops() != QSound.Infinite:
                self.warning_sound.setLoops(QSound.Infinite)
                self.warning_sound.play()
        else:
            self.warning_sound.stop()
            self.warning_sound.setLoops(0)

    # 显示监控画面，并进行数据处理，判断告警信息
    def plot_data(self):
        raise_warning = False
        # 根据用户需要制定相应的显示方式
        if isinstance(self.test_data, pd.DataFrame) and len(self.test_data) > self.idx + 1:
            warning_logic_data = self.test_data.iloc[self.idx, :]
            self.label_time.setText('时间 : ' + warning_logic_data['TIME'])
            if warning_logic_data.loc['RDIU6_BCMU_312_01'] < 3\
                    or warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 0:
                self.label_left_out.setStyleSheet('QLabel {background-color: green}')
                self.label_left_in.setStyleSheet('QLabel {background-color: green}')
                self.label_right_in.setStyleSheet('QLabel {background-color: green}')
                self.label_right_out.setStyleSheet('QLabel {background-color: green}')

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1\
                    and warning_logic_data.loc['BCMU_RDIU6_4_01'] >= 5:
                self.label_left_in.setStyleSheet('QLabel {background-color: green}')

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_4_01'] < 5:
                self.label_left_in.setStyleSheet('QLabel {background-color: red}')
                raise_warning = True

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_6_01'] >= 5:
                self.label_left_out.setStyleSheet('QLabel {background-color: green}')

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_6_01'] < 5:
                self.label_left_out.setStyleSheet('QLabel {background-color: red}')
                raise_warning = True

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_5_01'] >= 5:
                self.label_right_in.setStyleSheet('QLabel {background-color: green}')

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_5_01'] < 5:
                self.label_right_in.setStyleSheet('QLabel {background-color: red}')
                raise_warning = True

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_7_01'] >= 5:
                self.label_right_out.setStyleSheet('QLabel {background-color: green}')

            if warning_logic_data.loc['RDIU6_BCMU_312_01'] >= 3\
                    and warning_logic_data.loc['LGCU1_RDIU8_275_01_12'] == 1 \
                    and warning_logic_data.loc['BCMU_RDIU6_7_01'] < 5:
                self.label_right_out.setStyleSheet('QLabel {background-color: red}')
                raise_warning = True
        else:
            self.label_left_out.setStyleSheet('QLabel {background-color: white}')
            self.label_left_in.setStyleSheet('QLabel {background-color: white}')
            self.label_right_in.setStyleSheet('QLabel {background-color: white}')
            self.label_right_out.setStyleSheet('QLabel {background-color: white}')

        # 如果出现告警，播放告警音
        if raise_warning:
            self.ctrl_warning_sound(True)
            self.raise_fault()

        self.idx += 1

    # 处理出现的告警
    def raise_fault(self):
        if not self.raise_new_warning:
            self.btn_check_fault.setStyleSheet('QPushButton {background-color: cyan}')
            self.raise_new_warning = True

    # 读数据
    def read_data(self):
        # gear_paras = ['TIME', 'LGCU1_RDIU8_275_01_12']
        # brake_paras = ['RDIU6_BCMU_312_01','BCMU_RDIU6_4_01', 'BCMU_RDIU6_6_01',
        #                'BCMU_RDIU6_5_01', 'BCMU_RDIU6_7_01']
        # gear_paras_data = pd.read_csv('E:\\FTD\\FTPD-C919-10103-PD-181228-F-01-LGS-429001-16.txt', sep='\s+',
        #                               usecols=gear_paras, index_col=False, engine='c',
        #                               skip_blank_lines=True)
        # brake_paras_data = pd.read_csv('E:\\FTD\\FTPD-C919-10103-PD-181228-F-01-BRK-429001-32.txt', sep='\s+',
        #                                usecols=brake_paras, index_col=False, engine='c',
        #                                skip_blank_lines=True)
        # bp_cols = [i for i in range(len(brake_paras_data)) if i % 2 == 0]
        # brake_paras_data = brake_paras_data.drop(bp_cols)
        # brake_paras_data = brake_paras_data.reset_index(drop=True)
        # self.test_data = pd.concat([gear_paras_data, brake_paras_data], axis=1, join='inner')
        paras = ['TIME', 'BCMU_A429_Out_1_L4_Left_INBD_Wheelspeed_BCMU',
                 'BCMU_A429_Out_1_L5_Right_INBD_Wheelspeed_BCMU',
                 'BCMU_A429_Out_1_L6_Left_OUTBD_Wheelspeed_BCMU',
                 'BCMU_A429_Out_1_L7_Right_OUTBD_Wheelspeed_BCMU',
                 'RDIU6_BCMU_312_01']
        self.test_data = pd.read_csv('E:\\FTD\\FastPlot DataFile 0.txt', sep='\s+',
                                     usecols=paras, index_col=False, engine='c',
                                     skip_blank_lines=True)
        self.test_data.rename(columns={'BCMU_A429_Out_1_L4_Left_INBD_Wheelspeed_BCMU': 'BCMU_RDIU6_4_01',
                                       'BCMU_A429_Out_1_L5_Right_INBD_Wheelspeed_BCMU': 'BCMU_RDIU6_5_01',
                                       'BCMU_A429_Out_1_L6_Left_OUTBD_Wheelspeed_BCMU': 'BCMU_RDIU6_6_01',
                                       'BCMU_A429_Out_1_L7_Right_OUTBD_Wheelspeed_BCMU': 'BCMU_RDIU6_7_01'}, inplace=True)
        self.test_data['LGCU1_RDIU8_275_01_12'] = 1
        print(self.test_data)
        print('Read Done.')

    # 模拟时间
    def start_plot(self):
        self.timer.start(66)

    # 汉化
    def translate_lang(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate('BrakeMonitor', '刹车监控画面'))
        self.label_time.setText(_translate('BrakeMonitor', '时间 : 00:00:00:000'))
        self.btn_start.setText(_translate('BrakeMonitor', 'Start'))
        self.btn_read_data.setText(_translate('BrakeMonitor', 'Read Data'))
        self.btn_check_fault.setText(_translate('BrakeMonitor', '查看故障'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = BrakeMonitor()
    mw.show()
    sys.exit(app.exec_())