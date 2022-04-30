import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

# Data structures
hashvalues = []
y = []
queue = mp.Queue()


# Encryption functions
def encrypt_serial(nums):
    for x in nums:
        r = hashlib.sha256(str(x).encode())
        hashvalues.append(r.digest())
    # print(hashvalues)


def encrypt(nums):
    hash_obj = hashlib.sha256(str(nums).encode())
    queue.put(hash_obj.digest())


# Checks and Balances
def isValuesCorrect():
    # making copy of queue
    copy_queue = queue
    # copying queue into list
    while not copy_queue.empty():
        y.append(copy_queue.get())
    # comparing lists
    if set(hashvalues) == set(y):
        print("Hash is correct!")
    else:
        print("Wrong")
    # Emptying
    while not queue.empty():
        queue.get()

    if queue.empty():
        print("\nQueue ready for use.\n")


# Threaded
def threaded(numbers):
    with ThreadPoolExecutor(max_workers=5) as thread_manager:
        thread_manager.map(encrypt, numbers)


# Multiprocessing
def multi(numbers):
    with mp.Pool(processes=6) as p:
        p.map(encrypt, numbers)
        p.close()


if __name__ == "__main__":
    numbers = [x for x in range(100_000)]

    # Serial
    startTime = time.time()
    encrypt_serial(numbers)
    stopTime = time.time()
    serial_time = stopTime - startTime
    print(f'Time for Serial to encode: {serial_time}\n')

    # Threaded
    startTime = time.time()
    threaded(numbers)
    stopTime = time.time()
    thread_time = stopTime - startTime
    print(f'Time for Thread to encode: {thread_time}, speed up {serial_time / thread_time}')
    isValuesCorrect()

    # Multiprocessing
    startTime = time.time()
    multi(numbers)
    stopTime = time.time()
    multi_time = stopTime - startTime
    print(f'Time for Multiprocessing to encode: {multi_time}, speed up {serial_time / multi_time}')
    isValuesCorrect()

