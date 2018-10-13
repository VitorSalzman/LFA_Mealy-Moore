#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  validacoes.py
#  
#  Copyright 2018 Salzman <Salzman@SALZMAN-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# Função responsável por ler o arquivo de entrada, retorna uma lista com todas as linhas
def readFile(arquivo):
    try:
        arq = open("%s" % arquivo, 'r')
    except:
        print("Erro ao abrir o arquivo de leitura.")

    lst = []
    lst = arq.readlines()
    arq.close()
    return lst


# Função de saída do programa, escreve no arquivo pré-definido; retorna um boolean quando a escrita é feita com sucesso
def writeFile(lst, arquivo):
    try:
        arq = open("%s" % arquivo, 'w')
    except:
        print("Erro ao abrir o arquivo de escrita.")

    writeSucess = False
    for x in lst:
        arq.write(x)
        writeSucess = True

    arq.close()

    return writeSucess


def toDictionary(lst):
    dic = {}
    

    dic['symbols-in'] = lst[1][1:]
	dic['symbols-out'] = lst[2][1:]
	dic['states'] = lst[3][1:]
	dic['start'] = lst[4][1:]
	dic['finals'] = lst[5][1:]
	dic['trans'] = lst[7][:]
	if(isMoore(lst)):
		dic['out_fn']= lst[8][0:]

    return dic

def validMachine(lst):
	try:
		test = 100
		typeMachine = lst[0]
		test = lst[1].index('symbols-in')
		test = lst[2].index('symbols-out')
		test = lst[3].index('states')
		test = lst[4].index('start')
		test = lst[5].index('finals')
		test = lst[6].index('trans')
		if typeMachine.lower() == "moore":
			test = lst[7].index('out-fn')
		return True
	except ValueError:
		return False


# Verifica se a máquina passada na lista é do tipo Mealy
def isMealy(lst):
    if str(lst[0]).lower() == "mealy":
        return True
    else:
        return False

# Verifica se a máquina passada na lista é do tipo Moore
def isMoore(lst):
    if str(lst[0]).lower() == "moore":
        return True
    else:
        return False
