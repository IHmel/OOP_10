import socket
import hashlib
import cryptography
from cryptography.fernet import Fernet
import sqlite3
import os
################################################################
class server():
    def __init__(self):
        self.server = socket.socket()            # создаем объект сокета сервера
        hostname = socket.gethostname()     # получаем имя хоста локальной машины
        port = 12345                        # устанавливаем порт сервера
        self.server.bind((hostname, port))       # привязываем сокет сервера к хосту и порту
        self.server.listen(5)      
        self.connect()

    def data_recv(self,connection):
        data = connection.recv(1024)
        return data.decode()

    def data_send(self,connection,data):
        connection.send(data.encode())
    
    def connect(self):
        print("Server running")
        while True:
            connection, _ = self.server.accept()     # принимаем клиента
            auth = authenticate(connection)
            auth.cons()
            connection.close()  
################################################################
class authenticate(server):
    def __init__(self, connect):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        login TEXT,
                        pswd_hash TEXT
                        )
                        ''')
        con.commit()
        con.close()
        self.connection = connect
        
    def cons(self):
        flag = True
        while flag == True:
            self.data_send(self.connection,str('Выберете опцию из списка'+ '\n1 - Регистрация'+ '\n2 - Вход пользователя'+ '\n0 - Выход из программы'+ '\n'))
            self.data_send(self.connection,str('send'))
            choice = self.data_recv(self.connection)
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.session()
            elif choice == '0':
                self.data_send(self.connection,str('close'))
                flag = False

    def add_user(self):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        check_login = True
        while check_login:
            self.data_send(self.connection,str('Введите Логин:'))
            self.data_send(self.connection,str('send'))
            login = self.data_recv(self.connection)
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            users = cur.fetchall()
            if len(users) == 0:
                check_login = False
            else:
                self.data_send(self.connection,str('Такой логин уже есть'))
        check = False
        while check == False:
            self.data_send(self.connection,str('Введите пароль:'))
            self.data_send(self.connection,str('send'))
            pswrd = self.data_recv(self.connection)
            self.data_send(self.connection,str('Введите пароль еще раз:'))
            self.data_send(self.connection,str('send'))
            pswrd1 = self.data_recv(self.connection)
            if pswrd == pswrd1:
                check = True
                hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
                self.data_send(self.connection,str('Пользователь',login, 'успешно создан!', sep= ' '))
                sql = 'INSERT INTO Users (login, pswd_hash) values(?, ?)'
                data = [login, hash_pswrd]
                cur.execute(sql, data)
                con.commit()
            else:
                self.data_send(self.connection,str('Пароли не совпадают! Попробуйте еще раз'))
        con.close()
            
    def session(self):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        self.data_send(self.connection,str('Введите логин:'))
        self.data_send(self.connection,str('send'))
        login = self.data_recv(self.connection)
        try:
            self.data_send(self.connection,str('Введите пароль:'))
            self.data_send(self.connection,str('send'))
            pswrd = self.data_recv(self.connection)
            hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            data = cur.fetchall()
            con.close()
            if len(data) == 0:
                self.data_send(self.connection,str('Такого пользователя не существует'))
            else:
                hash_pswrd_ch = data[0][0]
                if hash_pswrd_ch == hash_pswrd:
                    self.data_send(self.connection,str('Вы успешно вошли в систему!'))
                    Session = True
                    while(Session == True):
                        Shop = shop(self.connection)
                        self.data_send(self.connection,str('Выберете опцию из списка'+ 
                                        '\n0 - Выход'+
                                        '\n1 - Смена пароля'+ 
                                        '\n2 - Список товаров'+
                                        '\n3 - Добавить товар'+
                                        '\n4 - Корзина'+
                                        '\n5 - Добавить в корзину'+
                                        '\n6 - Оплатить товар\n'))
                        self.data_send(self.connection,str('send'))
                        choice = self.data_recv(self.connection)
                        if choice == '1':
                            self.change_pswd(login)
                        elif choice == '0':
                            Session = False
                        elif choice == '2':
                            Shop.show_product()
                        elif choice == '3':
                            if login == 'admin':
                                Shop.add_product()
                            else:
                                self.data_send(self.connection,str('Недостаточно прав'+'\n'))
                        elif choice == '4':
                            Shop.show_shop_list(login)
                        elif choice == '5':
                            Shop.add_to_shop_list(login)
                        elif choice == '6':
                            Shop.pay(login)
                            
                else:
                    self.data_send(self.connection,str('Неверный пароль'))
        except KeyError:
            self.data_send(self.connection,str('Логин не существует!'))

    def change_pswd(self, login):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        check_pswd = False
        while check_pswd == False:
            self.data_send(self.connection,str('Введите старый пароль:'))
            self.data_send(self.connection,str('send'))
            old_pswrd = self.data_recv(self.connection)
            hash_old_pswrd = hashlib.sha256(bytes(old_pswrd, 'utf-8')).hexdigest()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            data = cur.fetchall()
            hash_pswrd_ch = data[0][0]
            if hash_pswrd_ch == hash_old_pswrd:
                check_pswd = True
                check = False
                while check == False:
                    self.data_send(self.connection,str('Введите пароль:'))
                    self.data_send(self.connection,str('send'))
                    pswrd = self.data_recv(self.connection)
                    self.data_send(self.connection,str('Введите пароль еще раз:'))
                    self.data_send(self.connection,str('send'))
                    pswrd1 = self.data_recv(self.connection)
                    if pswrd == pswrd1:
                        check = True
                        hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
                        cur.execute('UPDATE Users SET pswd_hash = ? WHERE login = ?', (hash_pswrd, login))
                        con.commit()
                        self.data_send(self.connection,str('Для пользователя',login, 'пароль успешно изменен!', sep= ' '))
                    else:
                        self.data_send(self.connection,str('Пароли не совпадают! Попробуйте еще раз'))
            else:
                self.data_send(self.connection,str('Неверный пароль'))
        con.close()

class shop(server):
    def __init__(self, connect):
        self.connection = connect
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Goods (
                        name TEXT,
                        count INTEGER,
                        cost INTEGER
                        )
                        ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS shop_list (
                        user TEXT,
                        name TEXT,
                        count INTEGER,
                        cost INTEGER,
                        oplata TEXT
                        )
                        ''')
        con.commit()
        con.close()
    
    def add_product(self):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        flag = True
        while flag:
            self.data_send(self.connection,str('Введите товар, коллисество и стоимость через пробел: '))
            self.data_send(self.connection,str('send'))
            data = self.data_recv(self.connection).split()
            self.data_send(self.connection,str(data))
            self.data_send(self.connection,str('Добавить товар? (д/н)'+'\n'))
            self.data_send(self.connection,str('send'))
            choice = self.data_recv(self.connection)
            if choice == 'Н' or choice == 'N' or choice == 'n' or choice == 'н':
                self.data_send(self.connection,str('Отменено'))
            else:
                cur.execute('INSERT INTO Goods VALUES (?,?,?)', [str(data[0]), int(data[1]), float(data[2])])
                con.commit()
            self.data_send(self.connection,str('Хотите добавить еще товар? (д/н)'))
            self.data_send(self.connection,str('send'))
            choice1 = self.data_recv(self.connection)
            if choice1 == 'Н' or choice1 == 'N' or choice1 == 'n' or choice1 == 'н':
                flag = False
        con.close()

    def show_product(self): 
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM Goods')
        results = cur.fetchall()
        massage =''
        for row in results:
            for r in row:
                massage = massage + str(r)+' '
            massage = massage +'\n'
        self.data_send(self.connection,str(massage))
    
    def show_shop_list(self, login): 
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        if login == 'admin':
            cur.execute('SELECT * FROM shop_list ORDER BY user')
        else:
            cur.execute('SELECT name, count, cost, oplata FROM shop_list where user = ?', [login])
        results = cur.fetchall()
        massage =''
        for row in results:
            for r in row:
                massage = massage + str(r)+' '
            massage = massage +'\n'
        self.data_send(self.connection,str(massage))
        con.close()
    
    def add_to_shop_list(self, login):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        flag = True
        while flag:
            self.show_product()
            self.data_send(self.connection,str('Введите товар, коллисество для заказа: '))
            self.data_send(self.connection,str('send'))
            data = self.data_recv(self.connection).split()
            name_zakaz = str(data[0]) #name
            kolvo_zakaz = int(data[1]) #kolvo v zakaz
            cur.execute('SELECT * FROM Goods where name =?', (name_zakaz,))
            result = cur.fetchone()
            kolvo = result[1] #kolvo v magazine
            cost = result[2] #cost
            if kolvo >= kolvo_zakaz:
                self.data_send(self.connection,str('Товар добавлен в корзину'))
                if kolvo == kolvo_zakaz:
                    cur.execute('DELETE FROM Goods where name =?', (name_zakaz,))
                else:
                    cur.execute('UPDATE Goods SET count=? where name =?', [kolvo - kolvo_zakaz, name_zakaz])
                cur.execute('SELECT * FROM shop_list WHERE user =? AND name =? AND oplata = ?', [login, name_zakaz, 'Не оплачен'])
                tovar = cur.fetchall()
                #self.data_send(self.connection,str(users)
                if len(tovar) == 0:
                    sql = 'INSERT INTO shop_list (user, name, count, cost, oplata) values(?, ?, ?, ?, ?)'
                    data = [login, name_zakaz, kolvo_zakaz, cost, 'Не оплачен']
                    cur.execute(sql, data)
                else:
                    real_kolvo = tovar[0][2]
                    cur.execute('UPDATE shop_list SET count = ? where name =?', [real_kolvo + kolvo_zakaz, name_zakaz])
                con.commit()
            else:
                self.data_send(self.connection,str('Товара недостаточно на складе'))
            self.data_send(self.connection,str('Хотите добавить в корзину еще товар? (д/н)'))
            self.data_send(self.connection,str('send'))
            choice1 = self.data_recv(self.connection)
            if choice1 == 'Н' or choice1 == 'N' or choice1 == 'n' or choice1 == 'н':
                flag = False
        con.close()

    def pay(self,login):
        con = sqlite3.connect(os.getcwd()+'/OOP_10/Lab3/shop.db')
        cur = con.cursor()
        self.show_shop_list(login)
        self.data_send(self.connection,str('Хотите оплатить товар? (д/н)'))
        self.data_send(self.connection,str('send'))
        choice1 = self.data_recv(self.connection)
        if choice1 == 'Y' or choice1 == 'y' or choice1 == 'Д' or choice1 == 'д':
            cur.execute('UPDATE shop_list SET oplata =?  where user =?', ['Оплачен',login])
            con.commit()
        con.close()

if __name__ == '__main__':
    Server =server()