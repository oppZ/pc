from os import execlp, fork, wait

"""
#Parallele
if fork() == 0:
    execlp("who", "who")
if fork() == 0:
    execlp("ps", "ps")
if fork() == 0:
    execlp("ls", "ls", "-l")
"""
# Sequentiel
if fork() == 0:
    if fork() == 0:
        execlp("who", "who")
    wait()
    print("-----")
    execlp("ps", "ps")
wait()
print("-----")
execlp("ls", "ls", "-l")
