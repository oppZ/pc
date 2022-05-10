import signal
import os
import time

pid = os.fork()
if pid == 0:
    signal.signal(signal.SIGINT, lambda s, f: print("intercepte"))
    while True:
        print("je suis ton fils")
        time.sleep(1)
else:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    for i in range(10):
        time.sleep(1)
#        if i == 3:
#            os.kill(pid, signal.SIGUSR1)
        if i == 3 or i == 5:
            os.kill(pid, signal.SIGUSR1)
        print("Je suis ton pere")