def count(array, element):
    count = 0
    for el in array:
        if el == element:
            count+=1
    return count

array = [int(i) for i in input().split()]
element = int(input())

print(count(array, element))