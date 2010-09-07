import json

def presenceOfFields(json): # проверяет все ли поля есть
    i=0
    spisok = []
    for el in json:
        i+=1
        s = []
        for key in sample.keys():
            if key not in el.keys():
                s.append(key)
        if s:
            spisok.append(('обьект '+ str(i), ' отсутствуют поля: ',*s, '\n'))
    if spisok:
        stroka=' '
        for el in spisok:
            for val in el:
                stroka+=val+' '
        return stroka
    else:
        return 'все поля содержаться'

def extraFields(json): #проверяет есть ли лишние поля
    spisok=[]
    i=0
    for el in json:
        s = []
        i+=1
        for key in el.keys():
            if key not in sample.keys():
                s.append(key)
        if s:
            spisok.append(('обьект '+ str(i), 'лишнее поле: ',*s, '\n'))
    if spisok:
        stroka = ' '
        for el in spisok:
            for val in el:
                stroka += val + ' '
        return stroka
    else:
        return 'лишних нет'

def typeChecking(json): #проверка типа
    spisok=[]
    i=0
    for object in json:
        i+=1
        s = []
        for key in object.keys():
            if sample[key] == 'int':
                if not isinstance(object[key], int):
                    s.append(key)
            if sample[key] == 'string':
                if not isinstance(object[key], str):
                    s.append(key)
            if sample[key] == 'bool':
                if not isinstance(object[key], bool):
                    s.append(key)
            if sample[key] == 'string (url)':
                if not('https://'==object[key][:8] or 'http://'==object[key][:7]):
                    s.append(key)
            if sample[key] == 'string (itemBuyEvent или itemViewEvent)':
                if not(object[key]=='itemBuyEvent' or object[key]=='itemViewEvent'):
                    s.append(key)
        if s:
            spisok.append(('обьект '+ str(i), ' неверный формат: ',*s, '\n'))
    if spisok:
        stroka = ' '
        for el in spisok:
            for val in el:
                stroka += val + ' '
        return stroka
    else:
        return 'все типы ок'

sample = {'timestamp': 'int',
'referer': 'string (url)',
'location': 'string (url)',
'remoteHost': 'string',
'partyId': 'string',
'sessionId': 'string',
'pageViewId': 'string',
'eventType': 'string (itemBuyEvent или itemViewEvent)',
'item_id': 'string',
'item_price': 'int',
'item_url': 'string (url)',
'basket_price': 'string',
'detectedDuplicate': 'bool',
'detectedCorruption': 'bool',
'firstInSession': 'bool',
'userAgentName': 'string'}

with open('task2.txt') as t:
    templates = json.load(t)
print(presenceOfFields(templates))
print(extraFields(templates))
print(typeChecking(templates))


