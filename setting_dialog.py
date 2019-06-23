# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Wang Xueliang
# Date: 2019/6/22

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QApplication,
                             QLabel, QSpinBox, QSizePolicy, QSpacerItem,
                             QPushButton)


class SettingDialog(QDialog):

    def __init__(self, parent=None, time_range=None, fre=None, port=None):
        super().__init__(parent)

        font = QFont()
        font.setFamily('微软雅黑')
        self.setFont(font)
        self.resize(260, 150)
        self.setWindowTitle('Setting')
        self.setWindowIcon(QIcon('window.ico'))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setSpacing(4)
        self.horizontalLayout = QHBoxLayout()
        self.label_time_range = QLabel(self)
        self.label_time_range.setMinimumSize(QSize(110, 25))
        self.label_time_range.setMaximumSize(QSize(110, 25))
        self.horizontalLayout.addWidget(self.label_time_range)
        self.spin_box_time_range = QSpinBox(self)
        self.spin_box_time_range.setMinimumSize(QSize(0, 25))
        self.spin_box_time_range.setMaximumSize(QSize(16777215, 25))
        self.spin_box_time_range.setMaximum(999)
        self.horizontalLayout.addWidget(self.spin_box_time_range)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_fre = QLabel(self)
        self.label_fre.setMinimumSize(QSize(110, 25))
        self.label_fre.setMaximumSize(QSize(110, 25))
        self.horizontalLayout_2.addWidget(self.label_fre)
        self.spin_box_fre = QSpinBox(self)
        self.spin_box_fre.setMinimumSize(QSize(0, 25))
        self.spin_box_fre.setMaximumSize(QSize(16777215, 25))
        self.spin_box_fre.setMaximum(999)
        self.horizontalLayout_2.addWidget(self.spin_box_fre)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_port = QLabel(self)
        self.label_port.setMinimumSize(QSize(110, 25))
        self.label_port.setMaximumSize(QSize(110, 25))
        self.horizontalLayout_3.addWidget(self.label_port)
        self.spin_box_port = QSpinBox(self)
        self.spin_box_port.setMinimumSize(QSize(0, 25))
        self.spin_box_port.setMaximumSize(QSize(16777215, 25))
        self.spin_box_port.setMaximum(999999)
        self.horizontalLayout_3.addWidget(self.spin_box_port)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item)
        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setMinimumSize(QSize(0, 25))
        self.btn_confirm.setMaximumSize(QSize(16777215, 25))
        self.horizontalLayout_4.addWidget(self.btn_confirm)
        self.btn_concel = QPushButton(self)
        self.btn_concel.setMinimumSize(QSize(0, 25))
        self.btn_concel.setMaximumSize(QSize(16777215, 25))
        self.horizontalLayout_4.addWidget(self.btn_concel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_time_range.setText('Time Range')
        self.label_fre.setText('Sample Frequency')
        self.label_port.setText('UDP Port')
        self.btn_confirm.setText('Confirm')
        self.btn_concel.setText('Cancel')

        self.spin_box_time_range.setValue(time_range)
        self.spin_box_fre.setValue(fre)
        self.spin_box_port.setValue(port)

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_concel.clicked.connect(self.reject)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = SettingDialog()
    Dialog.show()
    sys.exit(app.exec_())
