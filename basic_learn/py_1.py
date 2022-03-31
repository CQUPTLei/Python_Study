# -*- coding = utf-8 -*-
# @TIME : 2022/1/9 上午 12:01
# @Author : CQUPTLei
# @File : py_1.py
# @Softeare : PyCharm


# Keywords
import keyword
words=keyword.kwlist
print("Python关键字：")
print(words[1:10])
print(words[11:20])
print(words[21:30])
print(words[31:len(words)],"\n")


#输出
age=22
name='CUQPTLei'
print("I am %s, i am %d years old."%(name,age))
#分隔符： separate
print("www","baidu","com",sep=".") #中间连接符为“.”
print("你好啊",end= "")             #没有换行
print("我好")
print("那就好\n")
print("\t来了一个Tab")


#进制 十进制：%d 八进制：%o   十六进制：%x
a=0xc8
print("%#x %x"%(a,a))


#输入input
#输入必须是表达式
age=input("your age:")
print("您的年龄是",age)

in1=input("in1:")
print(in1)
print(type(in1))

s="abc"+"def"
in2=input(s)
print(in2)
print(type(in2))

a=int(input("输入一个数字："))
print("输入的数字为 %d" %a)

a=int("123")     #强制类型转换
print(type(a))
b=a+100
print(b)

# 运算符和表达式

