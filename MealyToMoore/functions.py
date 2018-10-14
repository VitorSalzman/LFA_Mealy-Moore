from sexpression import *


# Função responsável por ler o arquivo de entrada, retorna uma lista resultante do parseamento do arquivo
def readFile(arquivo):
    try:
        arq = open("%s" % arquivo, 'r')
        lstMaq = parse_sexp(arq.read())

    except:
        print("Erro ao abrir o arquivo de leitura.")
        arq.close()

    return lstMaq


# Função de saída do programa, escreve no arquivo pré-definido;
def writeFile(lst, arquivo):
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
            dic['out_fn'] = lst[7][1:]
        return dic
    else:
        print("Máquina no formato inválido.")

# Recebe uma máquina no formato dicionário e converte para lista para ser parseada e escrita no arquivo de saída
def toList(dict):
    lstOut =[dict['type'],'symbols-in','symbols-out','states','start','finals','trans']
    for i in range(0,len(lstOut)):
        lstOut[i].extend(dict[lstOut[i]])
    if dict['type'] == 'moore':
        lstOut.append('out-fn')
        lstOut[7].extend(dict['out-fn'])

    return lstOut

# Verifica se a lista passada está em formato válido
def isValid(lst):
    if isMealy(lst) or isMoore(lst):
        if (lst[1][0] == 'symbols-in' and lst[2][0] == 'symbols-out' and lst[3][0] == 'states'
                and lst[4][0] == 'start' and lst[5][0] == 'finals' and lst[6][0] == 'trans'):
            if isMoore(lst) and lst[7][0] == 'out-fn':
                return True
    else:
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


# Recebe uma máquina de Moore (já em formato de dicionário) e verifica se é conversível para M. de Mealy
def isConversible(mooMachine):
    if mooMachine['type'] == 'moore':
        sIni = mooMachine['start']
        for tst in mooMachine['out-fn'].values():
            if tst[0] == sIni and tst[1] == []:
                return True
        return False
    else:
        print("Máquina passada não é do tipo Moore. Não é possível avaliar se é conversível.")
        return False

# Recebe um dicionário no formato Moore e retorna um dicionário no formato Mealy
def mooreToMealy(mooMachine):
    if isConversible(mooMachine):
        lstoldtrans=mooMachine['trans']     # Transições de Moore
        lstoutfn=mooMachine['out-fn']       # Saídas de cada estado
        lstnewtrans=[]                      # Lista com novas transições
        dic=mooMachine.copy()               # Copia a máquina, os únicos campos a serem tratados são trans e out-fn

        # Percorre as listas de transição de Moore
        for i in lstoldtrans:
            # Percorre as listas com as saídas de cada estado
            for j in lstoutfn:
                # Verifica o estado-destino da transição e adiciona sua saída na transição de Mealy
                if i[1] == j[0]:
                    lstnewtrans.append((i[0],i[1],i[2],j[1]))

        # Atualizando o novo dicionário
        del(dic['trans'])
        del(dic['out-fn'])
        dic['trans']=lstnewtrans

        return dic

    else:
        print ('Não foi possível fazer conversão. Verifique se há saída no estado inicial.')
        return mooMachine

        
# Recebe um dicionário no formato Mealy e retorna um dicionário no formato Moore
def mealyToMoore(meaMachine):
    if isMealy([meaMachine['type']]):
        dic=copy(meaMachine)
        del(dic['trans'])
        lstoldstates=meaMachine['states']
        
        lst=[]
        
        for x in lstoldstates:
            if(x[0] == meaMachine['start']:
                x.append('()')

        for x in meaMachine['trans']:
            for y in lstoldstates:
                if(x[1]	== y[0] and x[3] not in state):
                    y.append(x[3])

        aux = 0
        for x in lstoldstates:
            if(len(lstoldstates[aux])== 1):
               lstoldstates[aux].append('()')
            elif(len(lstoldstates[aux]) > 2):
                strinaux = ''
                for y in lstoldstates[aux]:
                    if(y[:1] != 'q'):
                        lstoldstates[aux][0] += strinaux #incrementa o a string para diferenciar
                        lstoldstates.append([lstoldstates[aux][0],y]) #adiciona no aux no seguinte formato [estado,val]
                        str_aux += '`'
                del lstoldstates[aux]
                continue
            aux += 1

        for x in lstoldstates:
            dic['out-fn']=[]
            dic('out-fn'].append(x)


        for x in lstoldstates:
            dic['states'].append(x[0])

        for x in meaMachine['finals']:
            for y in meaMachine['out-fn']:
                if (x == y[0][:2]):
                    dic['finals'].append(y[0])

        for x in dic['states']:
            for y in meaMachine['trans']:
                for z in dic['out-fn']:
                    if(x[:2] == y[0][:2]):
                        if(y[1] == z[0][:2] and y[3] == z[1]):
                            dic['trans'].append([x,z[0],y[2]])

        return dic



    else:
        print ('Não foi possível fazer conversão. Tipo de máquina inválido.')
