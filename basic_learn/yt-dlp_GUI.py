# -*- coding = utf-8 -*-
# @TIME :     2022/10/26 上午 1:08
# @Author :   CQUPTLei
# @File :     yt-dlp_GUI.py
# @Software : PyCharm

# 本程序主窗口缩放会发生布局改变，读者可以修改为相对位置和相对大小
import time
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import filedialog
import yt_dlp


#默认参数
save_dir=r'D:\Python_Study\File_Save\test'  #我的默认保存地址
global path
global v_url
global v_video_format
global v_audio_format
v_url='https://www.youtube.com/watch?v=gg8su13TRkI&ab_channel=Kilun'
v_video_format='bestvideo'  #默认最高质量视频和音频，很多视频音频和视频是分开的，用ffmpeg自动合并
v_audio_format='bestaudio'
path=save_dir

# 提示信息打印函数
# '\033[5;36m' 用来设置输出内容的字体颜色和背景颜色
def LOG(info):
    print('\033[5;36m' + 'Info: ' + time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())) + ' ' + info + '\033[0m')

# 建立一个根窗口
root = Tk()
root.title('视频下载程序')
root.geometry('800x500')
root.resizable(0, 0) # 设置窗口大小不可变

#手动输入视频url，不输入则为默认url
def url_input():
    global v_url
    v_url = get_url.get()
    v_url = v_url.replace('&', '"&"') #URL中&不可用于shell


# 获取视频信息，并弹出一个窗口显示
def get_info():
    global v_url
    #这里可以使用yt-dlp的库函数，我只是测试os模块
    return_code = subprocess.run(['yt-dlp', '-F', v_url], stdout=subprocess.PIPE) #调用shell，获取视频信息
    res = return_code.stdout.decode('utf-8')   #视频信息保存与res中
    info_win = Toplevel(root)   #打开一个窗口显示可供下载的视频格式
    info_win.geometry('1000x600')
    info_win.config(background='#CCCCFF')
    info_win.title('该视频的详细信息')
    info_txt = Text(info_win, bg='#CCCCFF', fg='#000000', font=("Roboto", 12), wrap='word')
    info_txt.place(relx=0, y=0, relheight=1, relwidth=1) #text空间填满子窗口
    info_txt.insert(END, res)  #显示该视频信息


#选择视频保存路径，返回内容是字符串
def get_path():
    global path
    path = filedialog.askdirectory(title='请选择一个目录')# 返回一个字符串，且只能获取文件夹路径，不能获取文件的路径。
    #path = filedialog.askopenfilename(title='请选择文件')# 返回一个字符串，可以获取到任意文件的路径。
    # 生成保存文件的对话框， 选择的是一个文件而不是一个文件夹，返回一个字符串。
    # path = filedialog.asksaveasfilename(title='请输入保存的路径')
    entry_text.set(path)


#自定义选择音视频质量
def select_format():
    global v_video_format
    global v_audio_format
    v_video_format=video_input.get()
    v_audio_format=audio_input.get()
    # print(v_audio_format)


#下载函数，正式传入下载的各项参数
def start_download():
    global v_url
    global path
    global v_audio_format
    global v_video_format
    Q=(v_video_format,'+',v_audio_format)
    Q="".join(Q)
    #下载（器）选项，下列参数可以在YoutubeDL.py以及common.py中查询
    #鼠标放在相关函数上，弹窗中右键选择“编辑源”即可查看支持的参数及其说明
    download_opts = {
        #-----------------基本参数---------------------
        'proxy': '127.0.0.1:7890', #代理
        'format': Q,               #音视频质量
        'paths':{'home':path},     #保存路径

        #----------------加强参数----------------------
        'extractor_retries':10,    #发生错误时最大重复次数
        'no_warnings':True,        #不输出warning
        'ignoreerrors':'only_download',
        'wait_for_video':(20,30),   #重试等待时间区间，单位s
        'retries': 10,              # http错误的重复次数，5xx (很有用的选项)

        'fragment_retries': 10,      # 片段的重试次数
        'file_access_retries': 10,   # 文件获取错误重复次数
        'continuedl': True,          # 尝试继续下载
        'continue': True,
        'noprogress': False,          # 显示进度条
        'consoletitle':False,
        'restrict-filenames': False, #将文件名限制为仅 ASCII字符，并避免使用“&”和空格
    }
    #开始下载
    with yt_dlp.YoutubeDL(download_opts) as ydl:
        ydl.download([v_url])


#视频地址输入提示：
tip_txt=Label(root,text='输入视频URL',font=("Roboto", 12),width=11,height=2)
tip_txt.place(relx=0.01,rely=0)
# 视频地址输入框
get_url = Entry(root,bg='#FAFAD2')
get_url.place(x=105, y=0, width=600, height=40)
#确定按钮（必须点击，否则下载默认url中的视频）
btn0 = Button(root, text='确定', bg='#FFE4C4',command=url_input)
btn0.place(x=655, rely=0, width=50, height=40)
# 获取视频信息按钮（可选项目）
btn1 = Button(root, text='获取视频信息', bg='#FFD39B',command=get_info)
btn1.place(x=705, rely=0, width=85, height=40)


#选择视频保存路径
dir_label=Label(root,text='视频保存路径',font=("Roboto", 12),width=11,height=2)
dir_label.place(relx=0.01,rely=0.08)
# 保存目录输入框
entry_text = tkinter.StringVar()
entry = tkinter.Entry(root, textvariable=entry_text,bg='#00CD66', font=('FangSong', 10), width=30, state='readonly')
entry.place(x=105, y=40, width=600, height=40)
# 目录选择按钮
button = tkinter.Button(root, text='选择路径', bg='#C1CDC1',command=get_path)
button.place(x=705, y=40,width=85, height=40)


#视频、音频质量选择，默认最高质量，可以不选择
format_label=Label(root,text='自定义格式',font=("Roboto", 12),width=11,height=2)
format_label.place(relx=0.01,rely=0.17)
#视频
video_label=Label(root,text='视频',bg='#EEAD0E',font=("Roboto", 12))
video_label.place(x=105,y=80,width=50, height=40)
video_input=Entry(root,bg='#E6E6FA')
video_input.place(x=155,y=80,width=250,height=40)
#音频
audio_laubel=Label(root,text='音频',bg='#9932CC',font=("Roboto", 12))
audio_laubel.place(x=405,y=80,width=50, height=40)
audio_input=Entry(root,bg='#E6E6FA')
audio_input.place(x=455,y=80,width=250,height=40)
#确定按钮
button = tkinter.Button(root, text='确定', bg='#EEB4B4',command=select_format)
button.place(x=705, y=80,width=85, height=40)


#下载按钮
dl_txt=Label(root,text='可以不指定音视频质量，默认下载最高质量音视频，由ffmpeg自动合并',font=('FangSong', 12),bg='#FFFFF0')
dl_txt.place(x=1,y=120,width=530,height=40)
download = tkinter.Button(root, text='点击开始下载', bg='#00FF00',font=('楷体', 14),command=start_download)
download.place(x=525, y=120,width=265, height=40)


#日志输出框
log=Text(root,bg='black')
log.place(x=10,y=170,width=780,height=320)


root.mainloop()
