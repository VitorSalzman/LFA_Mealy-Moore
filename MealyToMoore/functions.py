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
    lstOut =[]
    aux = []
    lstOut.append(dict['type'])




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
        ''' Fazer tratamento de conversão'''
    else:
        print ('Não foi possível fazer conversão. Verifique se há saída no estado inicial.')

# Recebe um dicionário no formato Mealy e retorna um dicionário no formato Moore
def mealyToMoore(meaMachine):
    if isMealy([meaMachine['type']]):
        ''' Fazer tratamento de conversão'''
    else:
        print ('Não foi possível fazer conversão. Tipo de máquina inválido.')