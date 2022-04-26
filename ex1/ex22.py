import os
import sys

N = 10
i = 1
while os.fork() == 0 and i <= N:
    i += 1
#print(i)
#sys.exit(0)

for i in range(4) :
	pid = os.fork()
	if pid != 0 :
		print("Ok !")
	print("Bonjour !")
sys.exit(0)