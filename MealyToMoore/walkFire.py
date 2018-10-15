from functions import *

lst = readFile('moore1.txt')
print(lst)
d = toDictionary(lst)
print(d)
l1 = toList(d)

print (l1)

writeFile(l1,'umteste.txt')

# isso é um arquivo de testes