import socket
from tkinter import *
import pygame
import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
pygame.mixer.init()


def run():
    text = "run"
    pacote = text.encode()
    socketNormal.send(pacote)


def transformador_registro(registro):
    if registro < 10:
        registro = "00" + str(registro)
    elif registro < 100:
        registro = "0" + str(registro)
    else:
        registro = str(registro)
    return registro


socketNormal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '127.0.0.1'
porta = 50000
destino = (ip, porta)

socketNormal.connect(destino)

encerrado = False

tentativas = int.from_bytes(socketNormal.recv(2), 'big')
registro = int.from_bytes(socketNormal.recv(3), 'big')
tamNome = int.from_bytes(socketNormal.recv(2), 'big')
tamCap = int.from_bytes(socketNormal.recv(10), 'big')
nome = socketNormal.recv(tamNome).decode()
capturado = socketNormal.recv(tamCap).decode()


def captura():
    text = "cap"
    pacote = text.encode()
    socketNormal.send(pacote)

    tentativas = int.from_bytes(socketNormal.recv(2), 'big')
    registro = int.from_bytes(socketNormal.recv(3), 'big')
    tamNome = int.from_bytes(socketNormal.recv(2), 'big')
    tamCap = int.from_bytes(socketNormal.recv(10), 'big')
    nome = socketNormal.recv(tamNome).decode()
    capturado = socketNormal.recv(tamCap).decode()

    if capturado == "cap":
        title_label.config(text=f"Pokémon capturado.")
        texto.config(text=f"Ainda restaram {tentativas} pokébolas.")
        socketNormal.close()
    else:
        texto.config(text=f"O Pokémon escapou. Você ainda possui {tentativas} pokébolas.")

    if tentativas == 0 and capturado != "cap":
        texto.config(text=f"O Pokémon fugiu. Você não possui mais pokébolas.")
        socketNormal.close()


# UI SETUP

window = Tk()
window.title("Pokémon Capture Game")
window.config(bg='white')

title_label = Label(text=f"Um {nome} selvagem apareceu!", font=("Verdana", 20, "bold"), bg="white")
title_label.grid(column=0, row=1, columnspan=2)

texto = Label(text=f"Você possui {tentativas} pokébolas.", font=("Verdana", 10, "bold"), bg="white")
texto.grid(column=0, row=2, columnspan=2)

canvas = Canvas(width=600, height=300, highlightthickness=0, bg="#fff")
pokemon_img = PhotoImage(file=f"images/{registro}.png")
canvas.create_image(300, 150, image=pokemon_img)
canvas.grid(column=0, row=0, columnspan=2)

capture_button = Button(text="Capturar", highlightthickness=0, command=captura, width=20, height=3)
capture_button.grid(column=0, row=3, pady=20)

run_button = Button(text="Fugir", highlightthickness=0, command=run, width=20, height=3)
run_button.grid(column=1, row=3, pady=20)

numero_audio = transformador_registro(registro)
snd = pygame.mixer.Sound(f"sounds/{numero_audio}.wav")
pygame.mixer.Sound.play(snd)

window.mainloop()

socketNormal.close()
