# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Liang Jiayi
# Date: 2019/6/22

import socket


class DataConnection(object):
    def __init__(self, port):
        self.port = port
        self.host = socket.gethostname()
        self.clientSocket = None

    def connection(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind((self.host, self.port))

    # 监控大厅连接
    def recv_data(self):
        try:
            get_data = self.clientSocket.recv(524288).decode('gbk')
        except OSError or UnicodeDecodeError:
            get_data = ''
        # print(get_data)
        get_data_list = get_data.split(",")
        parameters = {}
        for para in get_data_list:
            if para != '':
                name = para.split('#')[0].split(':')[1]
                value = para.split('#')[1]
                parameters[name] = value
        return parameters

    def close_connect(self):
        if self.clientSocket is not None:
            # 关闭接受和发送消息通道，需要在close()之前执行
            # self.clientSocket.shutdown(2)
            self.clientSocket.close()
            self.clientSocket = None
