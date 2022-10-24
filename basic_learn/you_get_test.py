# -*- coding = utf-8 -*-
# @TIME : 2022/6/12 下午 8:20
# @Author : CQUPTLei
# @File : you_get_test.py
# @Softeare : PyCharm

import time
import os
from you_get import common

'''
默认参数
'''
#视频链接
v_url = 'https://www.youtube.com/watch?v=o_nxIQTM_B0&list=RD3iM_06QeZi8&index=2&ab_channel=%EC%9D%B4%EC%A7%80%EA%B8%88%5BIUOfficial%5D'
#保存格式
v_format = '137'
#保存路径
save_dir = 'D:\Python_Study\File_Save\JayChou'


#定义提示信息
def LOG(info):
    print('\033[5;36m' + 'You-get: ' + time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())) + ' '+info + '\033[0m')


#设要下载的视频连接
LOG("输入要下载的视频链接：")
url=input("URL:")
if url=='':
    pass
else:
    v_url=url


#设置代理,默认不设置
LOG("是否需要设置代理下载（y/n）？")
proxy=input()
if proxy=='y':
    common.set_http_proxy(input("请输入代理服务器和端口，例如：127.0.0.1:1080"))
elif proxy=='':
    pass

# common.set_http_proxy('116.129.254.212:48603')

#打印输出可供选择的清晰度
LOG("正在加载可供下载的清晰度...")
if input()=='':
    pass
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



