def characterReplacement(text):   #функция убирает спецсимолы
    for el in '!.,':
        text = text.replace(el, "")
    return text

def frequentWord(text, dlinna):  # функция выводит слова больше определенного размера
    text=text.split()
    maxCount= 0
    sMaxCount=[]
    for el in text:
        count = text.count(el)
        if len(el)>dlinna and count>maxCount:
            sMaxCount = []
            maxCount=count
            sMaxCount.append(el)
        elif len(el)>dlinna and count==maxCount:
            sMaxCount.append(el)
    return ' '.join(set(sMaxCount))

def englishWord(text): # функция ищет список самых длинных словна английском
    text = text.split()
    maxLen=0
    sMaxLen=[]
    for el in text:
        if 65<=ord(el[0])<=90 or 97<=ord(el[0])<=122:
            if len(el)>maxLen:
                maxLen=len(el)
                sMaxLen.append(el)
            elif len(el)==maxLen:
                sMaxLen.append(el)
    return ' '.join(set(sMaxLen))


n = input('Введите название файла: ')
with open(n) as f:
    Filetext = f.read()
Filetext=characterReplacement(Filetext)
print('Список слов больше 3-х букв: ', frequentWord(Filetext, 3))
print('Список самых длинных английский слов: ', englishWord(Filetext))