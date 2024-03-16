import threading

counter = 0
lock = threading.Lock()


def f():
    global counter
    lock.acquire()
    try:
        for _ in range(1000000):
            counter += 1
    finally:
        lock.release()


t1 = threading.Thread(target=f)
t2 = threading.Thread(target=f)

t1.start()
t2.start()

t1.join()
t2.join()

print(counter)
