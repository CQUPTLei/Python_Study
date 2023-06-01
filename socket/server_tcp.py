#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023-6-2 上午 1:23
# @Author  : dahu
# @FileName: server_tcp
# @Software: PyCharm
# @Abstract : tcp服务端

import socket

# 定义主机和端口号
host = '127.0.0.1'
port = 8080

# 创建套接字对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 将套接字绑定到指定的主机和端口
server_socket.bind((host, port))

# 开始监听传入的连接
server_socket.listen(1)
print("服务器正在监听端口 {}:{}".format(host, port))

# 接受传入的连接
client_socket, address = server_socket.accept()
print("与客户端建立连接：{}".format(address))

# 接收来自客户端的数据
data = client_socket.recv(1024).decode('utf-8')
print("从客户端接收到的数据：", data)

# 发送响应给客户端
response = "服务器已接收到数据：{}".format(data)
client_socket.sendall(response.encode('utf-8'))

# 关闭连接
client_socket.close()
server_socket.close()
