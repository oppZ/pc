import sys

if len(sys.argv) <= 1:
    print("Aucune moyenne a calculer")
    sys.exit(1)

for note in sys.argv[1:]:
    note = eval(note)
    if (type(note) != int or type(note) != float) or not (0 <= int(note) <= 20):
        print("Note non valide")
        sys.exit(1)

notes = [float(note) for note in sys.argv[1:]]
moyenne = sum(notes) / len(notes)
print(moyenne)
print("%.2f" % moyenne)
