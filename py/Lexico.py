import re


# definição de tokens


TOKENS = [
    ('NUMERO',       r'\d+'),
    ('SOMA',         r'\+'),
    ('SUBTRACAO',    r'-'),
    ('MULTIPLICACAO', r'\*'),
    ('DIVISAO',      r'/'),
    ('ATRIBUICAO',   r'='),
    ('PONTO_VIRGULA', r';'),
    ('ABRE_PAR',     r'\('),
    ('FECHA_PAR',    r'\)'),
    ('ID',           r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ESPACO',       r'[ \t\n]+'),
    ('ERRO',         r'.'),
]


# junta tudo


regex = '|'.join(
    f'(?P<{nome}>{padrao})'
    for nome, padrao in TOKENS
)


# analisa 


def analisador_lexico(codigo):

    tokens_encontrados = []

    for match in re.finditer(regex, codigo):

        tipo = match.lastgroup
        valor = match.group()

        # ignora
        if tipo == 'ESPACO':
            continue

        # olha o erro 
        elif tipo == 'ERRO':
            print(f'Erro léxico: símbolo inválido "{valor}"')

        else:
            tokens_encontrados.append((tipo, valor))

    return tokens_encontrados


# teste


codigo_fonte = """
x = 10 + 20;
y = x * 2;
z = (x + y) / 3;
"""

resultado = analisador_lexico(codigo_fonte)


# mostra 


print("\nTOKENS ENCONTRADOS:\n")

for token in resultado:
    print(token)