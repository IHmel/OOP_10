import socket
 
client = socket.socket()            # создаем сокет клиента
hostname = socket.gethostname()     # получаем хост локальной машины
port = 12345                        # устанавливаем порт сервера
client.connect((hostname, port))    # подключаемся к серверу
data = client.recv(1024)            # получаем данные с сервера
print("Server sent: ", data.decode()) 
#client.send(message.encode())       # отправляем сообщение серверу

client.close()                      # закрываем подключение