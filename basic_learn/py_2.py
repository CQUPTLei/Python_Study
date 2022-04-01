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

x = random.randint(0, 100)  # [0,100]之间的随机数
print(x, "\n")

# for循环
for i in range(0,10,2):  #步长为2
    print(i)


print("\n")  # 遍历字符串
name = "cqupt"
for x in name:
    print(x, end="\t")

print("\n")  # 遍历列表
a = ["aa", 'bb', "cc"]
for i in range(len(a)):
    print(i, a[i])

# while循环,while可以配合else一起用
print("\n")
i = 0
while i < 5:
    print("这是第%d次循环" % (i+1))
    i += 1


i=0
end=0
while i<=100:
    end+=i
    i+=1
print("\n计算1到100的和：",end,end="\n")

# break结束整个循环，continue结束本次循环进入下一次循环
i=0
while i<10:
    print("-"*50)
    i+=1
    if i==5:
        continue
    print(i)
print("\n")

#乘法表
i=1
while i<=9:
    j=1
    while j<=i:
        print("%d*%d=%d"%(i,j,i*j),end="\t")
        j+=1
    i+=1
    print("\n")