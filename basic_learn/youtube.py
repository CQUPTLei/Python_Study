# -*- coding = utf-8 -*-
# @TIME : 2022/6/13 下午 2:47
# @Author : CQUPTLei
# @File : youtube.py
# @Softeare : PyCharm

import pytube
from pytube import YouTube

# YouTube('http://youtube.com/watch?v=9bZkp7q19f0').streams.first().download()

yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
yt.streams.all()
yt.streams.filter(progressive=True).all()
yt.streams.filter(adaptive=True).all()
yt.streams.get_by_itag(22)
yt = None
while True:
    try:
        yt = YouTube(url)
        break
    except HTTPError:
        self.logger.error("请求出错一次：HTTPError")
        continue
    except URLError:
        self.logger.error("请求出错一次：URLError")
        continue
streams = yt.streams.filter(subtype='mp4').all()
from pytube import YouTube
yt=YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
mp4=yt.streams.first()
mp4.download(output_path, filename, filename_prefix)
