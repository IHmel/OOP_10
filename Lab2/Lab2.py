
import sqlite3;

class Database():

    con = sqlite3.connect("mydb.db")
    
    def console(self):
        flag = True
        while flag:
            choice = input('Выберете действие'+ '\n1 - Добавление'+ '\n2 - Удаление'+ '\n3 - Поиск'+'\n0 - Выход'+'\n')
            if choice == '0':
                flag = False
                
            if choice == '1':
                choice1 = input('1 - Добавление пользователя'+ '\n2 - Добавление структуры'+'\n')
                if choice1 == '1':
                    self.add_user()
                elif choice1 == '2':
                    self.add_structur()
            if choice == '2':
                choice1 = input('1 - Удаление пользователя'+ '\n2 - Удаление структуры'+'\n')
                if choice1 == '1':
                    self.delete_user('1')
                elif choice1 == '2':
                    self.delete_structure('1')
            if choice == '3':
                choice1 = input('1 - Поиск пользователя'+ '\n2 - Показать краткую информацию о всех пользователях'+ '\n3 - Поиск структуры'+ '\n4 - Показать информацию о всех структурах'+'\n')
                if choice1 == '1':
                    self.find_user()
                elif choice1 == '2':
                    self.find_all_users()
                elif choice1 == '3':
                    self.find_structure()
                elif choice1 == '4':
                    self.find_all_structure()

    def __init__(self):
        self.con = sqlite3.connect("mydb.db")
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
        print('Введите СНИЛС нового сотрудника или 0 для отмены: ')
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
                    data[0] = input('Введите ФИО: ')
                if choice == '2':
                    data[1] = input('Введите Год рождения: ')
                if choice == '3':
                    data[2] = input('Введите Должность: ')
                if choice == '4':
                    data[3] = input('Введите Долю ставки: ')
                if choice == '5':
                    data[4] = input('Введите Датy приема: ')
                
    def add_structur(self):
        cur = self.con.cursor()
        print('Введите название новой структуры или 0 для отмены: ')
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
                    data[1] = input('Введите Описание: ')
                if choice == '2':
                    data[2] = input('Введите Штатное расписание: ')
                    
    def find_all_structure(self):
        cur = self.con.cursor()
        print('info')
        cur.execute('SELECT Название, Описание, Штатное расписание FROM Structurs')
        results = cur.fetchall()
        for row in results:
            print(row)
    
    def find_all_users(self):
        cur = self.con.cursor()
        print('info')
        cur.execute('SELECT ФИО, Год рождения, СНИЛС FROM Users')
        results = cur.fetchall()
        for row in results:
            print(row)

    def find_structure(self):
        cur = self.con.cursor()
        print('Введите название струтуры или 0 для отмены: ')
        name = input()
        if name == '0':
            print('Отменено')
        else:
            cur.execute('SELECT * FROM Structurs WHERE Название = ?', (name,))
            results = cur.fetchall()
            row =results[0]
            print(row)
            flag = True
            while flag:
                choice = input('Выберете дальнейшие дествия'+ '\n1 - Удаление данных струтуры'+'\n2 - Изменения данных струтуры'+'\n0 - Для выхода'+'\n')
                if choice == '0':
                    flag = False
                    self.con.commit()
                if choice == '1':
                    self.delete_structure(name)
                    self.con.commit()
                    flag = False
                if choice == '2':
                    self.change_structure(name)
                    self.con.commit()
                    flag = False
        
    def find_user(self):
        cur = self.con.cursor()
        flag = True
        while flag:
            choice1 = input('1 - По ФИО'+ '\n2 - По снилс'+'\n0 - Для отмены'+'\n')
            if choice1 == '0':
                flag = False
                print('Отменено')
            elif choice1 == '2':
                print('Введите СНИЛС сотрудника')
                snils = input()
                cur.execute('SELECT * FROM Users WHERE СНИЛС = ?', (snils,))
                results = cur.fetchall()
                row =results[0]
                print(row)
                self.next(snils)
                flag = False
            elif choice1 == '1':
                print('Введите ФИО сотрудника')
                fio = input()
                cur.execute('SELECT * FROM Users WHERE ФИО = ?', (fio,))
                results = cur.fetchall()
                row =results[0]
                snils=row[5]
                print(row)
                self.next(snils)
                flag = False
                    
    def next(self,snils):
        flag = True
        while flag:
            choice = input('Выберете дальнейшие дествия'+ '\n1 - Удаление данных о пользователе'+'\n2 - Изменения данных о пользователе'+'\n0 - Для выхода'+'\n')
            if choice == '0':
                flag = False
                self.con.commit()
            if choice == '1':
                self.delete_user(snils)
                self.con.commit()
                flag = False
            if choice == '2':
                self.change_user(snils)
                self.con.commit()
                flag = False
                        
    def delete_user(self, snils):
        cur = self.con.cursor()
        if snils == '1':
            print('Введите СНИЛС сотрудника или 0 для отмены')
            snils = input()
        if snils == '0':
            print('Отменено')
        else:
            cur.execute('DELETE FROM Users WHERE СНИЛС =?', (snils,))
            self.con.commit()
        
    def delete_structure(self, name):
        cur = self.con.cursor()
        if name == '1':
            print('Введите название структуры или 0 для отмены')
            name = input()
        if name == '0':
            print('Отменено')
        else:
            cur.execute('DELETE FROM Structurs WHERE Название =?', (name,))
            self.con.commit()
                
    def change_structure(self, name):
        cur= self.con.cursor()
        if name == '0':
            print('Введите название новой структуры или 0 для отмены: ')
            name = input()
        if name == '0':
            print('Отменено')
        else:
            cur.execute('SELECT * FROM Structurs WHERE Название =?', (name,))
            rows = cur.fetchall()
            results = rows[0]
            #print(rows)
            data = [results[0], results[1], results[2]]
            self.delete_structure(name)
            #print(data)
            flag = True
            while flag:
                print(data)
                choice = input('Выберете данные для изменения'+ '\n1 - Описание'+ '\n2 - Штатное расписание'+'\n0 - Для сохранения'+'\n')
                if choice == '0':
                    flag = False
                    cur.execute('INSERT INTO Structurs VALUES (?,?,?)', data)
                    self.con.commit()
                if choice == '1':
                    data[1] = input('Введите Описание: ')
                if choice == '2':
                    data[2] = input('Введите Штатное расписание: ')
                    
    def change_user(self, snils):
        cur = self.con.cursor()
        if snils == '0':
            print('Введите СНИЛС нового сотрудника или 0 для отмены: ')
            snils = input()
        if snils == '0':
            print('Отменено')
        else:
            cur.execute('SELECT * FROM Users WHERE СНИЛС = ?', (snils,))
            rows = cur.fetchall()
            results = rows[0]
            #print(rows)
            data = [results[0], results[1], results[2], results[3], results[4], results[5]]
            self.delete_user(snils)
            #print(data)
            flag = True
            while flag:
                print(data)
                choice = input('Выберете данные для изменения'+ '\n1 - ФИО'+ '\n2 - Год рождения'+ '\n3 - Должность'+'\n4 - Доля ставки'+ '\n5 - Дата приема'+'\n0 - Для сохранения'+'\n')
                if choice == '0':
                    flag = False
                    cur.execute('INSERT INTO Users VALUES (?,?,?,?,?,?)', data)
                    self.con.commit()
                if choice == '1':
                    data[0] = input('Введите ФИО: ')
                if choice == '2':
                    data[1] = input('Введите Год рождения: ')
                if choice == '3':
                    data[2] = input('Введите Должность: ')
                if choice == '4':
                    data[3] = input('Введите Долю ставки: ')
                if choice == '5':
                    data[4] = input('Введите Датe приема: ')
                    
if __name__ == '__main__':
    db = Database()
    db.console()