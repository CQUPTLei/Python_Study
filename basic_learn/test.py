# -*- coding = utf-8 -*-
# @TIME : 2022/1/9 上午 12:01
# @Author : CQUPTLei
# @File : test.py
# @Softeare : PyCharm


# Keywords
import keyword
words=keyword.kwlist
print("Python关键字：")
print(words[1:10])
print(words[11:20])
print(words[21:30])
print(words[31:len(words)],"\n")


#格式化输出
age=22
name='CUQPTLei'
print("I am %s, i am %d years old."%(name,age))
#分隔符： separate
print("www","baidu","com",sep=".")
print("你好啊",end= "")  #没有换行
print("我好")
print("那就好\n")
print("\t来了一个Tab")


#进制 十进制：%d 八进制：%o   十六进制：%x
a=0xc8
print("%#x %x"%(a,a))


#input,输入必须是表达式
age=input("your age:")
print("您的年龄是",age)

in1=input("in1:")
print(in1)
print(type(in1))

s="abc"+"def"
in2=input("s:")
print(in2)
print(type(in2))

s1=3+5
s2=100
in3=input()
print(in3)
print(type(in3))