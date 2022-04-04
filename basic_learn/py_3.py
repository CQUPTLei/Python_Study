# -*- coding = utf-8 -*-
# @TIME : 2022/4/1 下午 4:20
# @Author : CQUPTLei
# @File : py_3.py
# @Softeare : PyCharm
# content：字符串、列表、元组、字典

'''
----------------字符串----------------
'''

#三种引号的使用
print("-"*40+'字符串'+'-'*40)
word='字符串'
sentence="这是一个句子"
paragraph='''这是一个段落
可以有多行
会保存格式
'''
print(word)
print(sentence)
print(paragraph)

my_str='I\' m a student'  #或者不用转义字符，使用双引号，意会
print(my_str)


#字符串的截取和连接
str="chongqing"
print(str)         #打印完整字符串
print(str[0])      #打印第一个字符
print(str[0:5])    #截取
print(str[0:5:2])  #步长为2截取
print(str[6:])     #第6个字符到结尾
print(str[:5])     #开头到第五个

print(str+" "+"hello")   #拼接
print(str*3)             #重复

print("ceshiz\nifucaun")
print(r"ceshiz\nifucaun")   #前面加r，对后面的字符串里面的转义字符全部不解释，即显示原始字符型


#字符串常用方法（函数）



'''
----------------------------列表--------------------------------
'''
#列表（类似数组，但可以使用混合数据类型，可以使用负数下标从后向前访问）
print("-"*40+'列表'+'-'*40)

namelist=[]              #定义空列表
namelist=['小张','小王','小李']
print(namelist)

testlist=[1,'字符串']      #定义混合类型列表
print(type(testlist[0]))
print(type(testlist[1]))

print("\n使用for循环遍历：")
for name in namelist:     #遍历列表
    print(name)

print("\n使用while循环遍历：")
i=0
while i<len(namelist):
    print(namelist[i])
    i+=1

'''
---------------------------列表常用操作-------------------------------------------------
'''
print("-"*40+'列表常用操作'+'-'*40)

#  1.增加 append(如果追加的是一个列表，就把这个列表整体当做一个元素加在后面，即列表嵌套，二维列表)
print("原始列表数据为:")
for name in namelist:
    print(name,end='\t')

nameadd=input('\n请输入你要添加的姓名：')
namelist.append(nameadd)

print("使用append方法增加后列表数据为:")
for name in namelist:
    print(name,end='\t')

#  2.扩展 extend(与append不同，将另一个列表的元素逐一加入另一个列表)

extendlist=['老师','老师','主任']
namelist.extend(extendlist)

print("\n使用extend方法扩展后列表数据为:")
for name in namelist:
    print(name,end='\t')

#  3.插入 insert（指定下标，插入元素）
namelist.insert(1,'校长')
print("\n使用insert方法插入后列表数据为:")
for name in namelist:
    print(name,end='\t')

# 4.删除 del（指定位置）
del namelist[1]
print("\n使用del语句删除后列表数据为:")
for name in namelist:
    print(name,end='\t')

# 5.弹出 pop（del 是内置函数，pop()是类方法），不指定下标时删除末尾元素
namelist.pop()
print("\n使用pop方法弹出后列表数据为:")
for name in namelist:
    print(name,end='\t')

# 6.移除 remove（根据类容而不是下标删除，但对于同样的值只删除第一个出现的那个）
namelist.remove('老师')
print("\n使用remove方法移除’老师‘后列表数据为:")
for name in namelist:
    print(name,end='\t')

# 7. 修改（根据下标指定值即可）
namelist[0]='小红'
print("\n修改指定下标内容后列表数据为:")
for name in namelist:
    print(name,end='\t')

# 8. 查（查找某元素是否在列表中 in 、not in）
findname=input('\n输入你要查找的姓名：')
if findname in namelist:     #(比使用for循环更加快捷)
    print(findname+'在该列表里面')
else:
    print(findname+'不在该列表里面')

# 9. 指定下标范围内查找，返回找到的对应数据的下标
print(namelist.index('小王',0,3))   #范围区间左闭右开，找不到会报错

# 10.统计某一元素出现的次数
print(namelist.count('小王'))

# 11. 反转与排序
numlist=[1,3,4,2,6,5,8]
print(numlist)
numlist.reverse()          #反转
print(numlist)
numlist.sort()              #升序
print(numlist)
numlist.sort(reverse=True)  #降序
print(numlist)

# 12.嵌套(与二维数组类似)
superlist=[[1,2],['a','b'],['元歌','百里']]
print(superlist[2][0]+'\n')

#将9个老师随机分配到3个办公室
import random
office=[[],[],[]]
teacher=['A','B','C','D','E','F','G','H','I']
for name in teacher:
    index=random.randint(0,2)
    office[index].append(name)

i=1
for teacher in office:
    print("办公室%d的人数为%d"%(i,len(teacher)))
    i+=1
    for name in teacher:
        print(name,end='\t')
    print('\n')