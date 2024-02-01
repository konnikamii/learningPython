from multiprocessing import Process, Value, Array, Lock
from multiprocessing import Queue, Pool
import os
import time


###Array
def add100ar(numbers, lock):
    for i in range(100):
        time.sleep(0.01)
        with lock:
            for i in range(len(numbers)):
                numbers[i] += 1


if __name__ == "__main__":
    lock = Lock()
    shared_array = Array("d", [0.0, 100.0, 200.0])
    print("array at beggining is", shared_array[:])

    p1 = Process(target=add100ar, args=(shared_array, lock))
    p2 = Process(target=add100ar, args=(shared_array, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("array at beggining is", shared_array[:])


###squares
def add100(number, lock):
    for i in range(100):
        time.sleep(0.01)
        with lock:
            number.value += 1


if __name__ == "__main__":
    lock = Lock()
    shared_number = Value("i", 0)
    print("array at beggining is", shared_number.value)

    p1 = Process(target=add100, args=(shared_number, lock))
    p2 = Process(target=add100, args=(shared_number, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("array at beggining is", shared_number.value)


###queue method
def square(numberss, queue):
    for i in numberss:
        queue.put(i * i)


def make_negative(numberss, queue):
    for i in numberss:
        queue.put(-1 * i)


if __name__ == "__main__":
    numberss = range(1, 6)
    q = Queue()

    p1 = Process(target=square, args=(numberss, q))
    p2 = Process(target=make_negative, args=(numberss, q))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    while not q.empty():
        print(q.get())


###qPool method


def cube(number):
    return number * number * number


if __name__ == "__main__":
    numbers = range(10)

    pool = Pool()
    # map, apply, join, close methods
    result = pool.map(cube, numbers)
    # pool.apply(cube, numbers[0])

    pool.close()
    pool.join()
    print(result)
