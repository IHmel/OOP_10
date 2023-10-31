import hashlib
import cryptography
from cryptography.fernet import Fernet
import sqlite3
import os


class authenticate:
    def __init__(self):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        login TEXT,
                        pswd_hash TEXT
                        )
                        ''')
        con.commit()
        con.close()
        
    def cons(self):
        flag = True
        while flag == True:
            choice = input('Выберете опцию из списка'+ '\n1 - Регистрация'+ '\n2 - Вход пользователя'+ '\n0 - Выход из программы'+ '\n')
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.session()
            elif choice == '0':
                flag = False

    def add_user(self):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        check_login = True
        while check_login:
            print('Введите Логин:')
            login = input()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            users = cur.fetchall()
            #print(users)
            if len(users) == 0:
                check_login = False
            else:
                print('Такой логин уже есть')
        check = False
        while check == False:
            print('Введите пароль:')
            pswrd = input()
            print('Введите пароль еще раз:')
            pswrd1 = input()
            if pswrd == pswrd1:
                check = True
                hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
                print('Пользователь',login, 'успешно создан!', sep= ' ')
                sql = 'INSERT INTO Users (login, pswd_hash) values(?, ?)'
                data = [login, hash_pswrd]
                cur.execute(sql, data)
                con.commit()
            else:
                print('Пароли не совпадают! Попробуйте еще раз')
        con.close()
            
    def session(self):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        print('Введите логин:')
        login = input()
        try:
            print('Введите пароль:')
            pswrd = input()
            hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            data = cur.fetchall()
            con.close()
            if len(data) == 0:
                print('Такого пользователя не существует')
            else:
                hash_pswrd_ch = data[0][0]
                if hash_pswrd_ch == hash_pswrd:
                    print('Вы успешно вошли в систему!')
                    Session = True
                    while(Session == True):
                        Shop = shop()
                        choice = input('Выберете опцию из списка'+ 
                                        '\n0 - Выход'+
                                        '\n1 - Смена пароля'+ 
                                        '\n2 - Список товаров'+
                                        '\n3 - Добавить товар'+
                                        '\n4 - Корзина'+
                                        '\n5 - Добавить в корзину'+
                                        '\n6 - Оплатить товар\n')
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
                                print('Недостаточно прав'+'\n')
                        elif choice == '4':
                            Shop.show_shop_list(login)
                        elif choice == '5':
                            Shop.add_to_shop_list(login)
                        elif choice == '6':
                            Shop.pay(login)
                            
                else:
                    print('Неверный пароль')
        except KeyError:
            print('Логин не существует!')

    def change_pswd(self, login):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        check_pswd = False
        while check_pswd == False:
            print('Введите старый пароль:')
            old_pswrd = input()
            hash_old_pswrd = hashlib.sha256(bytes(old_pswrd, 'utf-8')).hexdigest()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            data = cur.fetchall()
            hash_pswrd_ch = data[0][0]
            if hash_pswrd_ch == hash_old_pswrd:
                check_pswd = True
                check = False
                while check == False:
                    print('Введите пароль:')
                    pswrd = input()
                    print('Введите пароль еще раз:')
                    pswrd1 = input()
                    if pswrd == pswrd1:
                        check = True
                        hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
                        cur.execute('UPDATE Users SET pswd_hash = ? WHERE login = ?', (hash_pswrd, login))
                        con.commit()
                        print('Для пользователя',login, 'пароль успешно изменен!', sep= ' ')
                    else:
                        print('Пароли не совпадают! Попробуйте еще раз')
            else:
                print('Неверный пароль')
        con.close()

class shop:
    def __init__(self):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
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
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        flag = True
        while flag:
            print('Введите товар, коллисество и стоимость через пробел: ')
            data = input().split()
            print(data)
            choice = input('Добавить товар? (д/н)'+'\n')
            if choice == 'Н' or choice == 'N' or choice == 'n' or choice == 'н':
                print('Отменено')
            else:
                cur.execute('INSERT INTO Goods VALUES (?,?,?)', [str(data[0]), int(data[1]), float(data[2])])
                con.commit()
            choice1 = input('Хотите добавить еще товар? (д/н)')
            if choice1 == 'Н' or choice1 == 'N' or choice1 == 'n' or choice1 == 'н':
                flag = False
        con.close()

    def show_product(self): 
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM Goods')
        results = cur.fetchall()
        for row in results:
            print(*row)
    
    def show_shop_list(self, login): 
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        if login == 'admin':
            cur.execute('SELECT * FROM shop_list ORDER BY user')
        else:
            cur.execute('SELECT name, count, cost, oplata FROM shop_list where user = ?', [login])
        results = cur.fetchall()
        for row in results:
            print(*row)
        con.close()
    
    def add_to_shop_list(self, login):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        flag = True
        while flag:
            self.show_product()
            print('Введите товар, коллисество для заказа: ')
            data = input().split()
            name_zakaz = str(data[0]) #name
            #print(data[0], type(data[0]))
            kolvo_zakaz = int(data[1]) #kolvo v zakaz
            cur.execute('SELECT * FROM Goods where name =?', (name_zakaz,))
            result = cur.fetchone()
            kolvo = result[1] #kolvo v magazine
            cost = result[2] #cost
            if kolvo >= kolvo_zakaz:
                print('Товар добавлен в корзину')
                if kolvo == kolvo_zakaz:
                    cur.execute('DELETE FROM Goods where name =?', (name_zakaz,))
                else:
                    cur.execute('UPDATE Goods SET count=? where name =?', [kolvo - kolvo_zakaz, name_zakaz])
                cur.execute('SELECT * FROM shop_list WHERE user =? AND name =? AND oplata = ?', [login, name_zakaz, 'Не оплачен'])
                tovar = cur.fetchall()
                #print(users)
                if len(tovar) == 0:
                    sql = 'INSERT INTO shop_list (user, name, count, cost, oplata) values(?, ?, ?, ?, ?)'
                    data = [login, name_zakaz, kolvo_zakaz, cost, 'Не оплачен']
                    cur.execute(sql, data)
                else:
                    real_kolvo = tovar[0][2]
                    cur.execute('UPDATE shop_list SET count = ? where name =?', [real_kolvo + kolvo_zakaz, name_zakaz])
                con.commit()
            else:
                print('Товара недостаточно на складе')
            choice1 = input('Хотите добавить в корзину еще товар? (д/н)')
            if choice1 == 'Н' or choice1 == 'N' or choice1 == 'n' or choice1 == 'н':
                flag = False
        con.close()

    def pay(self,login):
        con = sqlite3.connect(os.getcwd()+'/Lab3/shop.db')
        cur = con.cursor()
        self.show_shop_list(login)
        choice1 = input('Хотите оплатить товар? (д/н)')
        if choice1 == 'Y' or choice1 == 'y' or choice1 == 'Д' or choice1 == 'д':
            cur.execute('UPDATE shop_list SET oplata =?  where user =?', ['Оплачен',login])
            con.commit()
        con.close()
        

if __name__ == '__main__':
    Cons = authenticate()
    Cons.cons()

