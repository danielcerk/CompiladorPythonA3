import ast
from graphviz import Digraph

codigo = """
def soma(a, b):
    return a + b
x = soma(2, 3)
"""
tree = ast.parse(codigo)

dot = Digraph(comment="AST de Python")
dot.attr("node", shape="box", style="rounded")

contador = 0

def novo_id():
    global contador
    contador += 1
    return f"n{contador}"

def adicionar_nos(node, parent_id=None):
    node_id = novo_id()
    label = type(node).__name__

    if isinstance(node, ast.FunctionDef):
        label += f"\\n{node.name}"
    elif isinstance(node, ast.Name):
        label += f"\\n{node.id}"
    elif isinstance(node, ast.Constant):
        label += f"\\n{node.value}"
    elif isinstance(node, ast.arg):
        label += f"\\n{node.arg}"

    dot.node(node_id, label)

    if parent_id:
        dot.edge(parent_id, node_id)

    for campo, valor in ast.iter_fields(node):
        if isinstance(valor, ast.AST):
            adicionar_nos(valor, node_id)
        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, ast.AST):
                    adicionar_nos(item, node_id)

adicionar_nos(tree)

dot.render("ast_python", format="png", cleanup=True)
print("Gerado: ast_python.png")
