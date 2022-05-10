from os import fork, getpid

nb_boucle = 3
for i in range(nb_boucle):
    ppid = getpid()
    if fork() == 0:
        print("i: ", i, ". Je suis le processus: ", getpid(), ". Mon pere est: ", ppid)
