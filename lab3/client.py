import socket
import select
import sys

HEADER_LENGTH = 10

# IP i PORT serwera
IP = "127.0.0.1"
PORT = 1111

# pobieramy od użytkownika username
my_username = input("Username: ")

# Stworzenie socketa
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Łączymy się z podanym IP i PORTem
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# nadajemy header i username 
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    # lista możliwych źródeł danych - terminal i socket
    sockets_list = [sys.stdin, client_socket]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for sockets in read_sockets:
        # jeżeli otrzymaliśmy dane na socket
        if sockets == client_socket:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                # wypisujemy informacje o tym na konsolę 
                sys.stdout.write('Connection closed by the server')
                sys.stdout.flush()

                # kończymy program
                sys.exit()
            # pobieramy username nadawcy
            username = client_socket.recv(int(username_header.decode('utf-8').strip())).decode('utf-8')
            # odbieramy header wiadomości (ten określonej długości)
            message_header = client_socket.recv(HEADER_LENGTH)
            # pobieramy treść wiadomości
            message = client_socket.recv(int(message_header.decode('utf-8').strip())).decode('utf-8')

            # Wypisujemy wiadomość na chacie
            sys.stdout.write(f'\r{username}: {message}\n')
            sys.stdout.flush()
        else:
            # zczytujemy wiadomość z terminala 
            message = sys.stdin.readline().rstrip()
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            sys.stdout.write('\033[F')
            sys.stdout.write(f'{my_username}: ')
            sys.stdout.write(message.decode('utf-8') + '\n')
            sys.stdout.flush()