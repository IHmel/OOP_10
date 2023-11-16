import socket

class client():
    def __init__(self):
        self.client = socket.socket()            # создаем сокет клиента
        hostname = socket.gethostname()     # получаем хост локальной машины
        port = 12345                        # устанавливаем порт сервера
        self.client.connect((hostname, port))
        self.run_client()
    
    def run_client(self):
        flag = True
        while flag:
            data = self.client.recv(1024**2)
            if data.decode()=='send': 
                self.client.send(input().encode())
            elif data.decode()=='close':
                self.client.close()    
            elif data.decode()!=None:
                print("Server sent:\n", data.decode()) 

if __name__ == '__main__':
    Client=client()