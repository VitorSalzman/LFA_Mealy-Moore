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
            ''' Call functions'''
        elif isMoore(lstMaqIn):
            '''DO THE STUFF'''



if __name__ == '__main__':
    main(argv)
