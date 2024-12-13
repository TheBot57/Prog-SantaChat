import socket
import random
import os
import threading

def generate_questions():
    a = random.randint(1000, 10000)
    b = random.randint(1, 100)
    c = random.randint(1, 4)
    f = (a - b) ** c - 25 * c
    return [
        {"question": "Vrai ou Faux : Le Père Noël est originaire de Finlande.", "answer": "faux"},
        {"question": "Quel est le célèbre personnage biblique auquel la fête de Noël est associée ? Ex: Marie", "answer": "jesus"},
        {"question": "Quel est le prénom du célèbre personnage  associé au Père Noël en Laponie ? Ex: Nicolas", "answer": "nicolas"},
        {"question": "Quel jour célèbre-t-on Noël dans la tradition chrétienne ? Ex: 24 Mars", "answer": "25 decembre"},
        {"question": "Quelle est la couleur traditionnelle des vêtements du Père Noël ? Ex: Bleu", "answer": "rouge"},
        {"question": "Vrai ou Faux : La fête de Noël est célébrée au Japon.", "answer": "vrai"},
        {"question": "Quel pays a offert le célèbre sapin de Noël installé chaque année à Trafalgar Square ? Ex: Suède", "answer": "norvege"},
        {"question": "Comment appelle-t-on la bûche traditionnelle de Noël ? Ex: Croissant", "answer": "gateau"},
        {"question": "Quel est le numéro de téléphone à contacter pour joindre les gestionnaires du Trafalgar Square sur maps ? Ex: +229 60000007", "answer": "+44 2079834750"},
        {"question": "Vrai ou Faux : Le film *Maman j'ai raté l'avion* est un classique de Noël.", "answer": "vrai"},
        {"question": "En stéganographie, quel outil populaire est utilisé pour cacher et extraire des données dans une image ? Ex: stegosolve", "answer": "steghide"},
        {"question": "Quel registre est utilisé pour pointer vers la pile en exploitation binaire en architecture x86-64 ? Ex: RAX", "answer": "rsp"},
        {"question": "Quel est le code HTTP pour une redirection permanente ? Ex: 302", "answer": "301"},
        {"question": "Quelle méthode de chiffrement est utilisée dans RSA ? Ex: Symetrique", "answer": "asymetrique"},
        {"question": "Quel port est typiquement utilisé pour HTTPS ? Ex: 80", "answer": "443"},
        {"question": "Vrai ou Faux : Un ransomware chiffre les fichiers d’un système et demande aux victimes de payer des rancons.", "answer": "vrai"},
        {"question": "Quel outil populaire est utilisé pour effectuer des scans réseau ? Ex: masscan", "answer": "nmap"},
        {f"question": f"Combien font ({a} - {b})**{c} - 25*{c} ? Ex: 1458", "answer": f"{f}"},
        {"question": "Quel outil de la NSA est souvent utilisé pour analyser des fichiers binaires ? Ex: IDA", "answer": "ghidra"},
        {"question": "Vrai ou Faux : Un honeypot est une stratégie offensive.", "answer": "faux"},
        {"question": "Quel est le mot magique ? Ex: Wish", "answer": ["Flag", "Wish", "Gift", "Cadeau"]},
    ]

good_responses = [
    "Hohoho! Bravo, petit génie!",
    "Ah, tu fais honneur à l'atelier du Père Noël!",
    "Formidable! Tu mérites un cadeau spécial.",
    "Incroyable! Je suis impressionné.",
    "Tu as fait sourire le Père Noël! Bien joué!",
]

bad_responses = [
    "Hohoho... essaie encore, petit renne.",
    "Ce n'est pas la bonne réponse, mais je crois en toi!",
    "Oh, c'est une erreur... mais tu y arriveras.",
    "Mauvaise réponse! On continue quand même!",
    "Le Père Noël t'encourage à réessayer!",
]

flag = "CMCTF{0zu_G1f7_f0r_S4N74}"

def handle_client(client_socket):
    def colored_text(text, color_code):
        """
    Applique une couleur au texte en utilisant les séquences d'échappement ANSI.
    :param text: Le texte à colorier.
    :param color_code: Le code de couleur ANSI.
    :return: Le texte coloré.
    """
        return f"\033[{color_code}m{text}\033[0m"
    def timeout_handler():
        client_socket.send(b"\nTemps ecoule! Hohoho...\n")
        client_socket.close()
    christmas_banner = '''
             * * * * * * * * * * * * * * * * * * *
           *                                    *
         *   Wishing you a Merry Christmas     *
       *      and a Happy New Year!           *
     *   May your days be filled with joy!   *
   *                                        *
  * * * * * * * * * * * * * * * * * * * * * 
'''
    christmas_banner = """ 
         X
         ^
        /*\\
       /*o*\\
      /*o*o*\\
     /*o*o*o*\\
    /*o*o*o*o*\\
   /*o*o*o*o*o*\\
  /*o*o*o*o*o*o*\\
 /*o*o*o*o*o*o*o*\\
/*o*o*o*o*o*o*o*o*\\
        | |
        
              * * * * * * * * * * * * * * * * * * *
           *                                    *
         *   Wishing you a Merry Christmas     *
       *      and a Happy New Year!           *
     *   May your days be filled with joy!   *
   *                                        *
  * * * * * * * * * * * * * * * * * * * * * 
        """
    client_socket.send(colored_text(christmas_banner, '32').encode()) 
    client_socket.send(b"Hohoho! Bienvenue dans Chat with Santa! \xf0\x9f\x8e\x85\n")
    client_socket.send(b"Reponds correctement aux 21 questions du Pere Noel pour obtenir son cadeau magique!\n\n")
    questions = generate_questions()

    for i, q in enumerate(questions):
        timer = threading.Timer(2, timeout_handler)  
        timer.start()

        client_socket.send(f"Question {i+1}: {q['question']}\n".encode())
        response = client_socket.recv(1024).decode().strip()

        timer.cancel() 

        if isinstance(q['answer'], list):
            if response.lower() not in [ans.lower() for ans in q['answer']]:
                try:
                    client_socket.send(f"{random.choice(bad_responses)}\n".encode())
                except OSError:
                    print(f"Connexion fermée avant la réponse à la question {i+1}.")
                client_socket.close()
                return
        else:
            if response.lower() != q['answer'].lower():
                try:
                    client_socket.send(f"{random.choice(bad_responses)}\n".encode())
                except OSError:
                    print(f"Connexion fermée avant la réponse à la question {i+1}.")
                client_socket.close()
                return

        client_socket.send(f"{random.choice(good_responses)}\n".encode())

    try:
        client_socket.send(b"\xf0\x9f\x8e\x89 Bravo! Voici votre flag magique : " + flag.encode() + b"\n")
    except OSError:
        print("Connexion fermée avant d'envoyer le flag.")

    client_socket.close()

