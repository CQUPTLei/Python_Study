# -*- coding = utf-8 -*-
# @TIME :     2022/10/26 上午 1:08
# @Author :   CQUPTLei
# @File :     yt-dlp_GUI.py
# @Software : PyCharm


import time
import os
import subprocess
import tkinter
from tkinter import *
import yt_dlp
from yt_dlp import downloader


# v_url='https://www.youtube.com/watch?v=Uf4RdtVytGs&ab_channel=EASMusicChannel'
# v_url: str=v_url.replace('&','"&')


#提示信息打印函数
#'\033[5;36m' 用来设置输出内容的字体颜色和背景颜色
def LOG(info):
    print('\033[5;36m' + 'Info: ' + time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())) + ' '+info + '\033[0m')


# os.system('yt-dlp --version')
# return_code = subprocess.run(['yt-dlp', '-F',v_url])
# print("return code:", return_code)

#建立一个根窗口
root = Tk()
root.title('视频下载程序')
root.geometry('800x500')


#获取视频信息
def get_info():
    v_url=get_url.get()
    v_url=v_url.replace('&','"&"')
    return_code = subprocess.run(['yt-dlp', '-F', v_url], stdout=subprocess.PIPE)
    res = return_code.stdout.decode('utf-8')
    # newwind() #打开一个窗口显示可供下载的视频格式
    info_win = Toplevel(root)
    info_win.geometry('1000x600')
    info_win.config(background='#CCCCFF')
    info_win.title('该视频的详细信息')
    info_txt = Text(info_win, bg='#CCCCFF', fg='#000000',font=("楷体", 12), wrap='word')
    # info_txt.pack(fill="both")
    info_txt.place(relx=0, y=0, relheight=1, relwidth=1)
    info_txt.insert(END,res)


#视频地址输入框
get_url = Entry(root)
get_url.place(x=260,y=60,width=400,height=50)

#获取视频信息按钮
btn1 = Button(root, text='方法一', command=get_info)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)


#设置保存位置按钮
btn1 = Button(root, text='确定', command=get_info)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

#获下载按钮
btn1 = Button(root, text='开始下载', command=get_info)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

#文本显示
txt=Text(root,bg='#CCCCFF',fg='#000000',width=26,height=10,font=("楷体",12),wrap='word')
txt.place(x=0,y=95)


# def newwind():
#     winNew = Toplevel(root)
#     winNew.geometry('320x240')
#     winNew.title('新窗体')
#     info_txt = Text(root, bg='#CCCCFF', fg='#000000',font=("楷体", 12), wrap='word')
#     info_txt.pack()
    # lb2 = Label(winNew, text='我在新窗体上')
    # lb2.place(relx=0.2, rely=0.2)
    # btClose = Button(winNew, text='关闭', command=winNew.destroy)
    # btClose.place(relx=0.7, rely=0.5)


# mainmenu = Menu(root)
# menuFile = Menu(mainmenu)
# mainmenu.add_cascade(label='菜单',menu=menuFile)
# menuFile.add_command(label='新窗体',command=newwind)
# menuFile.add_separator()
# menuFile.add_command(label='退出',command=root.destroy)



# root.config(menu=mainmenu)


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



root.mainloop()














