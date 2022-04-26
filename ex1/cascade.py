import os
import sys
N = 10

pid_pere_supreme = os.getpid()

for i in range(2, N+1):
    dfr, dfw = os.pipe()
    pid = os.fork()
    if pid == 0: # fils
        os.close(dfw)
        pid_pere = os.read(dfr, 4)
        os.close(dfr)
        print( "mon id est",os.getpid(),"id de mon pere", int.from_bytes(pid_pere, "big"))
    else:  # pere
        os.close(dfr)
        b_pid = bytes(os.getpid())
        os.write(dfw, os.getpid().to_bytes(4, byteorder="big"))
        os.close(dfw)
        if os.getpid() != pid_pere_supreme:
            sys.exit(0)
sys.exit(0)