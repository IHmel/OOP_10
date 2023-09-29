
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

    def add_struct(self):
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
                