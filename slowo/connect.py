import socket

class Connect:
    __buffer = 1024
    __socc = socket.socket

    def __init__(self, address, port) -> None:
        self.address = address
        self.socc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socc.connect((address, port))
        print("Connected to server")

    @property
    def buffer(self) -> int:
        return self.__buffer
                                      
    @property
    def socc(self) -> socket.socket:
        return self.__socc

    @socc.setter
    def socc(self, socc: socket.socket):
        self.__socc = socc

    def auth(self, login: str, password: str):
        login += '\n'
        password += '\n'
        try:
            if self.address == "146.59.45.35":
                self.socc.sendall(f'{login}{password}\0'.encode())
            else:
                self.socc.send(login.encode())
                self.socc.send(password.encode())

            response = self.receive()
            if response[0] == '-':
                print(f'Authentication failed!')
                return 0
            
            elif response[0] == '+':
                print('Authentication succesfull!')
                return int(response[1])
        except:
            print('Authentication error!')
            return 0

    def send(self, message: str):
        try:
            self.socc.send(message.encode())
            return True
        except:
            print(f'Error when sending message: {message.encode()}')
            return False

    def receive(self) -> str | bool:
        try:
            while True:
                line = self.socc.recv(self.buffer, socket.MSG_PEEK)
                #print(f'Received buffer: "{line}"')
                eol = line.find(b'\n')
                if eol >= 0:
                    size = eol + 1
                else:
                    size = self.buffer
                res = self.socc.recv(size).decode().rstrip("\n\r\0")
                if res != '':
                    return res
        except:
            print(f'Error when receiving message, dropping socket...')
            return False

    def __del__(self):
        if self.socc:
            self.socc.shutdown(socket.SHUT_RDWR)
            self.socc.close()

