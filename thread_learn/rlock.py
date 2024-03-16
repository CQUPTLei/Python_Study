import threading
import time


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.RLock()

    def increment(self):
        with self.lock:
            self.value += 1
            print(f"Incremented to {self.value} by {threading.currentThread().getName()}")
            time.sleep(0.1)  # 模拟一些计算或I/O操作

    def decrement(self):
        with self.lock:
            self.value -= 1
            print(f"Decremented to {self.value} by {threading.currentThread().getName()}")
            time.sleep(0.1)  # 模拟一些计算或I/O操作


def worker(counter):
    for _ in range(3):
        counter.increment()
        counter.decrement()


# 创建 Counter 实例
counter = Counter()

# 创建多个线程
threads = []
for i in range(3):
    thread = threading.Thread(target=worker, args=(counter,))
    threads.append(thread)
    thread.start()

# 等待线程执行完成
for thread in threads:
    thread.join()

print("Final counter value:", counter.value)
