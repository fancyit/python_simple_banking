from random import random, randint
import sqlite3

class Utils:
    conn = sqlite3.connect('card.s3db', check_same_thread=False)
    cur = conn.cursor()

    # check if AccountNumber in the fetched cards
    def check_acc(self, num):
        self.cur.execute(f"""
                    select * from card
                    where number like '%{str(num)}%' 
                """)
        count = self.cur.fetchall()
        return True if len(count) > 0 else False


    # Рассчитываем чексумму, удовлетворяющую алгоритму Луна
    def calcCheckSum(self, accNum):
        sum = 8
        for i in range(0, len(accNum)):
            tmp = int(accNum[i])
            if i % 2 == 0:
                tmp *= 2
                if tmp > 9:
                    tmp -= 9
            sum += tmp
        if sum % 10 == 0:
           checkSum = 0
        else:
           checkSum = (((sum // 10) +1) * 10) - sum
        # checkSum = (sum * 9) % 10
        return checkSum


    # Проверка номера карты алг-м Луна
    def luhn_check(self, card_num):
        sum = 8
        for i in range(6, len(card_num) - 1):
            tmp = int(card_num[i])
            if i % 2 == 0:
                tmp *= 2
                if tmp > 9:
                    tmp -= 9
            sum += tmp
        if sum % 10 == 0:
            checkSum = 0
        else:
            checkSum = (((sum // 10) +1) * 10) - sum
        # checkSum = (sum * 9) % 10
        return (checkSum == int(card_num[-1]))

    # Генерируем номер карты
    def GenerateAccountNumber(self):
        prefix = 400000
        accNum = randint(100000000, 999999999)
        while self.check_acc(accNum):
            accNum = randint(100000000, 999999999)
        checkSum = self.calcCheckSum(str(accNum))
        return (str(prefix) + str(accNum) + str(checkSum))

    # Генерирум пинкод
    def GeneratePIN(self):
        pin = randint(1000, 9999)
        return pin

    def Sql_Insert(self, table, columns, values):
        text = (f"INSERT INTO {table} ({columns}) values ({values})")
        return text


    def Sql_Select(self, what, table, where):
        text = "select "
        if what is not None:
            text += (what + " from " + table)
        if where is not None:
            text += " where " + where
        return text
