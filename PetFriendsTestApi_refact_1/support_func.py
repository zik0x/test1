def generate_string(n): #функция для генерации n символов
   return "x" * n

def russian_chars(): #функция русских символов
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars(): #функция китайских символов
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():  #функция спецсиволов
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

def is_age_valid(age): # Проверяем, что возраст - это число от 1 до 49 и целое
    if age.isdigit() and 0 < int(age) < 50 and float(age) == int(age):
        return False
    else:
        return True
