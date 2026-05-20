def analisador_semantico(tokens):

    tabela_simbolos = {}

    i = 0

    while i < len(tokens):

        tipo, valor = tokens[i]

        if tipo == 'ID':

            if ( i + 1 < len(tokens) and tokens[i + 1][0] == 'ATRIBUICAO' ):

                tabela_simbolos[valor] = True

                if valor in tabela_simbolos:

                    print(
                        f'Erro Semântico: '
                        f'variável "{valor}" redeclarada'
                    )
                
                else:

                    tabela_simbolos[valor] = True

            else:

                if ( i + 1 < len(tokens) and tokens[i + 1][0] == 'ABRE_PAR' ):
                    i += 1
                    continue

                if valor not in tabela_simbolos:

                    print(
                        f'Erro semântico: '
                        f'variável "{valor}" não declarada'
                    )

        elif tipo == 'DIVISAO':

            if i + 1 < len(tokens):

                prox_tipo, prox_valor = tokens[i + 1]

                if (
                    prox_tipo == 'NUMERO'
                    and prox_valor in ('0', '0.0')
                ):

                    print(
                        'Erro semântico: divisão por zero'
                    )

        i += 1

    print('\nTabela de símbolos:')
    print(tabela_simbolos)