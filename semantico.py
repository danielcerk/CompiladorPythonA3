def analisador_semantico(tokens):

    tabela_simbolos = {}

    i = 0

    while i < len(tokens):

        tipo, valor = tokens[i]

        if tipo == 'ID':

            if i + 1 < len(tokens) and tokens[i + 1][0] == 'ATRIBUICAO':

                variavel = valor

                if variavel in tabela_simbolos:
                    print(f'Aviso semântico: variável "{variavel}" redeclarada')

                tabela_simbolos[variavel] = True

            else:

                if valor not in tabela_simbolos:
                    print(f'Erro semântico: variável "{valor}" não declarada')

        if tipo == 'DIVISAO':

            if i + 1 < len(tokens):

                prox_tipo, prox_valor = tokens[i + 1]

                if prox_tipo == 'NUMERO' and prox_valor == '0':
                    print('Erro semântico: divisão por zero')

        i += 1

    print('\nTabela de símbolos:')
    print(tabela_simbolos)