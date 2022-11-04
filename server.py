import socket
# import sys

def recibir ():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    server_address = ('localhost', 10000)
    print('conectando...')
    sock.bind(server_address)

    
    sock.listen()

    while True:

        print('esperando conexion...')
        connection, client_address = sock.accept()
        try:
            print('conexion de', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(50)
                print(data.decode())
                if data:
                    print('devolviendo datos')
                    connection.sendall(data)
                else:
                    break

        finally:
            connection.close()
        break
    return 0
