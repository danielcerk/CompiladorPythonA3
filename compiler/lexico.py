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
    ('COMENTARIO', r'\#.*'),
    ('DIVISAO', r'/'),
    ('ATRIBUICAO', r'='),
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
    ('ESPACO', r'[ \t]+'),
    ('ERRO', r'.'),
]

# junta tudo

regex = '|'.join(
    f'(?P<{nome}>{padrao})'
    for nome, padrao in TOKENS
)

# analisa 

def analisador_lexico(codigo):

    tokens = []

    linhas = codigo.splitlines()

    pilha_indentacao = [0]

    for linha in linhas:

        # ignora linhas vazias
        if linha.strip() == '':

            continue

        indentacao = len(linha) - len(linha.lstrip(' '))

        # INDENT
        if indentacao > pilha_indentacao[-1]:

            pilha_indentacao.append(indentacao)
            tokens.append(('INDENT', indentacao))

        # DEDENT
        while indentacao < pilha_indentacao[-1]:

            pilha_indentacao.pop()
            tokens.append(('DEDENT', indentacao))

        # remove espaços iniciais
        linha_sem_indent = linha.lstrip()

        for match in re.finditer(regex, linha_sem_indent):

            tipo = match.lastgroup
            valor = match.group()

            if tipo == 'ESPACO':

                continue

            # gera erro

            elif tipo == 'ERRO':

                print(f'Erro léxico: símbolo inválido "{valor}"')

            else:

                tokens.append((tipo, valor))

        # fim da linha
        tokens.append(('NOVA_LINHA', '\\n'))


    while len(pilha_indentacao) > 1:
        
        pilha_indentacao.pop()
        tokens.append(('DEDENT', 0))

    return tokens
