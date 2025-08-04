import requests
import time
import random
import string
import re

BASE_URL = "https://api.mail.tm"
OUTPUT_FILE = "compte_info.txt"

def random_password(length=18):
    return ''.join(random.choices(string.ascii_letters, k=length))


def safe_request(method, url, **kwargs):
    try:
        res = method(url, timeout=10, **kwargs)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR RÉSEAU] {e}")
        return None

def save_info(email, password, code=None):
    with open(OUTPUT_FILE, 'w') as f:
        f.write(f"{email}\n")
        f.write(f"{password}\n")
        if code:
            f.write(f"{code}\n")
        

def create_account():
    print("[1] Récupération du domaine disponible...")
    res = safe_request(requests.get, f"{BASE_URL}/domains")
    if not res:
        raise Exception("Impossible de récupérer les domaines")

    data = res.json()
    if not data.get("hydra:member"):
        raise Exception("Aucun domaine disponible")

    domain = data["hydra:member"][0]["domain"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"{username}@{domain}"
    password = random_password()

    print(f"[2] Création du compte : {email}")
    print(f"[🔑] Mot de passe : {password}")

    res = safe_request(requests.post, f"{BASE_URL}/accounts", json={
        "address": email,
        "password": password
    })

    if not res or res.status_code != 201:
        raise Exception("Erreur à la création du compte :", res.text if res else "Aucune réponse")

    save_info(email, password)
    return email, password

def get_token(email, password):
    print("[3] Authentification...")
    res = safe_request(requests.post, f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })

    if not res:
        raise Exception("Échec d'authentification")

    token = res.json().get("token")
    if not token:
        raise Exception("Token non reçu")
    return token

def check_messages(token, email, password, max_attempts=30):
    headers = {"Authorization": f"Bearer {token}"}
    print("[4] En attente d'un email...")

    for i in range(max_attempts):
        res = safe_request(requests.get, f"{BASE_URL}/messages", headers=headers)
        if not res:
            print(f"[{i+1}/{max_attempts}] Erreur de requête, nouvelle tentative...")
            time.sleep(2)
            continue

        data = res.json()
        messages = data.get("hydra:member", [])
        if messages:
            msg_id = messages[0].get("id")
            subject = messages[0].get("subject", "(pas de sujet)")
            print(f"[📨] Email reçu : {subject}")

            time.sleep(1.5)

            msg_detail = safe_request(requests.get, f"{BASE_URL}/messages/{msg_id}", headers=headers)
            if not msg_detail:
                print("[⚠️] Impossible de lire le contenu du message.")
                return

            full_msg = msg_detail.json()
            text = full_msg.get("text") or full_msg.get("intro") or ""
            if not text:
                print("[ℹ️] Message vide.")
            else:
                print(f"[📥] Contenu reçu.\n{text[:200]}...\n")
                codes = re.findall(r'\b\d{4,8}\b', text)
                if codes:
                    code = codes[0]
                    print(f"[✅] Code trouvé : {code}")
                    save_info(email, password, code)
                else:
                    print("[❌] Aucun code numérique trouvé.")
            return

        print(f"[{i+1}/{max_attempts}] Pas encore de message, nouvelle tentative...")
        time.sleep(2)

    print("[-] Aucun email reçu après l’attente.")

def main():
    try:
        email, password = create_account()
        print(f"[🔗] Adresse email prête : {email}")
        token = get_token(email, password)

        print("[⏳] Utilise cette adresse pour recevoir ton code...")
        time.sleep(5)
        check_messages(token, email, password)

    except Exception as e:
        print(f"[ERREUR GÉNÉRALE] {e}")

if __name__ == "__main__":
    main()
