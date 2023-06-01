#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023-6-2 上午 1:24
# @Author  : dahu
# @FileName: client_tcp
# @Software: PyCharm
# @Abstract : tcp客户端

import socket

# 定义主机和端口号
host = '127.0.0.1'
port = 8080

# 创建套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
client_socket.connect((host, port))
print("与服务器建立连接：{}:{}".format(host, port))

# 发送数据给服务器
data = "Hello, Server!"
client_socket.sendall(data.encode('utf-8'))

# 接收服务器的响应
response = client_socket.recv(1024).decode('utf-8')
print("从服务器接收到的响应：", response)

# 关闭连接
client_socket.close()
