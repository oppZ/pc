import time
import signal as si
import sys


def arret_boucle(s, frame):
    global fin
    fin = True


fin = False
si.signal(si.SIGINT, arret_boucle)
while not fin:
    print("Dans la boucle")
    time.sleep(1)
