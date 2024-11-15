# -*- coding = utf-8 -*-
# @TIME : 2022/10/24 下午 4:02
# @Author : CQUPTLei
# @File : YouTube_download.py.py
# @Software : PyCharm

import time
import os
from you_get import common
import subprocess
'''
默认参数
'''
#视频链接
v_url = 'https://www.bilibili.com/video/BV1JF411L7zw?spm_id_from=333.851.b_7265636f6d6d656e64.5'
#保存格式
v_format = 'dash-flv'
#保存路径
save_dir = 'D:\Python_Study\File_Save\IU'

#提示信息打印函数
#'\033[5;36m' 用来设置输出内容的字体颜色和背景颜色
def LOG(info):
    print('\033[5;36m' + 'You-get: ' + time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())) + ' '+info + '\033[0m')

#设置要下载的视频连接
LOG("输入要下载的视频链接：")
url=input("URL:")
if url=='':
    pass
else:
    v_url=url.replace('&','"&"')
    #print(v_url)
    #v_url=url

#设置代理,默认不设置
#也可以在pycharm设置中设置（proxy）
# LOG("是否需要设置代理下载（y/n）？")
# proxy=input()
# if proxy=='y':
#     common.set_http_proxy(input("请输入代理服务器和端口，例如：127.0.0.1:1080"))
# elif proxy=='':
#     pass
#或者直接设置
# common.set_http_proxy('127.0.0.1:7890')

#打印输出可供选择的清晰度
LOG("正在加载可供下载的清晰度...")
if input()=='':
    pass
# subprocess.run(['you-get','-i',v_url])
os.system('you-get -i '+v_url)

#选择清晰度默认MP4最高画质
LOG("请输入你要下载的清晰度（默认dash-flv）：")
quality=input("format select:")
if quality=='':
   pass
else:
    v_format=quality

#设置保存路径，默认为D:\Python_Study\File_Save
LOG("请设置保存路径(默认路径为：D:\Python_Study\File_Save)")
path=input("save path:")
if path=='':
    pass
else:
    save_dir=path

#根据设置的参数进行下载
LOG("开始下载...")
common.any_download(url=v_url,stream_id=v_format,info_only=False,output_dir=save_dir,merge=True)
LOG("下载完毕")
