from functions import *

lst = readFile('testes.txt')
print(lst)
d = toDictionary(lst)
print(d)
l1 = mooreToMealy(d)

print (l1)
cu = toList(l1)

writeFile(cu,'umteste.txt')

# isso é um arquivo de testes