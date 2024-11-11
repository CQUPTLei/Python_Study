# -*- coding = utf-8 -*-
# @TIME : 2024/09/24 00:34
# @Author : Grace
# @File : cURL_test.py
# @Software : PyCharm Pro 2024.1
# Overview：

import requests

cookies = {
    'c_adb': '1',
    'UserName': 'weixin_43764974',
    'UserInfo': 'e9666afc6de64ca9a5c7938e610a6700',
    'UserToken': 'e9666afc6de64ca9a5c7938e610a6700',
    'UserNick': '%E6%84%9F%E8%B0%A2%E5%9C%B0%E5%BF%83%E5%BC%95%E5%8A%9B',
    'AU': '680',
    'UN': 'weixin_43764974',
    'BT': '1719235405228',
    'p_uid': 'U010000',
    'Hm_lvt_e5ef47b9f471504959267fd614d579cd': '1721817335',
    'ssxmod_itna2': 'QqGxBD97qmqiwwxlRx+rFxyDmE8nqqDcQj6o6o4nI3qbKDsaeY+DLnCMKHOT7HOGQs9iDkq2iRK7qidu3znoR3kG1Lo4k+G2jEqk2RBni77QCFxQN0NruiKFTILGUgI2ljHDAc=V8+NZCfeu/wimBEjDERhpIfQwf83n+2Ug+rUsQDI9fidwl8bqWxG2YDKDFqD2YiD=',
    'ssxmod_itna': 'QqfxRDyD9AoDuDBPGKiQ23RWxBm5Tq3tt77DlarexA5D8D6DQeGTr0TCpKtKetCiCSvm3DRhH3GtbhmE23at2CHeDHxY=DU=0DKPrDee=D5xGoDPxDeDAeKiTDY4Ddfh5H=DEDeKDRDWKDXEp8YAukfrKDR65D0g4FDQKDucIqDG5omA4D4xGrDm+82hp+VPoDn=iCrEKD9=oDsrijtAFwRbLqcPyfrxSomP7GDCKDjZv8DmmFr4Gd615Ar70evW1eM0xcvQ0D8i0eTBGrMA+4F70YpiiPqjEtz1roudD===',
    'tfstk': 'f7ssE1D_Vfc1wLWBiFeeV7fnN3tbL1Zrkx9AEtnZHhK9l-1dZEIw_SbfR61S0CCcsehpEd3t6Cdx961V3mWassofO_fS0RbNgICBIKAxkmdYvvKGYNo2_5xfH_-ba7rz4OXMonFzaPDTO8xvHoRvCdERMnxYaWl6rbpMm_PSKyz1pJ923VdAMmKLdL9kDcLxX2hptKKvMsL9pDpyEAh9WcHK9HMWhPOGCJORsfJ3VCB9Om6GAdLsSOdIDmICRFO-cBixDM9GKuFx70a2waAwzBfLYctfpK1WF1GLOnBCjgTdXWmfQnO11pb3GqO5kO7lkewTX9t61UsCtuPHfZCGcFbsn8XpX6bkZFU3tpsN4EOkRXFOL9O9PZ1atmdNP9CBzMlE4HBRRHsys0R5YNgb2HoXdQyQdq024WHR9Y-FJN89KdTUdJGOoFpHdQyQdq0DWpv6TJwI6Zf..',
    'uuid_tt_dd': '10_19122683020-1721893693359-511318',
    'fid': '20_67908638586-1723131572011-623453',
    'csdn_newcert_weixin_43764974': '1',
    'historyList-new': '%5B%5D',
    'c_ins_fref': 'https://blog.csdn.net/weixin_43764974',
    'c_ins_fpage': '/index.html',
    'c_ins_um': '-',
    'ins_first_time': '1725036224664',
    'c_ins_prid': '1725036225607_997641',
    'c_ins_rid': '1726259078184_674048',
    'Hm_lvt_ec8a58cd84a81850bcbd95ef89524721': '1724843519,1724949045,1725890925,1726689568',
    'https_waf_cookie': '61e8e913-74f9-4e74b6226eefcc42ea16a80b6dde291b4cb5',
    'c_segment': '6',
    'Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac': '1726259071,1726408076,1726689568,1726939428',
    'HMACCOUNT': 'ED87F025EACED012',
    'c_first_ref': 'www.google.com',
    'c_first_page': 'https%3A//blog.csdn.net/tianchounh/article/details/136435112',
    '_ga': 'GA1.2.1295386767.1719276740',
    'c_dl_prid': '1726690844839_342224',
    'c_dl_rid': '1727004468832_169803',
    'c_dl_fref': 'https://blog.csdn.net/tianchounh/article/details/136435112',
    'c_dl_fpage': '/download/xyyhsdt/20306295',
    'c_dl_um': '-',
    '_ga_7W1N0GEY1P': 'GS1.1.1727006817.43.0.1727006817.60.0.0',
    'weixin_43764974comment_new': '1726775928655',
    '_clck': '12dgjpz%7C2%7Cfpf%7C0%7C1636',
    'fe_request_id': '1727056836056_0542_6401181',
    'dc_sid': '031f72886fb1be946fb1caeee1cb7693',
    'dc_session_id': '10_1727105514118.977411',
    'c_dsid': '11_1727105513436.962170',
    'firstDie': '1',
    'c_page_id': 'default',
    'creative_btn_mp': '2',
    '_clsk': 'xvrt2s%7C1727105518481%7C3%7C0%7Ct.clarity.ms%2Fcollect',
    'c_pref': 'https%3A//blog.csdn.net/weixin_43764974%3Fspm%3D1000.2115.3001.5343',
    'c_ref': 'https%3A//blog.csdn.net/weixin_43764974/article/details/142455675%3Fspm%3D1001.2014.3001.5501',
    'log_Id_pv': '1973',
    'Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac': '1727105520',
    'log_Id_view': '48607',
    'log_Id_click': '2280',
    'dc_tos': 'sk9vnr',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'c_adb=1; UserName=weixin_43764974; UserInfo=e9666afc6de64ca9a5c7938e610a6700; UserToken=e9666afc6de64ca9a5c7938e610a6700; UserNick=%E6%84%9F%E8%B0%A2%E5%9C%B0%E5%BF%83%E5%BC%95%E5%8A%9B; AU=680; UN=weixin_43764974; BT=1719235405228; p_uid=U010000; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1721817335; ssxmod_itna2=QqGxBD97qmqiwwxlRx+rFxyDmE8nqqDcQj6o6o4nI3qbKDsaeY+DLnCMKHOT7HOGQs9iDkq2iRK7qidu3znoR3kG1Lo4k+G2jEqk2RBni77QCFxQN0NruiKFTILGUgI2ljHDAc=V8+NZCfeu/wimBEjDERhpIfQwf83n+2Ug+rUsQDI9fidwl8bqWxG2YDKDFqD2YiD=; ssxmod_itna=QqfxRDyD9AoDuDBPGKiQ23RWxBm5Tq3tt77DlarexA5D8D6DQeGTr0TCpKtKetCiCSvm3DRhH3GtbhmE23at2CHeDHxY=DU=0DKPrDee=D5xGoDPxDeDAeKiTDY4Ddfh5H=DEDeKDRDWKDXEp8YAukfrKDR65D0g4FDQKDucIqDG5omA4D4xGrDm+82hp+VPoDn=iCrEKD9=oDsrijtAFwRbLqcPyfrxSomP7GDCKDjZv8DmmFr4Gd615Ar70evW1eM0xcvQ0D8i0eTBGrMA+4F70YpiiPqjEtz1roudD===; tfstk=f7ssE1D_Vfc1wLWBiFeeV7fnN3tbL1Zrkx9AEtnZHhK9l-1dZEIw_SbfR61S0CCcsehpEd3t6Cdx961V3mWassofO_fS0RbNgICBIKAxkmdYvvKGYNo2_5xfH_-ba7rz4OXMonFzaPDTO8xvHoRvCdERMnxYaWl6rbpMm_PSKyz1pJ923VdAMmKLdL9kDcLxX2hptKKvMsL9pDpyEAh9WcHK9HMWhPOGCJORsfJ3VCB9Om6GAdLsSOdIDmICRFO-cBixDM9GKuFx70a2waAwzBfLYctfpK1WF1GLOnBCjgTdXWmfQnO11pb3GqO5kO7lkewTX9t61UsCtuPHfZCGcFbsn8XpX6bkZFU3tpsN4EOkRXFOL9O9PZ1atmdNP9CBzMlE4HBRRHsys0R5YNgb2HoXdQyQdq024WHR9Y-FJN89KdTUdJGOoFpHdQyQdq0DWpv6TJwI6Zf..; uuid_tt_dd=10_19122683020-1721893693359-511318; fid=20_67908638586-1723131572011-623453; csdn_newcert_weixin_43764974=1; historyList-new=%5B%5D; c_ins_fref=https://blog.csdn.net/weixin_43764974; c_ins_fpage=/index.html; c_ins_um=-; ins_first_time=1725036224664; c_ins_prid=1725036225607_997641; c_ins_rid=1726259078184_674048; Hm_lvt_ec8a58cd84a81850bcbd95ef89524721=1724843519,1724949045,1725890925,1726689568; https_waf_cookie=61e8e913-74f9-4e74b6226eefcc42ea16a80b6dde291b4cb5; c_segment=6; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1726259071,1726408076,1726689568,1726939428; HMACCOUNT=ED87F025EACED012; c_first_ref=www.google.com; c_first_page=https%3A//blog.csdn.net/tianchounh/article/details/136435112; _ga=GA1.2.1295386767.1719276740; c_dl_prid=1726690844839_342224; c_dl_rid=1727004468832_169803; c_dl_fref=https://blog.csdn.net/tianchounh/article/details/136435112; c_dl_fpage=/download/xyyhsdt/20306295; c_dl_um=-; _ga_7W1N0GEY1P=GS1.1.1727006817.43.0.1727006817.60.0.0; weixin_43764974comment_new=1726775928655; _clck=12dgjpz%7C2%7Cfpf%7C0%7C1636; fe_request_id=1727056836056_0542_6401181; dc_sid=031f72886fb1be946fb1caeee1cb7693; dc_session_id=10_1727105514118.977411; c_dsid=11_1727105513436.962170; firstDie=1; c_page_id=default; creative_btn_mp=2; _clsk=xvrt2s%7C1727105518481%7C3%7C0%7Ct.clarity.ms%2Fcollect; c_pref=https%3A//blog.csdn.net/weixin_43764974%3Fspm%3D1000.2115.3001.5343; c_ref=https%3A//blog.csdn.net/weixin_43764974/article/details/142455675%3Fspm%3D1001.2014.3001.5501; log_Id_pv=1973; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1727105520; log_Id_view=48607; log_Id_click=2280; dc_tos=sk9vnr',
    'Referer': 'https://blog.csdn.net/weixin_43764974?type=blog',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'page': '1',
    'size': '20',
    'businessType': 'blog',
    'orderby': '',
    'noMore': 'false',
    'year': '',
    'month': '',
    'username': 'weixin_43764974',
}

