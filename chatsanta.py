import socket
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
    start_server()