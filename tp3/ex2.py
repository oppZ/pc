import os
import sys

"""
if os.fork() == 0:
    os.close(dfr)
    os.dup2(dfw, sys.stdout.fileno())
    os.execlp("cat", "cat", "fichier_osef.txt")
    os.close(dfw)
else:
    os.close(dfw)
    os.dup2(dfr, sys.stdin.fileno())
    os.execlp("wc", "wc")
    os.close(dfr)
"""

dfr, dfw = os.pipe()
if os.fork() == 0:
    dfr2, dfw2 = os.pipe()
    if os.fork() == 0:
        os.close(dfr2)
        os.dup2(dfw2, sys.stdout.fileno())
        os.execlp("sort", "sort", "fichier_osef.txt")
        os.close(dfw2)
    else:
        os.close(dfr)
        os.close(dfw2)
        os.dup2(dfw, sys.stdout.fileno())
        os.dup2(dfr2, sys.stdin.fileno())
        os.execlp("grep", "grep", "gigachad")
        os.close(dfr2)
        os.close(dfw)
else:
    os.close(dfw)
    os.dup2(dfr, sys.stdin.fileno())
    os.execlp("tail", "tail", "-n 5", "fichier_trie.txt")
    os.close(dfr)
