
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

def capteur(type, tension_temperature, tension_pression):
    if type == "temperature":
        return tension_temperature.value
    elif type == "pression":
        return tension_pression.value
    else:
        return -1




def controleur(verrou, go_chauffage, go_pompe):
    while True:
        with verrou:
            T, P = temperature.value, pression.value
        if T >= seuil_t:
            go_chauffage.value = False
        elif T < seuil_t:
            go_chauffage.value = True

        if P >= seuil_p:
            go_pompe.value = True
        else:
            go_pompe.value = False

def ecran(verrou, temperature, pression):
    while True:

        with verrou:
            T, P = temperature.value, pression.value
        print(f"Il fait {round(T,2)}°C avec une pression de {round(P, 1)}hPa")
        time.sleep(1)


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

def set_temperature(verrou, temperature, tension_temperature, tension_pression):
    while True:
        V = capteur("temperature", tension_temperature, tension_pression)
        with verrou:
            temperature.value = conversion(V, "temperature")
        time.sleep(1)

def set_pression(verrou, pression, tension_temperature, tension_pression):
    while True:
        V = capteur("pression", tension_temperature, tension_pression)
        with verrou:
            pression.value = conversion(V, "pression")
        time.sleep(1)

if __name__ == "__main__":
    verrou = multiprocessing.Lock()
    seuil_t = 80    # °C
    seuil_p = 3000  # hPa
    tension_temperature = multiprocessing.Value(ctypes.c_double, 1.00)
    tension_pression = multiprocessing.Value(ctypes.c_double, 1.00)
    go_pompe = multiprocessing.Value(ctypes.c_bool, False, lock=False)
    go_chauffage = multiprocessing.Value(ctypes.c_bool, False, lock=False)
    temperature = multiprocessing.Value(ctypes.c_double, 25.00, lock=True)
    pression = multiprocessing.Value(ctypes.c_double, 1000.0, lock=True)

    pro_boucle = multiprocessing.Process(target=actualiser_tensions, args=(verrou, tension_pression, tension_temperature))
    pro_controleur = multiprocessing.Process(target=controleur, args=(verrou, go_chauffage, go_pompe))
    pro_ecran = multiprocessing.Process(target=ecran, args=(verrou, temperature, pression))
    pro_temperature = multiprocessing.Process(target=set_temperature,
                                              args=(verrou, temperature, tension_temperature, tension_pression))
    pro_pression = multiprocessing.Process(target=set_pression,
                                           args=(verrou, pression, tension_temperature, tension_pression))

    pro_boucle.start()
    pro_controleur.start()
    pro_ecran.start()
    pro_temperature.start()
    pro_pression.start()
