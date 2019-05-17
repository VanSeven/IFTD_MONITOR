import socket
import sys
import os
import sys


class DataConnection:
    def __init__(self, port):
        self.port = port
        self.host = socket.gethostname()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def Connection(self):
        self.clientSocket.bind((self.host, self.port))

    # 监控大厅连接
    def recvData(self):
        recvData = self.clientSocket.recv(524288).decode('utf-8')
        # print(recvData)
        recvDataList = recvData.split(",")
        parameters = {}
        for para in recvDataList:
            if para != "":
                name = para.split("#")[0].split(":")[1]
                value = para.split("#")[1]
                parameters[name] = value
        return parameters
    
    def closeConnect(self):
        self.clientSocket.close()
