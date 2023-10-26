import hashlib
import cryptography
from cryptography.fernet import Fernet
import sqlite3;

################################################################

#Класс движка

class authenticate:
    def __init__(self):
        con = sqlite3.connect('OOP_10/Lab3/shop.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        login TEXT,
                        pswd_hash TEXT
                        )
                        ''')
        con.commit()
        
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
        con = sqlite3.connect('OOP_10/Lab3/shop.db')
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
            
    def session(self):
        con = sqlite3.connect('OOP_10/Lab3/shop.db')
        cur = con.cursor()
        print('Введите логин:')
        login = input()
        try:
            print('Введите пароль:')
            pswrd = input()
            hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
            cur.execute('SELECT pswd_hash FROM Users WHERE login =? ', (login,))
            data = cur.fetchall()
            hash_pswrd_ch = data[0][0]
            if hash_pswrd_ch == hash_pswrd:
                print('Вы успешно вошли в систему!')
                Session = True
                while(Session == True):
                    choice = input('Выберете опцию из списка'+ '\n1 - Смена пароля'+ '\n2 - Выход'+ '\n')
                    if choice == '1':
                        self.change_pswd(login)
                    elif choice == '2':
                        Session = False
            else:
                print('Неверный пароль')
        except KeyError:
            print('Логин не существует!')


    def change_pswd(self, login):
        con = sqlite3.connect('OOP_10/Lab3/shop.db')
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
                        print('Для пользователя',login, 'пароль успешно изменен!', sep= ' ')
                    else:
                        print('Пароли не совпадают! Попробуйте еще раз')
            else:
                print('Неверный пароль')


if __name__ == '__main__':
    Cons = authenticate()
    Cons.cons()