def start_server():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", 12345))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Chat with Santa en écoute sur le port {port}... \xf0\x9f\x8e\x84")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion reçue de {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()







"""import socket
import os

# Define the questions and answers
questions = [
    # General Christmas culture questions
    {"question": "Quel est le personnage biblique celebre auquel la fête de Noel est associee ?", "answer": "jesus"},
    {"question": "Quel celebre personnage est associe au Pere Noel en Laponie ?", "answer": "nicolas"},
    {"question": "Quel jour celebre-t-on Noel dans la tradition chretienne ?", "answer": "25 decembre"},
    {"question": "Quel pays a offert le celebre sapin de Noel installe chaque annee à Trafalgar Square ?", "answer": "Norvege"},
    {"question": "Quelle est la couleur traditionnelle des vetements du Pere Noel ?", "answer": "rouge"},
    
    # Technical and humorous questions
    {"question": "En steganographie, quel outil est utilise pour cacher des donnees dans une image ?", "answer": "steghide"},
    {"question": "Quel est le registre utilise pour pointer vers la pile en exploitation binaire ?", "answer": "esp"},
    {"question": "Quel est le code HTTP pour une redirection permanente ?", "answer": "301"},
    {"question": "Quelle methode de chiffrement est utilisee dans RSA ?", "answer": "asymetrique"},
    
    # The final magic word question
    {"question": "Quel est le mot magique ?", "answer": ["Flag", "Wish", "Gift"]}  # Accept multiple answers
]

# The final flag
flag = "ChristmasCTF{0zu_Gift_f0r_S4N74}"

# Function to handle client communication
def handle_client(client_socket):
    client_socket.send(b"Bienvenue dans Chat with Santa!\n")
    client_socket.send(b"Repondez correctement aux 10 questions pour obtenir le flag !\n\n")

    for i, q in enumerate(questions):
        client_socket.send(f"Question {i+1}: {q['question']}\n".encode())
        response = client_socket.recv(1024).decode().strip()
        # For the final question, check if the response matches any allowed answerc
        if isinstance(q['answer'], list):
            if response.lower() not in [ans.lower() for ans in q['answer']]:
                client_socket.send(b"Mauvaise reponse! Essayez encore!\n")
                client_socket.close()
                return
        else:
            if response.lower() != q['answer'].lower():
                client_socket.send(b"Mauvaise reponse! Essayez encore!\n")
                client_socket.close()
                return

    client_socket.send(b"Bravo! Voici votre flag: " + flag.encode() + b"\n")
    client_socket.close()

# Set up the server
def start_server():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", 12345))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Chat with Santa en écoute sur le port {port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion reçue de {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
"""

"""import socket
import random
import os

# Define questions and answers
questions = [
    {"question": "Quel est le nom des 9 rennes du Père Noël ?", "answer": "Rudolph, Dasher, Dancer, Prancer, Vixen, Comet, Cupid, Donner, Blitzen"},
    {"question": "En quelle année a été publié 'Le Chant de Noël' de Charles Dickens ?", "answer": "1843"},
    {"question": "Quel est le nom du bonhomme de neige magique dans la chanson populaire de Noël ?", "answer": "Frosty"},
    {"question": "Quelle boisson est souvent laissée au Père Noël la veille de Noël ?", "answer": "Lait"}
]

flag = "CTF{Chat_with_Santa_Was_Fun}"

# Function to handle client communication
def handle_client(client_socket):
    client_socket.send(b"Bienvenue dans Chat with Santa!\n")
    client_socket.send(b"Repondez correctement aux 4 questions pour obtenir le flag!\n\n")

    for i, q in enumerate(questions):
        client_socket.send(f"Question {i+1}: {q['question']}\n".encode())
        response = client_socket.recv(1024).decode().strip()
        if response.lower() != q['answer'].lower():
            client_socket.send(b"Mauvaise reponse! Essayez encore!\n")
            client_socket.close()
            return

    client_socket.send(b"Bravo! Voici votre flag: " + flag.encode() + b"\n")
    client_socket.close()

# Set up the server
def start_server():
    host = "0.0.0.0"
    #port = 12345
    port = int(os.getenv("PORT", 12345))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Chat with Santa en ecoute sur le port {port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion recue de {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()"""
