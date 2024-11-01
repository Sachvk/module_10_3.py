import threading
import random
from time import sleep
from threading import Lock


class Bank:
    def __init__(self):
        threading.Thread.__init__(self)
        self.balance = int(0)
        self.lock = Lock()

    def deposit(self):
        for i in range(10):
            number = random.randrange(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            else:
                self.balance = self.balance + number
                print(f'Пополнение: {number}. Баланс: {self.balance}.')
                sleep(0.001)

    def take(self):
        for i in range(10):
            number = random.randrange(50, 500)
            print(f'Запрос на {number}')
            if number <= self.balance and self.lock.locked():
                self.balance = self.balance - number
                print(f'Снятие: {number}. Баланс: {self.balance}.')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
                sleep(0.001)

    def run(self):
        self.deposit()
        self.take()


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
