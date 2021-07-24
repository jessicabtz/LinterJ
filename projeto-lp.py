import sys

program = open(sys.argv[1], "r")
num_linhas = sum(1 for linha in open(sys.argv[1]))

cont_linhas = 0
cod = '!'
esp = 0
linhas = []
tipo = ['int', 'void', 'double', 'float']


def vazia(str):
    str = str.replace(" ", "")
    if str[0] == '\n':
        return 1
    return 0

def cont_space(str):
    count = 0
    carac = ''
    if str[0] in " \t":
        carac = str[0]
        for letra in str:
            if letra == carac:
                count = count + 1
            else:
                break
    return count


def is_func(str):
    for t in tipo:
        if t in str:
            ini = str.find(' ')
            fim = str.find('(')
            if str[fim-1] == " ":
                fim = fim-1
            if ini != -1 and fim != -1:
                txt = str[ini+1:fim]
                if txt.isidentifier():
                    return 1
    return 0


def is_conditional(str):
    if 'if(' in str or 'else' in str:
        return True
    else:
        return False


def is_while(str):
    if 'while' in str:
        aux = str.replace(" ", "")
        if ';' in str:
            pos = aux.find(')', aux.find('while'))
            if aux.find(';', pos) == pos + 1:
                return True
    return False


def is_loop(str, next_str, next_str2):
    if 'for(' in str:
        return True
    if 'do' in str:
        if '{' in str and str.find('{') == str.find('do')+2:
            return True
        elif '{' in next_str and next_str[0]=='{':
            return True
        elif 'while' in next_str2:
            return True
        else:
            return False
    if 'while' in str:
        if not is_while(str):
            return True
    else:
        return False


def dentro_for(str):
    if 'for(' in str:
        ini = str.find('for(')
        fim = str.find(')')
        for count, letra in enumerate(str):
            if letra == ';':
                if ini < count and fim > count:
                    return True
                else:
                    return False


while num_linhas > 0:
    linhas.append(program.readline())
    num_linhas = num_linhas - 1
program.close()


index = 0
num_elementos_lista = len(linhas)
while index < num_elementos_lista:
    linha = linhas[index]
    aux = linha.replace(" ", "")
    cont_linhas = cont_linhas + 1

    if index+1 < num_elementos_lista:
        next_linha = linhas[index + 1]
        next_aux = next_linha.replace(" ", "")
    if index+2 < num_elementos_lista:
        next_linha2 = linhas[index + 1]
        next_aux2 = next_linha2.replace(" ", "")

    if linha[0] == '#':
        if not vazia(next_linha) and next_linha[0] != '#':
            print(f'Linha {cont_linhas}: Recomenda-se uma linha em branco entre as linhas de inclusao e o inicio do codigo')
    if '}' in linha:
        if index != num_elementos_lista-1:
            if linha[linha.find('}') + 1] != '\n':
                if not is_while(linha):
                    print(f'Linha {cont_linhas}: Recomenda-se uma quebra de linha apos o fecha chaves')
        esp = esp - 4
    if aux[0] != '\n' and aux[0] != '{':
        if cont_space(linha) < esp or cont_space(linha) > esp:
            print(f'Linha {cont_linhas}: Recomenda-se que tenham {esp} espacos antes da linha')
    if linha.find(';') != -1:
        x = linha.find(';')
        if not dentro_for(aux) and linha[x+1] != '\n':
            print(f'Linha {cont_linhas}: Recomenda-se uma quebra de linha entre comandos')
    if is_func(linha) or is_conditional(aux) or is_loop(aux, next_aux, next_aux2):
        esp = esp + 4
        if '{' in linha:
            if linha[linha.find('{')+1] != '\n':
                print(f'Linha {cont_linhas}: Recomenda-se uma quebra de linha apos o abre chaves ')
        elif '{' in next_linha and next_aux[0] == '{':
            if cont_space(next_linha) < esp - 4 or cont_space(next_linha) > esp-4:
                print(f'Linha {cont_linhas}: Recomenda-se que tenham {esp-4} espacos antes da linha')
            if next_linha[next_linha.find('{')+1] != '\n':
                print(f'Linha {cont_linhas + 1}: Recomenda-se uma quebra de linha apos o abre chaves ')
        else:
            if cont_space(next_linha) < esp or cont_space(next_linha) > esp:
                print(f'Linha {cont_linhas + 1}: Recomenda-se que tenham {esp} espacos antes da linha')
            cont_linhas = cont_linhas + 1
            index = index + 1
            esp = esp - 4
    index = index + 1

