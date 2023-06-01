# -*- coding = utf-8 -*-
# @TIME :     2023-5-2 上午 9:50
# @Author :   CQUPTLei
# @File :     Test.py
# @Software : PyCharm
# @Abstract :
import time


class Test(object):
    def __init__(self, button):
        self.button = button
        self.a = 0

    def a0(self):
        print("我还会回来")
        self.a += 1

    def a1(self):
        while self.button == 1:
            for xunhuan in range(0, 86400):
                time.sleep(5)
                self.a0()
                print("5秒来一次")


if __name__ == '__main__':
    start = 1
    test = Test(start)
    test.a1()
