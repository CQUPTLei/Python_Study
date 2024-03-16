import threading

shared_resource = []
condition = threading.Condition()


def consumer():
    with condition:
        print("Consumer waiting...")
        condition.wait()
        print("Consumer consumed the resource:", shared_resource.pop(0))


def producer():
    with condition:
        print("Producer producing resource...")
        shared_resource.append("New Resource")
        condition.notify()
        print("Producer notified the consumer.")


# 创建线程
consumer_thread = threading.Thread(target=consumer)
producer_thread = threading.Thread(target=producer)

# 启动线程
consumer_thread.start()
producer_thread.start()

# 等待线程执行完成
consumer_thread.join()
producer_thread.join()

print("Main thread ends.")
