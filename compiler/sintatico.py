from graphviz import Digraph

class Programa:

    def __init__(self, statements):
        self.statements = statements


class Funcao:

    def __init__(self, nome, parametros, corpo):
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo


class Retorno:

    def __init__(self, valor):
        self.valor = valor


class Atribuicao:

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor


class BinOp:

    def __init__(self, esquerda, operador, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita


class Numero:

    def __init__(self, valor):
        self.valor = valor


class Variavel:

    def __init__(self, nome):
        self.nome = nome


class ChamadaFuncao:

    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos


class While:

    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0
        self.linha = 1

    # token atual
    def atual(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return ('EOF', '', -1)

    # consumir token
    def consumir(self, tipo_esperado):

        tipo, valor, linha = self.atual()

        if tipo == tipo_esperado:

            self.pos += 1
            return valor

        raise Exception(
            f'Erro sintático ( Linha {linha} ): Esperado {tipo_esperado}'
        )

    

    def parse(self):

        statements = []

        while self.atual()[0] != 'EOF':

            if self.atual()[0] == 'NOVA_LINHA':

                self.consumir('NOVA_LINHA')
                continue

            statements.append(
                self.statement()
            )

        return Programa(statements)

    

    def statement(self):

        tipo, _, linha = self.atual()

        if tipo == 'DEF':
            return self.funcao()

        elif tipo == 'RETURN':
            return self.retorno()

        elif tipo == 'WHILE':
            return self.while_stmt()

        elif tipo == 'ID':
            return self.atribuicao()

        raise Exception(f'Comando inválido: {tipo}')

   

    def funcao(self):

        self.consumir('DEF')

        nome = self.consumir('ID')

        self.consumir('ABRE_PAR')

        parametros = []

        if self.atual()[0] != 'FECHA_PAR':

            parametros.append(
                Variavel(self.consumir('ID'))
            )

            while self.atual()[0] == 'VIRGULA':

                self.consumir('VIRGULA')

                parametros.append(
                    Variavel(self.consumir('ID'))
                )

        self.consumir('FECHA_PAR')

        self.consumir('DOIS_PONTOS')

        self.consumir('NOVA_LINHA')

        self.consumir('INDENT')

        corpo = []

        while self.atual()[0] != 'DEDENT':

            corpo.append(
                self.statement()
            )

            if self.atual()[0] == 'NOVA_LINHA':

                self.consumir('NOVA_LINHA')

        self.consumir('DEDENT')

        return Funcao(nome, parametros, corpo)

    

    def retorno(self):

        self.consumir('RETURN')

        valor = self.expressao()

        return Retorno(valor)

  

    def while_stmt(self):

        self.consumir('WHILE')

        condicao = self.expressao()

        self.consumir('DOIS_PONTOS')

        self.consumir('NOVA_LINHA')

        self.consumir('INDENT')

        corpo = []

        while self.atual()[0] != 'DEDENT':

            corpo.append(
                self.statement()
            )

            if self.atual()[0] == 'NOVA_LINHA':

                self.consumir('NOVA_LINHA')

        self.consumir('DEDENT')

        return While(condicao, corpo)

   

    def atribuicao(self):

        nome = self.consumir('ID')

        self.consumir('ATRIBUICAO')

        valor = self.expressao()

        return Atribuicao(nome, valor)

    

    def expressao(self):

        esquerda = self.termo()

        operadores = [

            'SOMA',
            'SUBTRACAO',
            'MULTIPLICACAO',
            'DIVISAO',
            'MENOR',
            'MAIOR',
            'IGUAL_IGUAL',
            'DIFERENTE',
            'MENOR_IGUAL',
            'MAIOR_IGUAL'
        ]

        while self.atual()[0] in operadores:

            operador = self.atual()[1]

            self.pos += 1

            direita = self.termo()

            esquerda = BinOp(
                esquerda,
                operador,
                direita
            )

        return esquerda

    

    def termo(self):

        tipo, valor, linha = self.atual()

        # número
        if tipo == 'NUMERO':

            self.consumir('NUMERO')

            return Numero(valor)

        # variável ou função
        elif tipo == 'ID':

            nome = self.consumir('ID')

            # chamada de função
            if self.atual()[0] == 'ABRE_PAR':

                self.consumir('ABRE_PAR')

                argumentos = []

                if self.atual()[0] != 'FECHA_PAR':

                    argumentos.append(
                        self.expressao()
                    )

                    while self.atual()[0] == 'VIRGULA':

                        self.consumir('VIRGULA')

                        argumentos.append(
                            self.expressao()
                        )

                self.consumir('FECHA_PAR')

                return ChamadaFuncao(nome, argumentos)

            return Variavel(nome)

        # expressão entre parênteses
        elif tipo == 'ABRE_PAR':

            self.consumir('ABRE_PAR')

            expr = self.expressao()

            self.consumir('FECHA_PAR')

            return expr

        raise Exception(f'Expressão inválida: {tipo}')


def parser(tokens):

    p = Parser(tokens)

    return p.parse()


contador = 0

def novo_id():

    global contador

    contador += 1

    return f'n{contador}'


def gerar_ast(ast_programa):

    dot = Digraph(comment="AST Mini Python")

    dot.attr("node", shape="box", style="rounded")

    def adicionar_nos(node, parent_id=None):

        node_id = novo_id()

        if isinstance(node, Programa):
            label = "Programa"

        elif isinstance(node, Funcao):
            label = f"Funcao\\n{node.nome}"

        elif isinstance(node, Retorno):
            label = "Return"

        elif isinstance(node, Atribuicao):
            label = f"Atribuicao\\n{node.nome}"

        elif isinstance(node, BinOp):
            label = f"Operador\\n{node.operador}"

        elif isinstance(node, Numero):
            label = f"Numero\\n{node.valor}"

        elif isinstance(node, Variavel):
            label = f"Variavel\\n{node.nome}"

        elif isinstance(node, ChamadaFuncao):
            label = f"Chamada\\n{node.nome}"

        elif isinstance(node, While):
            label = "While"

        else:
            label = type(node).__name__

        dot.node(node_id, label)

        if parent_id:

            dot.edge(parent_id, node_id)

        if isinstance(node, Programa):

            for stmt in node.statements:
                adicionar_nos(stmt, node_id)

        elif isinstance(node, Funcao):

            for param in node.parametros:
                adicionar_nos(param, node_id)

            for stmt in node.corpo:
                adicionar_nos(stmt, node_id)

        elif isinstance(node, Retorno):

            adicionar_nos(node.valor, node_id)

        elif isinstance(node, Atribuicao):

            adicionar_nos(node.valor, node_id)

        elif isinstance(node, BinOp):

            adicionar_nos(node.esquerda, node_id)
            adicionar_nos(node.direita, node_id)

        elif isinstance(node, ChamadaFuncao):

            for arg in node.argumentos:
                adicionar_nos(arg, node_id)

        elif isinstance(node, While):

            adicionar_nos(node.condicao, node_id)

            for stmt in node.corpo:
                adicionar_nos(stmt, node_id)

    adicionar_nos(ast_programa)

    dot.render(
        "ast_mini_python",
        format="png",
        cleanup=True
    )

    print("AST gerada: ast_mini_python.png")