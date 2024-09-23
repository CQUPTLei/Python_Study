import requests
from bs4 import BeautifulSoup

# 定义请求的URL
url = 'https://organchem.csdb.cn/scdb/translate/translate.asp'

# 获取用户输入的载荷值
payload_value = input("请输入载荷的值: ")

# 定义POST请求的载荷（表单数据）
data = {
    'eng2chi': payload_value
}

# 定义请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SameSite=Lax; ASPSESSIONIDSUBSSQTC=DHHDELLCGJFPGJNAMNCAPDDJ; ASPSESSIONIDSWAQSQSD=LDLPCHIDLAOMCKCBGKMBCKCB',
    'origin': 'https://organchem.csdb.cn',
    'referer': 'https://organchem.csdb.cn/scdb/translate/default.asp',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'frame',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# 发送POST请求
response = requests.post(url, headers=headers, data=data)

# 将响应内容解码为GB2312编码
response.encoding = 'gb2312'

# 解析HTML响应内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有<font color=blue>标签并获取其中的文本
result = soup.find('font', color='blue').text

# 打印翻译结果
print("翻译结果: ", result)
