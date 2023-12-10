import socket

class client():
    def __init__(self):
        self.client = socket.socket()            # создаем сокет клиента
        hostname = socket.gethostname()     # получаем хост локальной машины
        port = 12345                        # устанавливаем порт сервера
        self.client.connect((hostname, port))
        self.start()
    
    def start(self):
        while True:
            data = self.client.recv(1024)  
            #print('data=', data)
            print("Server sent: \n", data.decode())
            if data == b'Closing connection':
                break 
            self.client.send(input().encode())          
        self.client.close()

if __name__ == "__main__":
    Client = client()