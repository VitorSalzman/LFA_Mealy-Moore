from functions import *

lstMaqIn = readFile("mealy3.txt")
arqConv = "teste.txt"

if isMealy(lstMaqIn):
    maqMealy = toDictionary(lstMaqIn)
    print(maqMealy)
    maqMoore = mealyToMoore(maqMealy)
    print(maqMoore)
    lstMoore = toList(maqMoore)
    print(lstMoore)
    writeFile(lstMoore, arqConv)

elif isMoore(lstMaqIn):
    maqMoore = toDictionary(lstMaqIn)
    maqMealy = mooreToMealy(maqMoore)
    lstMealy = toList(maqMealy)
    print(lstMealy)
    writeFile(lstMealy, arqConv)

else:
    print("Erro, tipo de máquina inválida")


    # # CONVERSAO DE MAQUINA DE MEALY PARA MOORE
    # def mealy_to_moore(machine_in):
    #     machine_out = {}
    #     machine_out['type'] = 'moore'
    #     machine_out['symbols-in'] = machine_in['symbols-in']
    #     machine_out['symbols-out'] = machine_in['symbols-out']
    #     machine_out['start'] = machine_in['start']
    #     machine_out['states'] = []
    #     machine_out['finals'] = []
    #     machine_out['trans'] = []
    #     machine_out['out-fn'] = []
    #
    #     aux = []
    #
    #     for field in machine_in['states']:  # jogar os estados no aux para trabalha-los
    #         aux.append([field])
    #
    #     for field in aux:
    #         if (field[0] == machine_in['start']):
    #             field.append('()')  # encontrou o inicial em aux e adiciona '()' nele
    #
    #     for trans in machine_in['trans']:
    #         for state in aux:  # aux é uma lista de estados
    #             if (trans[1] == state[0] and trans[3] not in state):
    #                 state.append(trans[3])  # modificando campo do aux
    #
    #     '''
    #     se for inicial precisa adicionar () no aux ai ficaria [q0,(),val1,val2] dps tratar-lo
    #     trans[1] = estado de saida
    #     state[0] = estado
    #     trans[3] = valor saida
    #     estado de saida = estado AND valor saida não está no estado (aux carrega [estado,valor,...]
    #     se nao tiver adiciona no aux o novo valor ficando aux[] = [estado,val1,val2,...]
    #     '''
    #
    #     pos = 0
    #     for field in aux:
    #         if (len(aux[pos]) == 1):
    #             aux[pos].append('()')
    #         elif (len(aux[pos]) > 2):  # corrigindo o aux de ter o mesmo estado varios valores (precisa criar + estados)
    #             str_aux = ''
    #             for data in aux[pos]:
    #                 if (data[:1] != 'q'):  # se não for o primeiro campo (sempre começa com estado 'q')
    #                     aux[pos][0] += str_aux  # incrementa o a string para diferenciar
    #                     aux.append([aux[pos][0], data])  # adiciona no aux no seguinte formato [estado,val]
    #                     str_aux += '`'
    #             del aux[pos]  # deleta o aux utilizado (ja que ele não esta no formato devido) [estado,val1,val2,...]
    #             continue  # pular o pos += 1
    #         pos += 1
    #
    #     for field in aux:  # adicionando todos os campos do aux no out-fn
    #         machine_out['out-fn'].append(field)
    #
    #     for field in aux:
    #         machine_out['states'].append(field[0])  # o primeiro valor de cada campo aux são os estados
    #
    #     for final_I in machine_in['finals']:
    #         for out_O in machine_out['out-fn']:
    #             if (final_I == out_O[0][
    #                            :2]):  # apenas verifica os 2 caracteres do estado out é final em mealy, se sim adiciona no final do moore (pode vir q2,q2`,etc)
    #                 machine_out['finals'].append(out_O[0])
    #
    #     for state_O in machine_out['states']:
    #         for trans_I in machine_in['trans']:
    #             for out_O in machine_out['out-fn']:
    #                 if (state_O[:2] == trans_I[0][:2]):  # ✓
    #                     if (trans_I[1] == out_O[0][:2] and trans_I[3] == out_O[1]):
    #                         machine_out['trans'].append([state_O, out_O[0], trans_I[2]])
    #                         '''
    #                         state_O = estado origem da transição
    #                         out_O[0] = estado destino da transição
    #                         trans_I[2] = entrada
    #                         '''
    #     return machine_out