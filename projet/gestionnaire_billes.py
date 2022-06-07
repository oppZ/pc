"""
Qui l a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 31/05/2022
"""
import multiprocessing as mp
import time
import os
# import signal


def fonctionnaire(liste: list):
    indice, nb_bille_demandee = liste
    pid[indice] = os.getpid()
    for i in range(5):
        verrou.acquire()
        while nb_bille.value < nb_bille_demandee:
            time.sleep(.01)
        nb_bille.value -= nb_bille_demandee
        verrou.release()
        print("Le fonctionnaire", indice, "a prit", nb_bille_demandee, "billes, il en reste", nb_bille.value)
        time.sleep(.5)
        verrou2.acquire()
        nb_bille.value += nb_bille_demandee
        verrou2.release()
        print("Le fonctionnaire", indice, "a rendu", nb_bille_demandee, ", il en reste", nb_bille.value)
    print("Le fonctionnaire", indice, "a fini.")


"""
def controleur(nb_bille_tot: mp.Value, pid: mp.Array):
    while 0 <= nb_bille.value <= nb_bille_tot.value:
        time.sleep(.01)
        return
    for process in pid:
        os.kill(process, signal.SIGKILL)
        os.kill(os.getppid(), signal.SIGKILL)
"""


if __name__ == "__main__":
    nb_process = 10
    nb_bille = mp.Value('I', nb_process-1)
    nb_bille_tot = mp.Value('I', nb_process-1)
    nb_bille_demandee = [i for i in range(nb_process)]
    verrou = mp.Lock()
    verrou2 = mp.Lock()

    pid = mp.Array('I', range(nb_process))

    # con_trolleur = mp.Process(target=controleur, args=(nb_bille_tot, pid))
    # con_trolleur.start()

    with mp.Pool(nb_process) as pool:
        pool.map(fonctionnaire, [[i, nb_bille_demandee[i]] for i in range(nb_process)])
