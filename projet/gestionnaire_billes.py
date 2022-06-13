"""
Qui l a fait: LICI Tancrede & WLAZLOWSKI Mateusz
Quand: 31/05/2022
"""
import multiprocessing as mp
import time
import os
import ctypes
import signal


"""
fonction qui utilise un nombre defini de billes pour travailles
le nombre de billes etant limite, les processus doivent potentiellement
attendre pour avoir assez de billes pour leur travail
"""
def fonctionnaire(liste: list):
    indice, nb_bille_demandee = liste
    pid[indice] = os.getpid()
    for i in range(5):
        # demande de k billes
        verrou.acquire()
        # tant qu'assez de billes ne sont pas disponibles
        while nb_bille.value < nb_bille_demandee:
            time.sleep(.01)
        # recuperer les billes
        nb_bille.value -= nb_bille_demandee
        verrou.release()
        print("Le fonctionnaire", indice, "a prit", nb_bille_demandee, "billes, il en reste", nb_bille.value)
        
        # travail
        time.sleep(.5)
        
        # rendre les billes apres le travail
        verrou2.acquire()
        nb_bille.value += nb_bille_demandee
        verrou2.release()
        print("Le fonctionnaire", indice, "a rendu", nb_bille_demandee, "billes, il en reste", nb_bille.value)
    
    # fin
    print("Le fonctionnaire", indice, "a fini.")
    # indique dans la liste partagee que le processus a fini
    finish[indice] = True

"""
processus qui controle la quantité de billes en ciruclation
si le nombre de billes est anormal, alors il arrete tous les processus
"""
def controleur(nb_bille_tot: mp.Value, pid: mp.Array):
    
    while 0 <= nb_bille.value <= nb_bille_tot.value:
        time.sleep(.01)
        # on teste si au moins un processus n'a pas fini son travail
        end = True
        for f in finish:
            if not f:
                end = False
        if end:
            # tous les fonctionnaires ont termine leur travail
            # aucun processus a arreter
            return

    # on arrete tous les processus lorsque le nombre de billes est anormal
    for process in pid:
        os.kill(process, signal.SIGKILL)
    os.kill(os.getppid(), signal.SIGKILL)



if __name__ == "__main__":
    # variables partages
    nb_process = 5
    nb_bille = mp.Value('I', nb_process-1)
    nb_bille_tot = mp.Value('I', nb_process-1)
    nb_bille_demandee = [i for i in range(nb_process)]
    verrou = mp.Lock()
    verrou2 = mp.Lock()

    # liste partagee des pids de chaque processus
    pid = mp.Array('I', range(nb_process))
    # liste partagee qui contient l'etat des processus 
    # false - travail non fini
    # true - travail fini
    finish = mp.Array(ctypes.c_bool, [False]*nb_process)
    
    # debut du processus controleur
    controleur_p = mp.Process(target=controleur, args=(nb_bille_tot, pid))
    controleur_p.start()

    # debut du travail des fonctionnaires
    with mp.Pool(nb_process) as pool:
        pool.map(fonctionnaire, [[i, nb_bille_demandee[i]] for i in range(nb_process)])
