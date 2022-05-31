"""
Qui l a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 31/05/2022
"""
import multiprocessing as mp
import time
import os


def fonctionnaire(liste: list):
    indice, nb_bille_demandee = liste
    for i in range(5):
        verrou.acquire()
        while nb_bille.value < nb_bille_demandee:
            time.sleep(.01)
        nb_bille.value -= nb_bille_demandee
        verrou.release()
        print("Le fonctionnaire", indice, "a prit", nb_bille_demandee, "billes, il en reste", nb_bille.value)
        time.sleep(.5)
        nb_bille.value += nb_bille_demandee
        print("Le fonctionnaire", indice, "a rendu", nb_bille_demandee, ", il en reste", nb_bille.value)


def controleur(processes: list, nb_bille_tot: mp.Value):
    print('lol')
    while 0 <= nb_bille.value <= nb_bille_tot and False:
        time.sleep(.01)
    for process in processes:
        os.getpid()


if __name__ == "__main__":
    nb_process = 10
    nb_bille = mp.Value('I', 9, lock=True)
    nb_bille_tot = nb_bille
    nb_bille_demandee = [i for i in range(nb_process)]
    verrou = mp.Lock()

    with mp.Pool(processes=nb_process) as pool:
        pool.map(fonctionnaire, [[i, nb_bille_demandee[i]] for i in range(nb_process)])

    con_trolleur = mp.Process(target=controleur, args=(mp.active_children(), nb_bille_tot,))
    con_trolleur.start()
    con_trolleur.join()
