import threading
import time

# 创建一个锁对象
lock = threading.Lock()


def worker():
    # 获取锁
    lock.acquire()
    try:
        # 执行需要同步的操作
        print("Thread {} is working...".format(threading.Thread.getName(t)))
        # 模拟耗时操作
        time.sleep(1)
    finally:
        # 释放锁
        lock.release()


# 创建多个线程并启动它们
threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("All threads finished.")
