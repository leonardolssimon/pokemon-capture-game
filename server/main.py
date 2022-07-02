import random as random
import pandas as pd
import socket

socketEscuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '127.0.0.1'
porta = 50000
origem = (ip, porta)

socketEscuta.bind(origem)
socketEscuta.listen(1)

[socketDados, infoCliente] = socketEscuta.accept()

pokedex = pd.read_csv("pokemon.csv")

firstGeneration = pokedex.head(149)

names = firstGeneration["name"].tolist()
captureRate = firstGeneration["capture_rate"].tolist()


def game():
    message = "nao"
    appeared = random.choice(names)

    if appeared in names:
        registro = names.index(appeared) + 1

    appeared_cap_rate = int(captureRate[registro - 1])

    # message = f"A wild {appeared} appeared. Capture or Run?"
    # print(message)

    tentativas = 10
    pacote = tentativas.to_bytes(2, 'big') + registro.to_bytes(3, 'big') + len(appeared).to_bytes(2, 'big') + len(
        message).to_bytes(10, 'big') + appeared.encode() + message.encode()
    socketDados.send(pacote)
    while tentativas > 0:

        letraByte = socketDados.recv(3)

        letra = letraByte.decode()

        if letra == "cap":
            catch = random.randint(0, 580)
            if catch <= appeared_cap_rate:
                message = "cap"
                tentativas -= 1
                pacote = tentativas.to_bytes(2, 'big') + registro.to_bytes(3, 'big') + len(appeared).to_bytes(2,
                                                                                                              'big') + len(
                    message).to_bytes(10, 'big') + appeared.encode() + message.encode()
                socketDados.send(pacote)
            else:
                message = "nao"
                tentativas -= 1
                pacote = tentativas.to_bytes(2, 'big') + registro.to_bytes(3, 'big') + len(appeared).to_bytes(2,
                                                                                                              'big') + len(
                    message).to_bytes(10, 'big') + appeared.encode() + message.encode()
                socketDados.send(pacote)
        else:
            break


game()

socketDados.close()
socketEscuta.close()
