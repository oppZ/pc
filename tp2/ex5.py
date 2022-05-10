from sys import argv, exit
from os import fork, wait, getpid
from time import sleep

pid = getpid()
for i in range(int(argv[1])):
    ret_fork = fork()
    if ret_fork == 0:
        print("Mon pid est: ", ret_fork, "Le pid de mon pere est: ", pid)
        sleep(2 * i)
        exit(i)

for i in range(int(argv[1])):
    print(wait())