# response = requests.get(
#     'https://blog.csdn.net/community/home-api/v1/get-business-list',
#     params=params,
#     cookies=cookies,
#     headers=headers,
# )

response = requests.request(
    method='get',
    url='https://blog.csdn.net/community/home-api/v1/get-business-list',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.text)

# import uncurl
#
# curl_command = '''
# curl 'https://blog.csdn.net/community/home-api/v1/get-business-list?page=1&size=20&businessType=blog&orderby=&noMore=false&year=&month=&username=weixin_43764974' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7' \
#   -H 'Connection: keep-alive' \
#   -H 'Cookie: c_adb=1; UserName=weixin_43764974; UserInfo=e9666afc6de64ca9a5c7938e610a6700; UserToken=e9666afc6de64ca9a5c7938e610a6700; UserNick=%E6%84%9F%E8%B0%A2%E5%9C%B0%E5%BF%83%E5%BC%95%E5%8A%9B; AU=680; UN=weixin_43764974; BT=1719235405228; p_uid=U010000; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1721817335; ssxmod_itna2=QqGxBD97qmqiwwxlRx+rFxyDmE8nqqDcQj6o6o4nI3qbKDsaeY+DLnCMKHOT7HOGQs9iDkq2iRK7qidu3znoR3kG1Lo4k+G2jEqk2RBni77QCFxQN0NruiKFTILGUgI2ljHDAc=V8+NZCfeu/wimBEjDERhpIfQwf83n+2Ug+rUsQDI9fidwl8bqWxG2YDKDFqD2YiD=; ssxmod_itna=QqfxRDyD9AoDuDBPGKiQ23RWxBm5Tq3tt77DlarexA5D8D6DQeGTr0TCpKtKetCiCSvm3DRhH3GtbhmE23at2CHeDHxY=DU=0DKPrDee=D5xGoDPxDeDAeKiTDY4Ddfh5H=DEDeKDRDWKDXEp8YAukfrKDR65D0g4FDQKDucIqDG5omA4D4xGrDm+82hp+VPoDn=iCrEKD9=oDsrijtAFwRbLqcPyfrxSomP7GDCKDjZv8DmmFr4Gd615Ar70evW1eM0xcvQ0D8i0eTBGrMA+4F70YpiiPqjEtz1roudD===; tfstk=f7ssE1D_Vfc1wLWBiFeeV7fnN3tbL1Zrkx9AEtnZHhK9l-1dZEIw_SbfR61S0CCcsehpEd3t6Cdx961V3mWassofO_fS0RbNgICBIKAxkmdYvvKGYNo2_5xfH_-ba7rz4OXMonFzaPDTO8xvHoRvCdERMnxYaWl6rbpMm_PSKyz1pJ923VdAMmKLdL9kDcLxX2hptKKvMsL9pDpyEAh9WcHK9HMWhPOGCJORsfJ3VCB9Om6GAdLsSOdIDmICRFO-cBixDM9GKuFx70a2waAwzBfLYctfpK1WF1GLOnBCjgTdXWmfQnO11pb3GqO5kO7lkewTX9t61UsCtuPHfZCGcFbsn8XpX6bkZFU3tpsN4EOkRXFOL9O9PZ1atmdNP9CBzMlE4HBRRHsys0R5YNgb2HoXdQyQdq024WHR9Y-FJN89KdTUdJGOoFpHdQyQdq0DWpv6TJwI6Zf..; uuid_tt_dd=10_19122683020-1721893693359-511318; fid=20_67908638586-1723131572011-623453; csdn_newcert_weixin_43764974=1; historyList-new=%5B%5D; c_ins_fref=https://blog.csdn.net/weixin_43764974; c_ins_fpage=/index.html; c_ins_um=-; ins_first_time=1725036224664; c_ins_prid=1725036225607_997641; c_ins_rid=1726259078184_674048; Hm_lvt_ec8a58cd84a81850bcbd95ef89524721=1724843519,1724949045,1725890925,1726689568; https_waf_cookie=61e8e913-74f9-4e74b6226eefcc42ea16a80b6dde291b4cb5; c_segment=6; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1726259071,1726408076,1726689568,1726939428; HMACCOUNT=ED87F025EACED012; c_first_ref=www.google.com; c_first_page=https%3A//blog.csdn.net/tianchounh/article/details/136435112; _ga=GA1.2.1295386767.1719276740; c_dl_prid=1726690844839_342224; c_dl_rid=1727004468832_169803; c_dl_fref=https://blog.csdn.net/tianchounh/article/details/136435112; c_dl_fpage=/download/xyyhsdt/20306295; c_dl_um=-; _ga_7W1N0GEY1P=GS1.1.1727006817.43.0.1727006817.60.0.0; weixin_43764974comment_new=1726775928655; _clck=12dgjpz%7C2%7Cfpf%7C0%7C1636; fe_request_id=1727056836056_0542_6401181; dc_sid=031f72886fb1be946fb1caeee1cb7693; dc_session_id=10_1727105514118.977411; c_dsid=11_1727105513436.962170; firstDie=1; c_page_id=default; creative_btn_mp=2; _clsk=xvrt2s%7C1727105518481%7C3%7C0%7Ct.clarity.ms%2Fcollect; c_pref=https%3A//blog.csdn.net/weixin_43764974%3Fspm%3D1000.2115.3001.5343; c_ref=https%3A//blog.csdn.net/weixin_43764974/article/details/142455675%3Fspm%3D1001.2014.3001.5501; log_Id_pv=1973; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1727105520; log_Id_view=48607; log_Id_click=2280; dc_tos=sk9vnr' \
#   -H 'Referer: https://blog.csdn.net/weixin_43764974?type=blog' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"'
# '''
#
# # 使用uncurl转换为requests请求
# req = uncurl.parse_context(curl_command)
#
# req1 = uncurl.parse(curl_command)
#
# local_namespace = {}
#
# # exec('import requests\n' + 'response = ' + req1 + '\njson_response = response.json()', {}, local_namespace)
#
# # 在exec中导入requests并执行请求
# exec('import requests\n'
#      'response = ' + req1 + '\n'
#      'json_response = response.json()',  # 解析JSON
#      {}, local_namespace)
#
# print(local_namespace['json_response'])
#
# # print(global_namespace)
# # # 执行请求
# # response = requests.request(
# #     method=req.method,
# #     url=req.url,
# #     headers=req.headers,
# # )
# #
# # # 打印响应
# # print(response.json())  # 如果返回的是JSON格式
