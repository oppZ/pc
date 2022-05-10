from os import fork
from sys import exit

dicoNotes = {"E1": [10, 15, 20], "E2": [12, 16, 15], "E3": [11, 13, 20]}
clees = list(dicoNotes.keys())
print(clees)

for i in range(len(dicoNotes)):
    if fork() == 0:
        moyenne = 0
        etudiant = clees[i]
        for note in dicoNotes[etudiant]:
            moyenne += note
        moyenne /= len(etudiant)
        print("La moyenne de ", etudiant, " est de ", moyenne)
        exit(0)
