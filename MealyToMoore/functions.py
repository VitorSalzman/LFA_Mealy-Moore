from sexpression import *


# Função responsável por ler o arquivo de entrada, retorna uma lista resultante do parseamento do arquivo
def readFile(arquivo):
    lstMaq = None
    arq = None
    try:
        arq = open("%s" % arquivo, 'r')
        lstMaq = parse_sexp(arq.read())

    except:
        print("Erro ao abrir o arquivo de leitura.")
        arq.close()

    return lstMaq


# Função de saída do programa, escreve no arquivo pré-definido;
def writeFile(lst, arquivo):
    arq = None
    try:
        arq = open("%s" % arquivo, 'w')
    except:
        print("Erro ao abrir o arquivo de escrita.")
    try:
        arq.write(print_sexp(lst))
    except:
        print("Erro na escrita")

    arq.close()


# Recebe uma lista e transforma em um dicionário (valores das chaves serão listas)
# Decisão de projeto para maior facilidade de manipulação
def toDictionary(lst):
    if isValid(lst):
        dic = {'type': lst[0], 'symbols-in': lst[1][1:], 'symbols-out': lst[2][1:], 'states': lst[3][1:],
               'start': lst[4][1:], 'finals': lst[5][1:], 'trans': lst[6][1:]}
        if (isMoore(lst)):
            dic['out-fn'] = lst[7][1:]
        return dic
    else:
        print("Máquina no formato inválido.")


# Recebe uma máquina no formato dicionário e converte para lista para ser parseada e escrita no arquivo de saída
def toList(dic):
    lstOut = [dic['type'], dic['symbols-in'], dic['symbols-out'], dic['states'], dic['start'], dic['finals'], dic['trans']]
    for i in range(1, len(lstOut)):
        lstOut[i].extend(dic[lstOut[i][0]])
    if dic['type'] == 'moore':
        lstOut.append(dic['out-fn'])
        lstOut[7].extend(dic['out-fn'])

    return lstOut


# Verifica se a lista passada está em formato válido
def isValid(lst):
    if isMealy(lst):
        if (lst[1][0] == 'symbols-in' and lst[2][0] == 'symbols-out' and lst[3][0] == 'states'
                and lst[4][0] == 'start' and lst[5][0] == 'finals' and lst[6][0] == 'trans'):
            return True

    elif isMoore(lst):
        if (lst[1][0] == 'symbols-in' and lst[2][0] == 'symbols-out' and lst[3][0] == 'states'
                and lst[4][0] == 'start' and lst[5][0] == 'finals' and lst[6][0] == 'trans'
                and lst[7][0] == 'out-fn'):
            return True
    else:
        return False


# Verifica se a máquina passada na lista é do tipo Mealy
def isMealy(lst):
    if lst[0] == "mealy":
        return True
    else:
        return False


# Verifica se a máquina passada na lista é do tipo Moore
def isMoore(lst):
    if lst[0] == "moore":
        return True
    else:
        return False


# Recebe uma máquina de Moore (já em formato de dicionário) e verifica se é conversível para M. de Mealy
def isConversible(mooMachine):
    if mooMachine['type'] == 'moore':
        sIni = mooMachine['start'][0]
        for tst in mooMachine['out-fn']:
            if tst[0] == sIni and tst[1] == []:
                return True
        return False
    else:
        print("Máquina passada não é do tipo Moore. Não é possível avaliar se é conversível.")
        return False


# Recebe um dicionário no formato Moore e retorna um dicionário no formato Mealy
def mooreToMealy(mooMachine):
    if isConversible(mooMachine):
        lstoldtrans = mooMachine['trans']  # Transições de Moore
        lstoutfn = mooMachine['out-fn']  # Saídas de cada estado
        lstnewtrans = []  # Lista com novas transições
        dic = mooMachine.copy()  # Copia a máquina, os únicos campos a serem tratados são trans e out-fn
        dic['type'] = 'mealy'

        # Percorre as listas de transição de Moore
        for i in lstoldtrans:
            # Percorre as listas com as saídas de cada estado
            for j in lstoutfn:
                # Verifica o estado-destino da transição e adiciona sua saída na transição de Mealy
                if i[1] == j[0]:
                    lstnewtrans.append([i[0], i[1], i[2], j[1]])

        # Atualizando o novo dicionário
        del (dic['trans'])
        del (dic['out-fn'])
        dic['trans'] = lstnewtrans
        print(dic['type'])
        
        return dic

    else:
        print('Não foi possível fazer conversão. Verifique se há saída no estado inicial.')
        return mooMachine




