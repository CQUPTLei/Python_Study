# -*- coding = utf-8 -*-
# @TIME : 2024/09/24 03:28
# @Author : Grace
# @File : requests_demo.py
# @Software : PyCharm Pro 2024.1
# Overview：

import requests

r = requests.get(r'https://www.baidu.com',)

print(r.status_code)
print(r.text)