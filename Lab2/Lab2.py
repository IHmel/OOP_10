import hashlib
import cryptography
from cryptography.fernet import Fernet
################################################################
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
#Класс движка

class console:
    
    user_list = {}
    key = str
    def read_file(self):
        self.key = open('key.key', 'rb').read()
        with open('users.txt') as file: #Читаем файл
            lines = file.read().splitlines() # read().splitlines()
        for line in lines: # Проходимся по каждой строчке
            key,value = line.split(' ') 
            self.user_list.update({key:value})	 # Добавляем в словарь

    def write_file(self):
        with open('users.txt','w') as out:
            for key,val in self.user_list.items():
                out.write('{} {}\n'.format(key,val))
    
    def add_user(self):
        print('Введите Логин:')
        login = input()
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
                self.user_list.update({login:hash_pswrd})
                self.write_file()
            else:
                print('Пароли не совпадают! Попробуйте еще раз')
            
    def session(self):
        print('Введите логин:')
        login = input()
        try:
            hash_pswrd_ch = self.user_list[login]
            print('Введите пароль:')
            pswrd = input()
            hash_pswrd = hashlib.sha256(bytes(pswrd, 'utf-8')).hexdigest()
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
        check_pswd = False
        while check_pswd == False:
            print('Введите старый пароль:')
            old_pswrd = input()
            hash_old_pswrd = hashlib.sha256(bytes(old_pswrd, 'utf-8')).hexdigest()
            hash_pswrd_ch = self.user_list[login]
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
                        self.user_list.update({login:hash_pswrd})
                        self.write_file()
                        print('Для пользователя',login, 'пароль успешно изменен!', sep= ' ')
                    else:
                        print('Пароли не совпадают! Попробуйте еще раз')
            else:
                print('Неверный пароль')


if __name__ == '__main__':
    #generate_key()
    Cons = console()
    Cons.read_file()
    while(True):
        choice = input('Выберете опцию из списка'+ '\n1 - Регистрация'+ '\n2 - Вход пользователя'+ '\n3 - Выход из программы'+ '\n')
        if choice == '1':
            Cons.add_user()
        elif choice == '2':
            Cons.session()
        elif choice == '3':
            login = input('Введите логин:')
        elif choice == '4':
            print(Cons.user_list)

