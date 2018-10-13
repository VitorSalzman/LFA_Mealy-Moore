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

#Função responsável por ler o arquivo de entrada, retorna uma lista com todas as linhas
def readFile(arquivo):
	try{
	arq = open("%s" %arquivo, 'r')
	}
	lst=[]
	lst=arq.readlines()
	arq.close()
	return lst
	
def writeFile(lst,arquivo):
	arq = open("%s" %arquivo, 'w')
	writeSucess = False
	for x in lst:
		arq.write(x)
		writeSucess = True
	
	arq.close()
	
	return writeSucess
	
def toDictionary(lst):
	
	dic={}
	lstaux=lst[1].split()
	lstin=[]
	for x in range(1,len(lstaux),1):
		lstin.append(lstaux[x])
		
	lstaux=lst[2].split()
	lstout=[]
	for x in range(1,len(lstaux),1):
		lstout.append(lstaux[x])
		
	lstaux=lst[3].split()
	lststates=[]
	for x in range(1,len(lstaux),1):
		lststates.append(lstaux[x])	
	
	lstaux=lst[5].split()
	lstfinals=[]
	for x in range(1,len(lstaux),1):
		lstfinals.append(lstaux[x])	
	
	
	lsttrans=[]
	lstaux=lst[7].split()
	for x in range(0,len(lstaux),1):
		lsttrans.append(lstaux[x])
	if(len(lst[8])>1):    #isto pois um len maior que 1 caracteriza outra linha de transições. Um len igual a 1 caracteriza a linha "out"
		lstaux=lst[8].split()
		for x in range(0,len(lstaux),1):
			lsttrans.append(lstaux[x])	
			
				
	dic['symbols-in'] = lstin
	dic['symbols-out'] = lstout
	dic['states'] = lststates
	dic['start'] = lst[4][1]
	dic['finals'] = lstfinals
	dic['trans'] = lsttrans
	
	return dic
	#Falta tratar as saídas de estados de máquinas de Moore
	

def isMealy(lst):
	if(str(lst[0][2])=="e"):
		return True
	else:
		return False
		
def isMoore(lst):
	
	if(str(lst[0][2])=="o"):
		return True
	else:
		return False
							
	
if __name__ == '__main__':
	main()

