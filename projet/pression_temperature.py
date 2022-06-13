
import multiprocessing
import ctypes
import time

"""
temperature : 1V = 25°C
pression : 1V = 1000hPa
"""
def conversion(V, type):
    if type == "temperature":
        return V*25.00
    elif type == "pression":
        return V*1000
    else:
        return -1

    
"""
fonction qui simule le foncitionnement du capteur
la fonction nous renvoie la tension de la temperature ou de la pression en fonction d'un parametre
"""
def capteur(type, tension_temperature, tension_pression):
    # acces des valeurs partages
    if type == "temperature":
        return tension_temperature.value
    elif type == "pression":
        return tension_pression.value
    else:
        return -1



"""
fonction qui controle le chauffage et la pompe pour pouvoir maintenir
la temperature et la pression a un niveau voulu
"""
def controleur(verrou, go_chauffage, go_pompe):
    while True:
        with verrou:
            # nous recuperons les valeurs de la pression et de la temperature actuels
            T, P = temperature.value, pression.value
        # si la temperature n'atteind pas le seuil de temperature, alors nous mettons le chauffage
        # sinon, nous eteignons le chauffage
        if T >= seuil_t:
            go_chauffage.value = False
        elif T < seuil_t:
            go_chauffage.value = True

        # si la pression est trop importante, alors nous ouvrons les pompes
        # sinon, nous les fermons
        if P >= seuil_p:
            go_pompe.value = True
        else:
            go_pompe.value = False

"""
fonction qui accede aux valeurs partages de la pression et de la temperature pour les afficher
a l'ecran
"""
def ecran(verrou, temperature, pression):
    while True:
        with verrou:
            T, P = temperature.value, pression.value
            
        print(f"Il fait {round(T,2)}°C avec une pression de {round(P, 1)}hPa")
        time.sleep(1)


"""
actualiser_tensions simule le temps passee : chaque 50 ms nous actualisons la valeur de
la tension de la temperature et de la pression en fonction si le chauffage est actif ou pas 
et si la pompe est ouverte ou pas
"""
def actualiser_tensions(verrou, tension_pression, tension_temperature):
    while True:
        with verrou:
            if go_pompe:
                tension_pression.value -= 0.001
            else:
                tension_pression.value += 0.001
            if go_chauffage:
                tension_temperature.value += 0.001
            else:
                tension_temperature.value -= 0.001
        time.sleep(0.05)


"""
nous changeons chaque seconde la valeur de la valeur partagee de la temperature
"""
def set_temperature(verrou, temperature, tension_temperature, tension_pression):
    while True:
        V = capteur("temperature", tension_temperature, tension_pression)
        with verrou:
            temperature.value = conversion(V, "temperature")
        time.sleep(1)

"""
nous changeons chaque seconde la valeur de la valeur partagee de la pression
"""        
def set_pression(verrou, pression, tension_temperature, tension_pression):
    while True:
        V = capteur("pression", tension_temperature, tension_pression)
        with verrou:
            pression.value = conversion(V, "pression")
        time.sleep(1)

if __name__ == "__main__":
    # valeurs partages
    verrou = multiprocessing.Lock()
    seuil_t = 80    # °C
    seuil_p = 3000  # hPa
    tension_temperature = multiprocessing.Value(ctypes.c_double, 1.00)
    tension_pression = multiprocessing.Value(ctypes.c_double, 1.00)
    go_pompe = multiprocessing.Value(ctypes.c_bool, False, lock=False)
    go_chauffage = multiprocessing.Value(ctypes.c_bool, False, lock=False)
    temperature = multiprocessing.Value(ctypes.c_double, 25.00, lock=True)
    pression = multiprocessing.Value(ctypes.c_double, 1000.0, lock=True)

    # definition de tous les processus a lancer
    pro_boucle = multiprocessing.Process(target=actualiser_tensions, args=(verrou, tension_pression, tension_temperature))
    pro_controleur = multiprocessing.Process(target=controleur, args=(verrou, go_chauffage, go_pompe))
    pro_ecran = multiprocessing.Process(target=ecran, args=(verrou, temperature, pression))
    pro_temperature = multiprocessing.Process(target=set_temperature,
                                              args=(verrou, temperature, tension_temperature, tension_pression))
    pro_pression = multiprocessing.Process(target=set_pression,
                                           args=(verrou, pression, tension_temperature, tension_pression))

    # mettre en route tous les processus
    pro_boucle.start()
    pro_controleur.start()
    pro_ecran.start()
    pro_temperature.start()
    pro_pression.start()
