import pyautogui
import time
import os
import random
from datetime import datetime, timedelta

INFO_PATH = "compte_info.txt"
CHECK_INTERVAL = 0.5
DELAY_ENTRE_CHAMPS = 1.3

ETAPES = ["email", "password", "code", "password"]

def lire_infos():
    if not os.path.exists(INFO_PATH):
        return [""] * len(ETAPES)
    with open(INFO_PATH, 'r') as f:
        lignes = [line.strip() for line in f if line.strip()]
    while len(lignes) < len(ETAPES):
        lignes.append("")
    return lignes[:len(ETAPES)]

def ecrire_et_tab(texte, label):
    print(f"✏️ Remplissage {label} : {texte}")
    pyautogui.write(texte, interval=0.05)
    pyautogui.press('tab')
    time.sleep(DELAY_ENTRE_CHAMPS)

def ecrire_et_enter(texte, label):
    print(f"✏️ Remplissage {label} : {texte}")
    pyautogui.write(texte, interval=0.05)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(DELAY_ENTRE_CHAMPS)

def attendre_et_ecrire_code(index):
    while True:
        infos = lire_infos()
        code = infos[index]
        if code:
            pyautogui.write(code, interval=0.05)
            pyautogui.press('tab')
            print(f"✅ Code inséré : {code}")
            break
        print("⏳ En attente du code...")
        time.sleep(CHECK_INTERVAL)

def generer_date_naissance(min_age=18, max_age=70):
    today = datetime.today()
    start_date = today.replace(year=today.year - max_age)
    end_date   = today.replace(year=today.year - min_age)

    jours_intervalle = (end_date - start_date).days

    # on boucle jusqu'à tomber sur un mois 1–9
    while True:
        candidate = start_date + timedelta(days=random.randint(0, jours_intervalle))
        if 1 <= candidate.month <= 9:
            return candidate.strftime("%d%m%Y")

def surveiller_et_remplir():
    print("🟢 En attente de données dans 'compte_info.txt'...")
    print("📌 Clique dans le premier champ, tu as 3 secondes.")
    time.sleep(3)

    infos = lire_infos()

    ecrire_et_enter(infos[0], "email")
    ecrire_et_enter(infos[1], "password")
    attendre_et_ecrire_code(2)
    ecrire_et_enter(infos[3], "password")
    ecrire_et_tab(infos[1], "password")
    ecrire_et_enter(generer_date_naissance(), "date de naissance")



    print("""⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⢦⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡀⠈⣇⢀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢘⣷⣄⣙⡏⠁⠀⠀⢬⣉⠙⠶⣄⣀⣀⣀⣠⣤⣤⡄⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣼⠿⠟⠉⠉⠀⠀⠀⠀⠀⠉⠙⠛⢿⠉⠉⠁⠀⠀⢸⡇⠀⠀⠀
⠀⠀⠀⣀⣶⡿⠁⠀⠀⠀⠀⡄⠀⢰⣆⠀⠀⠀⠀⠘⣇⠀⠀⠀⢀⣸⡇⠀⠀⠀
⢴⠞⠛⠉⢹⡄⢰⡆⠀⠀⢸⢿⡆⠸⡟⣧⠀⠀⠀⠀⢹⡤⠶⠛⠛⣿⡅⠀⠀⠀
⠸⣇⠀⠀⠸⡇⢸⠀⠀⣶⣿⠤⠿⣆⣿⠙⣳⣄⠀⠀⠈⣧⠀⠀⣺⣽⠇⠀⠀⠀
⠀⠙⣶⣶⠿⡇⣾⡇⠀⣿⣿⣶⡄⠙⢿⡄⠏⠻⣷⣄⠀⢻⡶⢿⣿⠿⠂⠀⠀⠀
⠀⠀⠹⡆⠀⣿⠋⢷⡀⣿⡟⠇⠉⠀⠀⠁⠀⠀⢻⡼⣿⠿⠷⣾⣅⡀⠀⠀⠀⠀
⠀⠀⠀⠹⣾⣷⡶⠾⢷⣸⣷⡀⠀⠀⣆⣤⣴⣤⣾⡿⣏⣀⠀⢻⡿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢹⣧⣄⣤⠿⣿⣿⣿⢶⣶⣾⣯⣿⢿⠁⣸⠏⠙⠛⠶⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣾⣿⠷⠈⢁⣿⣄⣻⣿⣹⣿⣼⣸⣧⠀⠀⠀⠀⢈⣷⠀⠀⠀
⠀⠀⠀⠀⣠⣶⠟⠋⠈⢳⣤⣾⡥⢽⡏⣿⠉⣸⡿⢯⣿⢷⣼⠃⠀⢸⡇⠀⠀⠀
⠀⠀⠀⠀⠻⣏⠀⠀⠀⣾⠁⢻⡟⠋⣿⣿⠀⣿⣀⣤⣿⣼⠛⠇⢀⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣇⠀⠀⠈⢷⣿⠟⠛⣻⡟⢀⡟⠄⢀⣿⡇⠀⠀⢸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣸⣧⠀⠀⠀⣿⠆⢰⣿⢢⣼⠃⠀⣾⢿⡀⠀⠀⣼⣿⣷⢲⣦⡄
⠀⠀⠀⠐⣏⢻⣭⣿⡇⠀⣀⡿⠀⢸⣧⡾⣿⡀⠀⢡⣾⠻⢿⣴⣿⣿⣣⣾⠿⠀
⠀⠀⠀⠀⠹⣄⠻⠿⣣⣴⠿⠶⠶⡿⠉⣇⠈⢳⣤⠿⣿⣶⡟⠹⣿⠛⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠹⢷⣾⣿⡟⠛⠶⢼⣇⣀⣿⣠⡴⢿⡖⠛⢯⣙⡾⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣿⠷⠶⢤⣼⣇⣠⣽⣇⣠⣤⣷⡴⠞⢿⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠉⠙⣷⠈⢷⣀⣤⠾⣶⣶⣾⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⡤⡴⠒⣛⣛⣿⣄⣈⣻⡾⢋⠉⠀⠀⢹⣿⠀⠀⠀⠀⠀""")

    contenu_precedent = "\n".join(lire_infos())
    while "\n".join(lire_infos()) == contenu_precedent:
        time.sleep(CHECK_INTERVAL)

    surveiller_et_remplir()

if __name__ == "__main__":
    try:
        surveiller_et_remplir()
    except KeyboardInterrupt:
        print("\n👋 Script arrêté.")
