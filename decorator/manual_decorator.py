# -*- coding = utf-8 -*-
# @TIME : 2025/07/03 21:25
# @Author : Grace
# @File : manual_decorator.py
# @Software : PyCharm Professional 2025.1.2
# Introduction：手动实现装饰器

import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    """
    计算斐波那契数列
    使用lru_cache缓存结果，避免重复计算
    """
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试性能差异
import time

def fibonacci_without_cache(n):
    """没有缓存的斐波那契函数"""
    if n < 2:
        return n
    return fibonacci_without_cache(n-1) + fibonacci_without_cache(n-2)

# 比较性能
start = time.time()
result1 = fibonacci(35)
time1 = time.time() - start

start = time.time()
result2 = fibonacci_without_cache(35)
time2 = time.time() - start

print(f"带缓存: {result1}, 耗时: {time1:.4f}秒")
print(f"不带缓存: {result2}, 耗时: {time2:.4f}秒")
print(f"性能提升: {time2/time1:.2f}倍")

# 查看缓存信息
print(f"缓存信息: {fibonacci.cache_info()}")
