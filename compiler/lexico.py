import re

# definição de tokens

TOKENS = [

    ('NUMERO', r'\d+(\.\d+)?'),
    ('IGUAL_IGUAL', r'=='),
    ('DIFERENTE', r'!='),
    ('MAIOR_IGUAL', r'>='),
    ('MENOR_IGUAL', r'<='),
    ('MAIOR', r'>'),
    ('MENOR', r'<'),
    ('SOMA', r'\+'),
    ('SUBTRACAO', r'-'),
    ('MULTIPLICACAO', r'\*'),
    ('DIVISAO', r'/'),
    ('ATRIBUICAO', r'='),
    ('DELIMITADOR', r'\n'),
    ('DOIS_PONTOS', r':'),
    ('VIRGULA', r','),
    ('ABRE_PAR', r'\('),
    ('FECHA_PAR', r'\)'),
    ('DEF', r'\bdef\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),
    ('RETURN', r'\breturn\b'),
    ('AND', r'\band\b'),
    ('OR', r'\bor\b'),
    ('NOT', r'\bnot\b'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ESPACO', r'[ \t\r]+'),
    ('ERRO', r'.'),
    
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
