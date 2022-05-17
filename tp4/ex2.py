import multiprocessing as mp
import time


def prog(sm: mp.Semaphore(), txt: str) -> None:
    i = 0
    while i < 10:
        sm.acquire()
        print(txt)
        sm.release()
        time.sleep(.1)
        i += 1


if __name__ == "__main__":
    sm = mp.Semaphore(1)
    p1 = mp.Process(target=prog, args=(sm, "lol"))
    p2 = mp.Process(target=prog, args=(sm, "mdr"))
    p1.start(), p2.start()
    p1.join()
    p2.join()
