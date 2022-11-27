def my_sorted2(array): #сортировка по возрастанию(выбором) вроде как с более быстрым алгоритмом - за счет меньшего количества перестановок(за каждый проход перестановка максимум 1)
    for i in range(len(array)):
        idx_min = i
        for j in range(i, len(array)):
            if array[j] < array[idx_min]:
                idx_min = j
        if i != idx_min:
            array[i], array[idx_min] = array[idx_min], array[i]
    return array

def my_sorted(array): #сортировка по возрастанию как-бы написал
    for i in range(len(array)):
        for j in range(i, len(array)):
            if array[j] < array[i]:
                array[i], array[j] = array[j], array[i]
    return array

def number2(array, n, left, right): #Двоичный поиск
    if left > right:
        return "Такого числа нет"
    middle = (right + left) // 2
    if array[middle] >= n and array[middle-1]<n:
        return middle-1
    elif n < array[middle]:

        return number2(array, n, left, middle - 1)
    else:
        return number2(array, n, middle + 1, right)

def number(array, n):   #поиск как бы написал
    i = 0
    if n<=array[0] or n>array[-1]:
        return 'Образец: такого числа нет'
    else:
        while i<len(array) and array[i]<n:
            i+=1
        return i-1


try:
    array  = [int(i) for i in input("Введите последовательность цифр через пробел :").split()]
    n = int(input('Введите число :'))
except ValueError:
    print("Для введения доступны только числа")
else:
    print(array)
    print(my_sorted(array))
    print(my_sorted2(array))
    print(number(my_sorted(array), n))
    print(number2(my_sorted2(array), n, 0, len(array)-1))
