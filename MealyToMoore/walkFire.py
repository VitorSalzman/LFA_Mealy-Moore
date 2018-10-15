from functions import *
lstMaqIn = readFile('mealy3.txt')
arqConv = 'bbbb.txt'

if isMealy(lstMaqIn):
    maqMealy = toDictionary(lstMaqIn)
    maqMoore = mealyToMoore1(maqMealy)
    
    #print(maqMoore)
    
    lstMoore = toList(maqMoore)
    writeFile(lstMoore, arqConv)

elif isMoore(lstMaqIn):
    maqMoore = toDictionary(lstMaqIn)
    maqMealy = mooreToMealy(maqMoore)
    lstMealy = toList(maqMealy)
    writeFile(lstMealy, arqConv)
else:
    print("Erro, tipo de máquina inválida")
