import socket


def enviar(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server, addr = ('localhost', 10000)
    print('conectando a ', server)
    sock.connect((server, addr))

    try:
        print('enviando... ')
        sock.send(message.encode())

        amount_received = 0
        amount_expected = len(message)

    #    while amount_received < amount_expected:
        data = sock.recv(50).decode()
    #        amount_received += len(data)
        print(data)

    finally:
        print('cierre conexion')
        sock.close()

    return 0