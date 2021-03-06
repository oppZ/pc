"""
Qui l'a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 31/05/2022
"""

import random
import multiprocessing as mp
import math


def somme_fct(nb_valeur: int):
    """
    Somme les termes calcules
    """
    somme = 0
    for i in range(nb_valeur):
        somme += math.sqrt(1 - random.random() ** 2)
    return somme


if __name__ == "__main__":
    # Parametre modifiable
    nb_valeur = 100000

    nb_process = mp.cpu_count()
    with mp.Pool(processes=nb_process) as pool:
        sortie = pool.map(somme_fct, [nb_valeur // nb_process] * nb_process)
        moyenne = sum(sortie) / nb_valeur
        print("pi vaut", moyenne * 4)
