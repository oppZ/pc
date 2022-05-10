from sys import exit
from os import fork, wait, getpid

N = 2
ppid = getpid()
for i in range(2*N):
    fork()

if ppid == getpid():
    for i in range(2**N):
        wait()
print("Bonjour")
exit(0)
