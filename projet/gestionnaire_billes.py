import multiprocessing as mp
import time

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

if __name__ == "__main__":
    nb_process = 10
    nb_bille = mp.Value('I', 9, lock=True)
    nb_bille_demandee = [i for i in range(nb_process)]
    verrou = mp.Lock()

    with mp.Pool(processes=nb_process) as pool:
        sortie = pool.map(fonctionnaire, [ [ i, nb_bille_demandee[i] ] for i in range(nb_process)])
