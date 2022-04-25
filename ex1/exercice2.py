import sys
if len(sys.argv) <= 1:
	print("Aucune moyenne à calculer")
	return

for note in sys.argv[1:]:
	if (type(note) != int) or not (0 <= int(note) <= 20):
		print("Note non valide")
		return

notes = [ int(note) for note in sys.argv[1:] ]
moyenne = sum(notes)/len(notes)
print("%.2f" %moyenne)
