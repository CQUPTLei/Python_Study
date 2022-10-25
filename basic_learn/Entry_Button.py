# -*- coding = utf-8 -*-
# @TIME :     2022/10/26 上午 12:00
# @Author :   CQUPTLei
# @File :     Entry_Button.py
# @Software : PyCharm

from tkinter import *

def run1():
     a = float(inp1.get())
     b = float(inp2.get())
     s = '%0.2f+%0.2f=%0.2f\n' % (a, b, a + b)
     txt.insert(END, s)   # 追加显示运算结果
     inp1.delete(0, END)  # 清空输入
     inp2.delete(0, END)  # 清空输入

def run2(x, y):
     a = float(x)
     b = float(y)
     s = '%0.2f+%0.2f=%0.2f\n' % (a, b, a + b)
     txt.insert(END, s)   # 追加显示运算结果
     inp1.delete(0, END)  # 清空输入
     inp2.delete(0, END)  # 清空输入

root = Tk()
root.geometry('460x240')
root.title('简单加法器')

lb1 = Label(root, text='请输入两个数，按下面两个按钮之一进行加法计算')
lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

inp1 = Entry(root)
inp1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
inp2 = Entry(root)
inp2.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.1)

# 方法-直接调用 run1()
btn1 = Button(root, text='方法一', command=run1)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

# 方法二利用 lambda 传参数调用run2()
btn2 = Button(root, text='方法二', command=lambda: run2(inp1.get(), inp2.get()))
btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = Text(root)
txt.place(rely=0.6, relheight=0.4)

root.mainloop()
