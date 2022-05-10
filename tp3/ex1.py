from multiprocessing import Process, Queue, Pipe


def fonction_osef(fichier):
    fichier.put("cringe")

def fonction_cool(fichier):
    fichier.put()

if __name__ == "__main__":
    fichier = Queue()
    cote_pere, cote_fils = Pipe()
    p1 = Process(target=(fonction_osef(fichier)))
    p0 = Process(target=(fonction_osef(int(input("Entrez un nombre")))))
    p0.start()
    p1.start()
    p0.join()
    p1.join()
