import array as ar
import multiprocessing as mp


def tri_pair(lst_nb: ar.array, sm: mp.Semaphore()) -> int:
    i = 0
    n = len(lst_nb)
    while i < n:
        sm.acquire()
        somme.value += lst_nb[i]
        sm.release()
        i += 2


def tri_impair(lst_nb: ar.array, sm: mp.Semaphore()) -> int:
    i = 1
    n = len(lst_nb)
    while i < n:
        sm.acquire()
        somme.value += lst_nb[i]
        sm.release()
        i += 2


if __name__ == "__main__":
    lst_nb = ar.array("I", range(1000))

    sm = mp.Semaphore(1)
    somme = mp.Value('I', 0)
    pair = mp.Process(target=tri_pair, args=(lst_nb, sm))
    impair = mp.Process(target=tri_impair, args=(lst_nb, sm))
    pair.start()
    impair.start()
    pair.join()
    impair.join()
    print(somme.value)
