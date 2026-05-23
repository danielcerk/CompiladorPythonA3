def analisador_semantico(tokens):

    tabela_simbolos = {}

    i = 0

    while i < len(tokens):

        tipo, valor, linha = tokens[i]

        if tipo == 'DEF':

            i += 1

            # nome da função
            if i < len(tokens) and tokens[i][0] == 'ID':

                nome_funcao = tokens[i][1]
                tabela_simbolos[nome_funcao] = 'funcao'

            i += 1

            # parâmetros
            if i < len(tokens) and tokens[i][0] == 'ABRE_PAR':

                i += 1

                while (
                    i < len(tokens)
                    and tokens[i][0] != 'FECHA_PAR'
                ):

                    if tokens[i][0] == 'ID':

                        parametro = tokens[i][1]
                        tabela_simbolos[parametro] = 'parametro'

                    i += 1

        if tipo == 'ID':

            if ( i + 1 < len(tokens) and tokens[i + 1][0] == 'ATRIBUICAO' ):
                
                if valor not in tabela_simbolos:

                    tabela_simbolos[valor] = True
                    i +=1
                    continue

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
                        f'Erro semântico (Linha {linha}): '
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
                        f'Erro semântico (Linha {linha}): divisão por zero'
                    )

        i += 1

    print('\nTabela de símbolos:')
    print(tabela_simbolos)