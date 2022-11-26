n = input('введите название файла: ')
with open(n) as f:
    s=f.read().split()
for i in range(len(s)):
    if s[i][len(s[i])-1] in '!.,':
        s[i] = s[i][0:len(s[i])-1]
dct={}
for el in s:
    dct[el]=dct.get(el, 0)+1
p=[]
ang=[]
for key, val in dct.items():
    if len(key)>3:
        p.append((val , key))

    if 65<=ord(key[0])<=90 or 97<=ord(key[0])<=122:
        ang.append(key)
print(sorted(p, reverse=True)[0][1])

print(sorted(ang, key=lambda x: len(x), reverse=True)[0])
