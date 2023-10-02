
import sqlite3;

class Database():

    con = sqlite3.connect("mydb.db")
    
    def __init__(self):
        self.con = sqlite3.connect("metanit.db")
        cur = self.con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        ФИО TEXT,
                        Год рождения INTEGER,
                        Должность TEXT, 
                        Доля ставки REAL,
                        Дата приема TEXt,
                        СНИЛС TEXT NOT NULL
                        )
                        ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Structurs (
                        Название TEXT NOT NULL,
                        Описание TEXT,
                        Штатное расписание TEXT
                        )
                        ''')
        self.con.commit()

    def add_user(self):
        cur = self.con.cursor()
        print('Введите СНИЛС нового сотрудника или 0 для отмены')
        snils = input()
        if snils == '0':
            print('Отменено')
        else:
            data = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', snils]
            flag = True
            while flag:
                choice = input('Выберете данные для ввода'+ '\n1 - ФИО'+ '\n2 - Год рождения'+ '\n3 - Должность'+'\n4 - Доля ставки'+ '\n5 - Дата приема'+'\n0 - Для сохранения'+'\n')
                if choice == '0':
                    flag = False
                    cur.execute('INSERT INTO Users VALUES (?,?,?,?,?,?)', data)
                    self.con.commit()
                if choice == '1':
                    data[0] = input('Введите ФИО')
                if choice == '2':
                    data[1] = input('Введите Год рождения')
                if choice == '3':
                    data[2] = input('Введите Должность')
                if choice == '4':
                    data[3] = input('Введите Долю ставки')
                if choice == '5':
                    data[4] = input('Введите Датy приема')
                
    def add_structur(self):
        cur = self.con.cursor()
        print('Введите название новой структуры или 0 для отмены')
        name = input()
        if name == '0':
            print('Отменено')
        else:
            data = [name, 'NULL', 'NULL']
            flag = True
            while flag:
                choice = input('Выберете данные для ввода'+ '\n1 - Описание'+'\n2 - Штатное расписание'+'\n0 - Для сохранения'+'\n')
                if choice == '0':
                    flag = False
                    cur.execute('INSERT INTO Structurs VALUES (?,?,?)', data)
                    self.con.commit()
                if choice == '1':
                    data[1] = input('Введите Описание')
                if choice == '2':
                    data[2] = input('Введите Штатное расписание')
                    
    def find_user(self):
        cur = self.con.cursor()
        print('Введите СНИЛС нового сотрудника или 0 для отмены')
        snils = input()
        if snils == '0':
            print('Отменено')
        else:
            cur.execute('SELECT СНИЛС WHERE СНИЛС = ?', (snils))
            results = cur.fetchall()
            for row in results:
                print(row)
            while flag:
                choice = input('Выберете дальнейшие дествия'+ '\n1 - Удаление данных о пользователе'+'\n2 - Изменения данных о пользователе'+'\n0 - Для выхода'+'\n')
                if choice == '0':
                    flag = False
                    self.con.commit()
                if choice == '1':
                    self.con.commit()
                    self.delete_user(snils)
                    flag = False
                if choice == '2':
                    self.con.commit()
                    self.change_user(snils)
                    flag = False

    def delete_user(self, snils):
        cur = self.con.cursor()
        if snils == '0':
            print('Введите СНИЛС нового сотрудника или 0 для отмены')
            snils = input()
        if snils == '0':
            print('Отменено')
        else:
            cur.execute('DELETE FROM Users WHERE СНИЛС =?', (snils))
            self.con.commit()
        
    def change_user(self, snils):
        cur = self.con.cursor()
        if snils == '0':
            print('Введите СНИЛС нового сотрудника или 0 для отмены')
            snils = input()
        if snils == '0':
            print('Отменено')
        else:
            data = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', snils]
            flag = True
            while flag:
                choice = input('Выберете данные для изменения'+ '\n1 - ФИО'+ '\n2 - Год рождения'+ '\n3 - Должность'+'\n4 - Доля ставки'+ '\n5 - Дата приема'+'\n0 - Для сохранения'+'\n')
                if choice == '0':
                    flag = False
                    cur.execute('INSERT INTO Users VALUES (?,?,?,?,?,?)', data)
                    self.con.commit()
                if choice == '1':
                    data[0] = input('Введите ФИО')
                if choice == '2':
                    data[1] = input('Введите Год рождения')
                if choice == '3':
                    data[2] = input('Введите Должность')
                if choice == '4':
                    data[3] = input('Введите Долю ставки')
                if choice == '5':
                    data[4] = input('Введите Датe приема')