# Função auxiliar para tratar a criação de novos estados na conversão de Me pra Mo
def _estadosMoore(meaMachine):
    newStates = []  # Lista que guardará novos estados criados
    finalStates = []  # Lista com novos estados finais
    out_fn = []  # Lista com relação estado/saída

    # Percorre todos os estados
    for i in meaMachine['states']:
        saidas = []

        if i == meaMachine['start']:
            saidas.append([])
        # Percorre todos os "estados-destino" das transições
        for j in meaMachine['trans'][1]:
            # Ao achar o estado atual como destino de uma transição, pega-se a saída
            if i == j:
                if meaMachine['trans'][3] not in saidas:  # Sem repetí-la
                    saidas.append(meaMachine['trans'][3])
        # Caso um estado seja destino de mais de uma saída das transições de mealy, cria-se novos estados para cada saída distinta
        if len(saidas) > 1:
            apost = "\'"  # Apóstrofo para diferenciar novos estados
            out_fn.append([i, saidas[0]])  # Estado original associado a primeira saída
            for n in range(1, len( saidas)):  # A primeira saída está associada para o estado original, n-1 estados novos serão criados e associados as saídas sobressalentes
                ns = i + apost  # Novo estado = estado + '
                apost += "\'"
                print(ns)
                newStates.append(ns)  # Novo estado criado, adicionado
                out_fn.append([ns, saidas[n]])
                if i in meaMachine['finals']:  # Caso o estado original seja final, o novo estado criado derivado também é final
                    finalStates.append(ns)
        elif len(saidas) == 1:  # Caso o estado tenha apenas uma saída
            out_fn.append([i, saidas[0]])
        else:
            out_fn.append([i, saidas])  # No caso de saídas vazias

    return newStates, finalStates, out_fn


# Função auxiliar que trata das transições
def _transMoore(meaMachine, newMoore):
    newMoore['trans'] = []
    for i in meaMachine['trans']:       # para cada transição em mealy
        for j in newMoore['out-fn']:    # procura nos estados de moore
            if j[0][0:len(i[0])] == i[1] and j[1] == i[3]:      # se o nome do estado (sem apóstrofos) for igual e a saída dele for igual
                transMoor = [i[0],j[0],i[2]]                # estado inicial, estado final e simbolo de transição
                newMoore['trans'].append(transMoor)
    return newMoore


# Recebe um dicionário no formato Mealy e retorna um dicionário no formato Moore
'''def mealyToMoore1(meaMachine):
    if isMealy([meaMachine['type']]):
        dic = meaMachine.copy()  # Cria cópia do dicionário para conversão
        dic['type'] = 'moore'  # Novo dic é máquina de moore
        del (dic['trans'])  # As transições são diferentes, logo deleta-se do novo dicionário
        newStates, finalStates, dic['out-fn'] = _estadosMoore(meaMachine)  # Listas que guardarão respectivamentes novos estados finais
        dic['states'] = list(set(dic['states'].extend(newStates)))  # Adição dos estados usando set() para evitar repetições e forçando o tipo ser list()
        dic['finals'] = list(set(dic['finals'].extend(finalStates)))
        dic = _transMoore(meaMachine,dic)

        return dic


    else:
        print('Não foi possível fazer conversão. Tipo de máquina inválido.')
'''

def mealyToMoore1(mealyMachine):
	
	if isMealy([mealyMachine['type']]): #Validação de máquina de mealy
		#Criação de máquina de Moore
		mooreMachine={}
		mooreMachine['type'] = 'moore'
		mooreMachine['symbols-in'] = mealyMachine['symbols-in']
		mooreMachine['symbols-out'] = mealyMachine['symbols-out']
		mooreMachine['start'] = mealyMachine['start']
		mooreMachine['states'] = []
		mooreMachine['finals'] = []
		mooreMachine['trans'] = []
		lst = []
		for x in mealyMachine['states']:  #criando vetor auxiliar com estados da máquina de mealy 
			lst.append([x])

		for x in mealyMachine['trans']:
			for y in lst:
				if(x[1] == y[0] and x[3] not in y): # adicionando saídas a estados no vetor auxiliar
					y.append(x[3])
		pos = 0
		for x in lst:
			if(len(lst[pos]) == 1):
				lst[pos].append('()')
			elif(len(lst[pos]) > 2):
				i = 0
				string = ''
				for y in lst[pos]:
					if(i > 0):
						lst[pos][0] += string
						lst.append([lst[pos][0],y])
						string += '`'
						i+=1
				del lst[pos]
				continue
			pos = pos+1
			

		mooreMachine['out-fn'] = lst
		
		for x in lst:
			mooreMachine['states'].append(x[0])
		
		for x in mealyMachine['finals']:
			for y in mooreMachine['out-fn']:
				if(x == y[0][:2]):
					mooreMachine['finals'].append(y[0])
			
		for x in mealyMachine['trans']:
			for y in mooreMachine['out-fn']:
				if(x[1] == y[0][:2]):
					if(x[3] == y[1]):
						mooreMachine['trans'].append([x[0],y[0],x[2]])
						
	
		return mooreMachine		
				

	else:
		print('Não foi possível fazer conversão. Tipo de máquina inválido.')
		return mealyMachine
