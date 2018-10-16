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
    lstOut = [dic['type'], ['symbols-in'], ['symbols-out'], ['states'], ['start'], ['finals'], ['trans']]
    
    for i in range(1, len(lstOut)):           #Retirado pois estava dando erro. A retirada não impactou no resultado
        lstOut[i].extend(dic[lstOut[i][0]])

		
    if dic['type'] == 'moore':
        lstOut.append(['out-fn'])
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

        
        return dic

    else:
        print('Não foi possível fazer conversão. Verifique se há saída no estado inicial.')
        return mooMachine




# Função auxiliar para tratar novos estados na conversão de Me pra Mo
def _estadosMoore(meaMachine):
    states = []

    for dino in  meaMachine['states']: # Lista que guardará novos estados criado
        states.append([dino])

    # Tratamento de estado inicial
    for i in states:
        if i == meaMachine['start']:
            i.append('[]') # estado inicial tem saída vazia

    # Analisa saída das transições e adiciona nos estados
    for j in meaMachine['trans']:
        for s in states:
            if j[1] == s[0] and j[3] not in s:  # se estado de destino é o estado já listado e ainda não foi adicionado saída
                s.append(j[3])          # Adiciona a saída

    i = 0
    while i < len(states):
        if len(states[i]) == 1:     # se o estado não tiver valor nenhum associado, saída vazia
            states[i].append("[]")
        elif len(states[i])>2:      # um estado pode ter apenas uma saída, se tiver mais de uma, surgem novos estados
            apost = "\'"
            for v in range(1,len(states[i])):
                novoEstado = states[i][0] + apost
                states.append([novoEstado,states[i][v]])        # lista
                apost+="\'"
            del states[i]
            continue        # evita incrementar pois len acaba mudando
        i+= 1
    return states

# Função auxiliar que trata das transições
def _transMoore(meaMachine, newMoore):         #por enquanto, SEM UTILIZAÇÃO
    newMoore['trans'] = []
    for i in meaMachine['trans']:       # para cada transição em mealy
        for j in newMoore['out-fn']:    # procura nos estados de moore
            if j[0][0:len(i[0])] == i[1] and j[1] == i[3]:      # se o nome do estado (sem apóstrofos) for igual e a saída dele for igual
                transMoor = [i[0],j[0],i[2]]                # estado inicial, estado final e simbolo de transição
                newMoore['trans'].append(transMoor)
    return newMoore


# Recebe um dicionário no formato Mealy e retorna um dicionário no formato Moore
def mealyToMoore(meaMachine):
    moore = meaMachine.copy()  # Cria cópia do dicionário para conversão
    moore['type'] = 'moore'
    moore['states'] = []
    moore['out-fn'] = _estadosMoore(meaMachine)  # Estados com saída
    moore['trans'] = []  # Limpa as transições no novo dicionário

    for i in moore['out-fn']:
        moore['states'].append(i[0])    # Adiciona os estados para a nova máquina

    # Adiciona possíveis novos estados finais
    for out in moore['states']:
        if out[0:2] in meaMachine['finals']:
            moore['finals'].append(out)

    # Tratando
    for stt in moore['states']:
        for transi in meaMachine['trans']:
            for sttO in moore['out-fn']:
                if (stt[0:2] == transi[0][0:2]):
                    if(transi[1] == sttO[0][0:2] and transi[3] == sttO[1]):
                        moore['trans'].append([stt,sttO[0],transi[2]])

    return moore