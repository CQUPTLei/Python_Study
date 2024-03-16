import threading

semaphore = threading.Semaphore(value=2)  # 允许同时两个线程访问


def access_resource():
    with semaphore:
        print(threading.currentThread().getName(), "is accessing the resource.")
        # 假设这里是对共享资源的访问


# 创建多个线程
threads = []
for i in range(5):
    thread = threading.Thread(target=access_resource)
    threads.append(thread)
    thread.start()

# 等待线程执行完成
for thread in threads:
    thread.join()

print("Main thread ends.")
