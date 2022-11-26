class Client:
    def __init__(self, name, surname, city, balance):
        self.name = name
        self.surname = surname
        self.city = city
        self.balance = balance
    def __str__(self):
        return f'{self.name} {self.surname}. {self.city}. Баланс: {self.balance} руб.'

    def fio(self):
        return f'{self.name} {self.surname} г.{self.city}'
k1 = Client('Петя', 'Иванов', 'Новосибирск', 50)
k2 = Client('Петsdfsя', 'Ивsdfsdfанов', 'Новосибирsdfsdск', 500)
k3 = Client('Пя', 'Ив', 'Нк', 5)


spisok = [k1,k2,k3]
for el in spisok:
    print(el.fio())
