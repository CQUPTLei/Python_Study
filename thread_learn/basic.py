import threading


def my_function():
    print("Thread {} is running...".format(threading.Thread.getName(my_thread)))


# 创建线程
my_thread = threading.Thread(target=my_function, name="myThread")

# 启动线程
my_thread.start()

# 等待线程执行完成
my_thread.join()

print("Main thread ends.")
