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

ast_programa = Programa([

    Funcao(
        nome='soma',

        parametros=[
            Variavel('a'),
            Variavel('b')
        ],

        corpo=[

            Retorno(

                BinOp(
                    esquerda=Variavel('a'),
                    operador='+',
                    direita=Variavel('b')
                )

            )

        ]
    ),

    Atribuicao(

        nome='x',

        valor=ChamadaFuncao(
            nome='soma',

            argumentos=[
                Numero(2),
                Numero(3)
            ]
        )
    )
])

dot = Digraph(comment="AST Mini Python")
dot.attr("node", shape="box", style="rounded")

contador = 0


def novo_id():

    global contador

    contador += 1

    return f"n{contador}"


def adicionar_nos(node, parent_id=None):

    node_id = novo_id()

    if isinstance(node, Programa):

        label = "Programa"

    elif isinstance(node, Funcao):

        label = f"Funcao\\n{node.nome}"

    elif isinstance(node, Retorno):

        label = "retorna"

    elif isinstance(node, Atribuicao):

        label = f"Atribuicao\\n{node.nome}"

    elif isinstance(node, BinOp):

        label = f"operador\\n{node.operador}"

    elif isinstance(node, Numero):

        label = f"Numero\\n{node.valor}"

    elif isinstance(node, Variavel):

        label = f"Variavel\\n{node.nome}"

    elif isinstance(node, ChamadaFuncao):

        label = f"Chama\\n{node.nome}"

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

adicionar_nos(ast_programa)

dot.render("ast_mini_python", format="png", cleanup=True)