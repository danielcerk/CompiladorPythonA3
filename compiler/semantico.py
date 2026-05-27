from compiler.sintatico import (
    
    Programa,
    Funcao,
    Atribuicao,
    Variavel,
    BinOp,
    Numero,
    Retorno,
    If,
    While,
    For,
    ChamadaFuncao

)


def analisador_semantico(ast):

    tabela_simbolos = {}

    visitar(ast, tabela_simbolos)

    print('\nTabela de símbolos:')
    print(tabela_simbolos)

def visitar(node, tabela):

    #se o nó é o programa inteiro
    if isinstance(node, Programa):

        for stmt in node.statements:

            visitar(stmt, tabela)

    #verifica se é função
    elif isinstance(node, Funcao):

        tabela[node.nome] = 'funcao'

        for param in node.parametros:

            tabela[param.nome] = 'parametro'

        for stmt in node.corpo:

            visitar(stmt, tabela)

    #verifica atribuição
    elif isinstance(node, Atribuicao):

        tabela[node.nome] = 'variavel'

        visitar(node.valor, tabela)

    #variável
    elif isinstance(node, Variavel):

        if node.nome not in tabela:

            print(
                f'Erro semântico: '
                f'variável "{node.nome}" não declarada'
            )

    #verifica operações
    elif isinstance(node, BinOp):

        #divisão por zero
        if (
            node.operador == '/'
            and isinstance(node.direita, Numero)
            and node.direita.valor in ('0', '0.0')
        ):

            print(
                'Erro semântico: divisão por zero'
            )

        visitar(node.esquerda, tabela)
        visitar(node.direita, tabela)

    #retorno
    elif isinstance(node, Retorno):

        visitar(node.valor, tabela)

    elif isinstance(node, If):

        visitar(node.condicao, tabela)

        for stmt in node.corpo:

            visitar(stmt, tabela)

        for elif_node in node.elifs:

            visitar(elif_node, tabela)

        for stmt in node.else_corpo:

            visitar(stmt, tabela)

    elif isinstance(node, While):

        visitar(node.condicao, tabela)

        for stmt in node.corpo:

            visitar(stmt, tabela)

    #for
    elif isinstance(node, For):

        tabela[node.variavel.nome] = 'variavel'

        visitar(node.iteravel, tabela)

        for stmt in node.corpo:

            visitar(stmt, tabela)

    #chamada de função
    elif isinstance(node, ChamadaFuncao):

        if node.nome not in tabela:

            print(
                f'Erro semântico: '
                f'função "{node.nome}" não declarada'
            )

        for arg in node.argumentos:

            visitar(arg, tabela)