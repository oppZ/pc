from sys import argv


for arg in argv[1:]:
    arg_inverse = ""
    for i in range(len(arg)-1, -1, -1):
        arg_inverse += arg[i]
    print(arg_inverse)
