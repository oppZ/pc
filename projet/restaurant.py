"""
Qui l'a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 07/06/2022
"""
import multiprocessing as mp
import random
import ctypes
import time


def effacer_ecran(): print(CLEARSCR, end='')  # Recupere de la course hippique


def serveur(id_serveur: int) -> None:
    """
    Serveur qui s occupant d une commande a la fois
    """
    while True:
        time.sleep(1)
        if nb_commande_traitees.value > 0:
            for com in commandes:
                if com != 0:
                    verrou.acquire()
                    nb_commande_traitees.value -= 1
                    commande_en_cours[id_serveur] = commandes[indice.value]
                    commande_en_cours[id_serveur + 1] = commandes[indice.value - 1]
                    indice.value -= 2
                    verrou.release()
                    break
        else:
            return


def client(id_client: int) -> None:
    """
    Client passant une commande a la fois
    """
    while True:
        time.sleep(random.randint(1, 3))
        if nb_commande_envoyees.value > 0:
            verrou.acquire()
            nb_commande_envoyees.value -= 1
            commandes[indice.value] = id_client
            commandes[indice.value + 1] = random.randint(65, 90)
            indice.value += 2
            verrou.release()
        else:
            return


def major_dhomme(nb_serveurs: int) -> None:
    """
    Affiche les commandes etant traitees par les serveurs et la liste des commandes en attente
    """
    while nb_commande_envoyees.value > 0 or nb_commande_traitees.value > 0:
        effacer_ecran()

        for i in range(nb_serveurs):
            print("Le serveur", i, "traite la commande", (commande_en_cours[2 * i], commande_en_cours[2 * i + 1]))

        print("Commandes de clients en attente:", end='')
        for i in range(0, len(commandes), 2):
            if commandes[i:i + 2] != [0, 0]:
                print('(', commandes[i], ',', commandes[i + 1], ')', end='')

        print()  # Permet d'afficher correctement le texte sur le terminal
        time.sleep(.1)


if __name__ == "__main__":
    CLEARSCR = "\x1B[2J\x1B[;H"  # Recupere de la course hippique

    # Parametres modifiables
    nb_serveurs = 5
    nb_clients = 15
    nb_commandes = 10

    nb_commande_envoyees = mp.Value(ctypes.c_int, nb_commandes)
    nb_commande_traitees = mp.Value(ctypes.c_int, nb_commandes)
    commandes = mp.Array(ctypes.c_short, [0] * 50)
    indice = mp.Value(ctypes.c_short, 0)  # Pointeur de la liste de commandes partage entre les programmes
    verrou = mp.Lock()  # Verrou permetant d empecher que deux programmes modifient la liste des commandes
    commande_en_cours = mp.Array(ctypes.c_short, [0] * (nb_serveurs * 2))
    lst_prog = []

    for i in range(nb_clients):
        lst_prog.append(mp.Process(target=client, args=(i,)))
        lst_prog[-1].start()

    for i in range(nb_serveurs):
        lst_prog.append(mp.Process(target=serveur, args=(i,)))
        lst_prog[-1].start()

    printage = mp.Process(target=major_dhomme, args=(nb_serveurs,))
    printage.start()
    printage.join()
