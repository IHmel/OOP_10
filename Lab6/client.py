import socket

class client():
    def __init__(self):
        self.client = socket.socket()            # создаем сокет клиента
        hostname = socket.gethostname()     # получаем хост локальной машины
        port = 12345                        # устанавливаем порт сервера
        self.client.connect((hostname, port))
while True:
    data = client.recv(1024**2)  
    print("Server sent: ", data.decode()) 
    client.send(input().encode())          
client.close()                      # закрываем подключение