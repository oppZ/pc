import multiprocessing as mp
import random as rm
import time


def prod(file: mp.Queue) -> None:
    i = 0
    while i < 10:
        file.put(rm.randint(0, 15))
        i += 1


def cons(file: mp.Queue, sm: mp.Semaphore, txt: str) -> None:
    i = 0
    while i < 10:
        sm.acquire()
        print(txt, file.get())
        sm.release()
        time.sleep(.1)
        i += 1


if __name__ == "__main__":
    file1 = mp.Queue()
    file2 = mp.Queue()
    sm = mp.Semaphore(1)
    p1 = mp.Process(target=prod, args=(file1,))
    p2 = mp.Process(target=prod, args=(file2,))
    c1 = mp.Process(target=cons, args=(file1, sm, '1'))
    c2 = mp.Process(target=cons, args=(file2, sm, '2'))
    p1.start()
    p2.start()
    c1.start()
    c2.start()
    p1.join()
    p2.join()
    c1.join()
    c2.join()
