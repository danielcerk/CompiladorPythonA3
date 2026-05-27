import re

# definição de tokens



TOKENS = [
    ('NUMERO', r'\d+(\.\d+)?'),
    ('IGUAL_IGUAL', r'=='),
    ('DIFERENTE', r'!='),
    ('MAIOR_IGUAL', r'>='),
    ('MENOR_IGUAL', r'<='),
    ('INCREMENTA_ATRIBUICAO', r'\+='),
    ('DECREMENTA_ATRIBUICAO', r'\-='),
    ('MAIOR', r'>'),
    ('MENOR', r'<'),
    ('SOMA', r'\+'),
    ('SUBTRACAO', r'-'),
    ('MULTIPLICACAO', r'\*'),
    ('DIVISAO', r'/'),
    ('ATRIBUICAO', r'='),
    ('DOIS_PONTOS', r':'),
    ('VIRGULA', r','),
    ('ABRE_PAR', r'\('),
    ('FECHA_PAR', r'\)'),
    ('COMENTARIO', r'\#.*'),
    ('DEF', r'\bdef\b'),
    ('IF', r'\bif\b'),
    ('ELIF', r'\belif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),
    ('FOR', r'\bfor\b'),
    ('RETURN', r'\breturn\b'),
    ('AND', r'\band\b'),
    ('OR', r'\bor\b'),
    ('NOT', r'\bnot\b'),
    ('IN', r'\bin\b'),
    ('TRUE', r'\bTrue\b'),
    ('FALSE', r'\bFalse\b'),
    ('NONE', r'\bNone\b'),
    (
        'STRING',
        r"'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\"|'[^'\n]*'|\"[^\"\n]*\""
    ),
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

    for numero_linha, linha in enumerate(linhas, start=1):

        # ignora linhas vazias
        if linha.strip() == '':

            continue

        indentacao = len(linha) - len(linha.lstrip(' '))

        # INDENT
        if indentacao > pilha_indentacao[-1]:

            pilha_indentacao.append(
                indentacao
            )

            tokens.append(('INDENT',indentacao, numero_linha))

        # DEDENT
        while (indentacao < pilha_indentacao[-1]):

            pilha_indentacao.pop()

            tokens.append(('DEDENT',indentacao,numero_linha))

        linha_sem_indent = linha.lstrip()

        for match in re.finditer(regex, linha_sem_indent):

            tipo = match.lastgroup
            valor = match.group()

            if tipo in ('ESPACO','COMENTARIO'):

                continue

            elif tipo == 'ERRO':

                print(
                    f'Erro léxico '
                    f'( Linha {numero_linha} ): '
                    f'símbolo inválido "{valor}"'
                )

            else:

                tokens.append((tipo, valor, numero_linha))

        tokens.append(('NOVA_LINHA','\\n',numero_linha))

    while len(pilha_indentacao) > 1:

        pilha_indentacao.pop()

        tokens.append(('DEDENT', 0, numero_linha ))

    return tokens