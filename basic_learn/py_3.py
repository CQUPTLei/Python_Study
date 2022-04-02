# -*- coding = utf-8 -*-
# @TIME : 2022/4/1 下午 4:20
# @Author : CQUPTLei
# @File : py_3.py
# @Softeare : PyCharm
# content：字符串、列表、元组、字典

#三种引号的使用
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

