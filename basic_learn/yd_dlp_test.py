# -*- coding = utf-8 -*-
# @TIME :     2022/10/25 下午 5:48
# @Author :   CQUPTLei
# @File :     yd_dlp_test.py
# @Software : PyCharm

import time
import os
import subprocess
import tkinter
from tkinter import *
import yt_dlp
from yt_dlp import downloader


v_url='https://www.youtube.com/watch?v=Uf4RdtVytGs&ab_channel=EASMusicChannel'
v_url: str=v_url.replace('&','"&')


#提示信息打印函数
#'\033[5;36m' 用来设置输出内容的字体颜色和背景颜色
def LOG(info):
    print('\033[5;36m' + 'Info: ' + time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())) + ' '+info + '\033[0m')


# os.system('yt-dlp --version')
return_code = subprocess.run(['yt-dlp', '-F',v_url],stdout=subprocess.PIPE)
res=return_code.stdout.decode('utf-8')
# print("return code:", return_code)
# with open(r'D:\Python_Study\basic_learn\out.txt', 'w+') as file:
#     file.write(res)
#     file.close()
print(res)
# #建立一个根窗口
# root = Tk()
# root.title('视频下载程序')
# root.geometry('800x500')
#
# #=========================================================================
# #测试标签（label）的使用,标签文字不变
# lb = Label(root,text='哈哈哈哈哈',
#         bg='#d3fbfb',
#         fg='red',
#         font=('华文新魏',32),
#         width=10,     #这里的单位是‘字符’，一个汉字2个字符
#         height=2,
#         relief=SUNKEN)
# lb.place(x=0,y=0)
#
# #获取时间，标签文字变化(使用configure方法)
# def get_time():
#     timestr = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前的时间并转化为字符串
#     time_lb.configure(text=timestr)               # 重新设置标签文本
#     txt.insert(END,'Info: '+timestr+'\n')         # 用Text输出时间
#     # root.after(1000, get_time)                  # 每隔1s调用函数 gettime 自身获取时间
#     time_lb.after(500,get_time)
#
# time_lb = Label(root, text='', fg='purple',bg='#d3fbfb', font=("黑体", 40),relief=SUNKEN)
# time_lb.place(x=256,y=0)
#
# #==========================================================================
# #滚动条
#
# # scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# #测试文本的使用（Text）
# txt=Text(root,bg='#CCCCFF',fg='#000000',width=26,height=10,font=("楷体",12),wrap=NONE)
# scroll = tkinter.Scrollbar(root)
# scroll.pack(side=RIGHT,fill=Y)
#
# scroll.config(command=txt.yview)
# txt.config(yscrollcommand=scroll.set)
# txt.place(x=0,y=95)
#
# txt.yview_moveto(1)
# txt.update()
#
# get_time()
#
# #==========================================================================
# #输入框（Entry）和按钮（Button）的使用
# inp1 = Entry(root)
# inp1.place(x=260,y=60,width=400,height=50)
#
#
#
# root.mainloop()
#
#
#
#
# text = tkinter.Text(win, width=50, height=8)









