import re  # Verificaremos se precisa -q
from sys import argv  # import para utilizar os argumentos passados pela linha de comando
from functions import *

def main(args):
    if len(args) != 5:
        print("Formato de entrada inválido. Esperado: nomeprograma -i arquivoIn.txt -o arquivoOut.txt")
    else:
        # Armazena nome do arquivo de entrada contendo a máquina a ser convertida
        arqMaq = args[2]
        # Armazena nome do arquivo de saída onde a máquina convertida será guardada
        arqConv = args[4]

        # Lista (pode vir a ser dicionário) com a máquina
        lstMaqIn = readFile(arqMaq)

        if isMealy(lstMaqIn):
            maqMealy = toDictionary(lstMaqIn)
            maqMoore = mealyToMoore(maqMealy)
            lstMoore = toList(maqMoore)
            writeFile(lstMoore,arqConv)

        elif isMoore(lstMaqIn):
            maqMoore = toDictionary(lstMaqIn)
            maqMealy = mooreToMealy(maqMoore)
            lstMealy = toList(maqMealy)
            writeFile(lstMealy,arqConv)
        else:
              print("Erro, tipo de máquina inválida")

if __name__ == '__main__':
    main(argv)
