"""
Qui l a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 07/06/2022
"""
import multiprocessing as mp
import random
import ctypes
import time


def effacer_ecran(): print(CLEARSCR, end='')


def serveur(id_serveur: int) -> None:
    while keep_running.value:
        time.sleep(1)
        if commandes != mp.Array(ctypes.c_short, [0] * 50):
            verrou.acquire()
            commande_en_cours[id_serveur] = commandes[indice.value]
            commande_en_cours[id_serveur + 1] = commandes[indice.value - 1]
            indice.value -= 2
            verrou.release()


def client(id_client: int) -> None:
    while keep_running.value:
        time.sleep(random.randint(1, 3))
        verrou.acquire()
        commandes[indice.value] = id_client
        commandes[indice.value + 1] = random.randint(65, 90)
        indice.value += 2
        verrou.release()


def major_dhomme(nb_serveurs: int, nb_clients: int) -> None:
    while keep_running.value:
        effacer_ecran()
        for i in range(nb_serveurs):
            print("Le serveur", i, "traite la commande", (commande_en_cours[2 * i], commande_en_cours[2 * i + 1]))
        print("Commandes de clients en attente:", end='')
        for i in range(len(commandes)):
            if commandes[i:i+2] != mp.Array(ctypes.c_short, (0, 0)):
                print('(', commandes[i], ',', commandes[i + 1], ')', end='')
        print()
        time.sleep(1)


if __name__ == "__main__":
    CLEARSCR = "\x1B[2J\x1B[;H"  # Clear SCreen

    nb_serveurs = 5
    nb_clients = 8
    keep_running = mp.Value(ctypes.c_bool, True)
    commandes = mp.Array(ctypes.c_short, [0] * 50)
    indice = mp.Value(ctypes.c_short, 0)
    verrou = mp.Lock()
    verrou2 = mp.Lock()

    commande_en_cours = mp.Array(ctypes.c_short, [0] * (nb_serveurs * 2))

    lst_clients = []

    for i in range(nb_clients):
        lst_clients.append(mp.Process(target=client, args=(i,)))
        lst_clients[-1].start()

    for i in range(nb_serveurs):
        lst_clients.append(mp.Process(target=serveur, args=(i,)))
        lst_clients[-1].start()

    printage = mp.Process(target=major_dhomme, args=(nb_serveurs, nb_clients))
    printage.start()
