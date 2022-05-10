import multiprocessing as mp
import random as rm
import array as ar


def somme(pipe: mp.Pipe()) -> None:
    resultat = 0

    while True:
        nb = pipe.recv()
        if nb != -1:
            resultat += nb

        else:
            pipe.send(resultat)
            return


def generation_nb(pipe_paire: mp.Pipe(), pipe_impaire: mp.Pipe()) -> None:
    n = 20
    liste_random = ar.array('I')
    for i in range(n):
        nb = rm.randint(0, 29)
        liste_random.append(nb)
        if nb % 2 == 0:

            pipe_paire.send(nb)
        else:
            pipe_impaire.send(nb)
    pipe_paire.send(-1)
    pipe_impaire.send(-1)
    print("La somme des nombres paires est ", str(pipe_paire.recv()))
    print("La somme des nombres impaires est ", str(pipe_impaire.recv()))
    return


if __name__ == "__main__":
    pere_paire, fils_paire = mp.Pipe()
    pere_impaire, fils_impaire = mp.Pipe()

    generateur = mp.Process(target=generation_nb, args=(pere_paire, pere_impaire,))
    filtre_pair = mp.Process(target=somme, args=(fils_paire,))
    filtre_impair = mp.Process(target=somme, args=(fils_impaire,))

    generateur.start()

    filtre_pair.start()
    filtre_impair.start()
    filtre_pair.join()
    filtre_impair.join()
    generateur.join()
