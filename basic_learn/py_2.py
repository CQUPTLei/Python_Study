# -*- coding = utf-8 -*-
# @TIME : 2022/3/31 下午 9:24
# @Author : CQUPTLei
# @File : py_2.py
# @Softeare : PyCharm


'''
条件判断
非 0 和 非空 为True
0 和 None 为False
'''

if True:
    print("True")
else:
    print("False")

score = int(input("输入成绩:"))
if score >= 90 and score <= 100:
    print("等级为：A")
elif score >= 80 and score < 90:
    print("等级为：B")
else:
    print("等级为：C")


import random
x=random.randint(0,100)   #[0,100]之间的随机数
print(x)