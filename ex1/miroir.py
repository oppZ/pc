from sys import argv

arg_inverse = ""
for i in range(len(argv[1])-1, -1, -1):
    arg_inverse += argv[1][i]

print(arg_inverse)
