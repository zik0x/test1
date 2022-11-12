per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
deposit=[]
s = int(input('Введите сумму вклада(в рублях):'))
print('Доход по депозиту в каждом из банков:')
for key in per_cent:
    deposit.append(per_cent[key]*s/100) #это по заданию
    print(key, ':', per_cent[key]*s/100, end=' ')
print()
#print(deposit) #это по заданию
print('Максимальная сумма, которую вы можете заработать —', max(deposit), 'руб.')