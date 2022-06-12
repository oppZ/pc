# Cours hippique
# Version très complexe, avec arbitre, en annoncant le gagnant!
import ctypes
import multiprocessing as mp
import random
import signal
import sys
import time

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR = "\x1B[2J\x1B[;H"  # Clear SCreen
CLEAREOS = "\x1B[J"  # Clear End Of Screen
CLEARELN = "\x1B[2K"  # Clear Entire LiNe
CLEARCUP = "\x1B[1J"  # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH"  # ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"  # effacer après la position du curseur
CRLF = "\r\n"  # Retour à la ligne

# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h"  # Curseur visible
CURSOFF = "\x1B[?25l"  # Curseur invisible

# Actions sur les caractères affichables
NORMAL = "\x1B[0m"  # Normal
BOLD = "\x1B[1m"  # Gras
UNDERLINE = "\x1B[4m"  # Souligné

# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK = "\033[22;30m"  # Noir. NE PAS UTILISER. On verra rien !!
CL_RED = "\033[22;31m"  # Rouge
CL_GREEN = "\033[22;32m"  # Vert
CL_BROWN = "\033[22;33m"  # Brun
CL_BLUE = "\033[22;34m"  # Bleu
CL_MAGENTA = "\033[22;35m"  # Magenta
CL_CYAN = "\033[22;36m"  # Cyan
CL_GRAY = "\033[22;37m"  # Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY = "\033[01;30m"  # Gris foncé
CL_LIGHTRED = "\033[01;31m"  # Rouge clair
CL_LIGHTGREEN = "\033[01;32m"  # Vert clair
CL_YELLOW = "\033[01;33m"  # Jaune
CL_LIGHTBLU = "\033[01;34m"  # Bleu clair
CL_LIGHTMAGENTA = "\033[01;35m"  # Magenta clair
CL_LIGHTCYAN = "\033[01;36m"  # Cyan clair
CL_WHITE = "\033[01;37m"  # Blanc
# -------------------------------------------------------


# Définition de qq fonctions de gestion de l'écran


def effacer_ecran(): print(CLEARSCR, end='')


def erase_line_from_beg_to_curs(): print("\033[1K", end='')


def curseur_invisible(): print(CURSOFF, end='')


def curseur_visible(): print(CURSON, end='')


def move_to(lig, col): print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def en_couleur(Coul): print(Coul, end='')


def en_rouge(): print(CL_RED, end='')  # Un exemple !


# -------------------------------------------------------
# La tache d'un cheval
def un_cheval(verrou_fct: mp.Lock, pos_fct: mp.Array, ma_ligne: int, keep_running):  # ma_ligne commence à 0
    col = 1

    while col < LONGEUR_COURSE and keep_running.value:
        with verrou_fct:
            move_to(ma_ligne + 1, col)  # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[ma_ligne % len(lyst_colors)])
            print('(' + chr(ord('A') + ma_ligne) + '>')

            col += 1
            pos_fct[ma_ligne] = col

        try:  # En cas d'interruption
            time.sleep(0.1 * random.randint(1, 5))
        finally:
            pass


# ------------------------------------------------
def prise_en_compte_signaux(signum, frame):
    # On vient ici en cas de CTRL-C p. ex.
    move_to(Nb_process + 11, 1)
    print(f"Il y a eu interruption No {signum} au clavier ..., on finit proprement")

    for i in range(Nb_process):
        mes_process[i].terminate()

    move_to(Nb_process + 12, 1)
    curseur_visible()
    en_couleur(CL_WHITE)
    print("Fini")
    sys.exit(0)


# ---------------------------------------------------
def arbitre_fct(verrou_fct: mp.Lock, pos_fct: mp.Array, pari: mp.Value) -> None:
    """
    Trouve le premier et le dernier de la course.
    Annonce si le pari est remporte ou non
    """
    premier_trouve = False
    dernier_trouve = False
    premier_index = -1
    dernier_index = -1
    while keep_running.value:
        with verrou_fct:
            premier = max(pos_fct)
            dernier = min(pos_fct)
            for i, position in enumerate(pos_fct):
                if position == premier and not premier_trouve:
                    premier_index = i + 1
                    if position == 100:
                        premier_trouve = True
                        break
            for i, position in enumerate(pos_fct):
                if position == dernier and not dernier_trouve:
                    dernier_index = i + 1
                    if position == 99:
                        dernier_trouve = True
                        break

            move_to(len(pos_fct) + 1, 100)
            erase_line_from_beg_to_curs()
            en_couleur(CL_WHITE)
            move_to(len(pos_fct) + 1, 0)
            print("Le premier est", chr(64 + premier_index), "et la grosse merde est", chr(64 + dernier_index))
        time.sleep(.1)
    if pari.value == chr(64 + premier_index):
        print("Bien joué... mais vous n'avez rien gagne.")
    elif pari.value == chr(64 + dernier_index):
        print("MDR T'ES TROP NUL TON CHEVAL EST DERNIER!!!")
    else:
        print("Dommage, vous venez de perde toute vos economies.")


# La partie principale :
if __name__ == "__main__":

    # Une liste de couleurs à affecter aléatoirement aux chevaux
    lyst_colors = [CL_WHITE, CL_RED, CL_GREEN, CL_BROWN, CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
                   CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

    LONGEUR_COURSE = 100  # Tout le monde aura la même copie (donc no need to have a 'value')

    keep_running = mp.Value(ctypes.c_bool, True)

    Nb_process = 20
    mes_process = [0 for i in range(Nb_process)]

    signal.signal(signal.SIGINT, prise_en_compte_signaux)
    signal.signal(signal.SIGQUIT, prise_en_compte_signaux)

    pari = mp.Value(ctypes.c_wchar, str(input("Sur quel canasson pariez-vous? ")))

    effacer_ecran()
    curseur_invisible()

    verrou = mp.Lock()
    pos = mp.Array('I', [1] * Nb_process)

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = mp.Process(target=un_cheval, args=(verrou, pos, i, keep_running,))
        mes_process[i].start()

    arbitre = mp.Process(target=arbitre_fct, args=(verrou, pos, pari))
    arbitre.start()

    move_to(Nb_process + 10, 1)
    print("tous lancés, Controle-C pour tout arrêter")

    # On attend la fin de la course
    for i in range(Nb_process): mes_process[i].join()
    keep_running.value = False

    move_to(Nb_process + 12, 1)
    curseur_visible()
    print("Fini")
