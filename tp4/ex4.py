import multiprocessing as mp
import time
import random as rm


def rdv1():
    print("1 est mort")


def rdv2():
    print("2 est mort")


def rdv3():
    print("3 est mort")


def attente1(sm1, sm2, sm3, tps):
    time.sleep(tps)
    print("1 a fini d attendre")
    sm1.release()
    sm1.release()
    sm2.acquire()
    sm3.acquire()
    rdv1()


def attente2(sm1, sm2, sm3, tps):
    time.sleep(tps)
    print("2 a fini d attendre")
    sm2.release()
    sm2.release()
    sm1.acquire()
    sm3.acquire()
    rdv2()


def attente3(sm1, sm2, sm3, tps):
    time.sleep(tps)
    print("3 a fini d attendre")
    sm3.release()
    sm3.release()
    sm1.acquire()
    sm2.acquire()
    rdv3()


if __name__ == "__main__":
    sm1 = mp.Semaphore(0)
    sm2 = mp.Semaphore(0)
    sm3 = mp.Semaphore(0)
    p1 = mp.Process(target=attente1, args=(sm1, sm2, sm3, rm.randint(1, 4)))
    p2 = mp.Process(target=attente2, args=(sm1, sm2, sm3, rm.randint(1, 4)))
    p3 = mp.Process(target=attente3, args=(sm1, sm2, sm3, rm.randint(1, 4)))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
