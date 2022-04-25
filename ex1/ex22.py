import os,sys
N = 10
i=1
while os.fork()==0 and i<=N :
	i += 1
print(i)
sys.exit(0)