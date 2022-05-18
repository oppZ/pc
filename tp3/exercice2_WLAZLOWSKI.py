import os
import sys

dfr, dfw = os.pipe()
dfr2, dfw2 = os.pipe()

if os.path.exists("sortie"):
    os.remove("sortie")

output_file = os.open("sortie", os.O_RDWR | os.O_CREAT)

pid = os.fork()
if pid == 0:
    os.close(dfr)
    os.dup2(dfw, sys.stdout.fileno())
    os.close(dfw)
    os.execlp("sort", "sort", "fichier")

os.wait()
os.close(dfw)

pid = os.fork()
if pid == 0:
    os.dup2(dfr, sys.stdin.fileno())
    os.dup2(dfw2, sys.stdout.fileno())
    os.execlp("grep", "grep",  "chaine")

os.wait()
os.close(dfr)
os.close(dfw2)

pid = os.fork()
if pid == 0:
    os.dup2(dfr2, sys.stdin.fileno())
    os.dup2(output_file, sys.stdout.fileno())
    os.execlp("tail", "tail", "-n", "5")

os.wait()
os.close(dfr2)
os.close(output_file)
