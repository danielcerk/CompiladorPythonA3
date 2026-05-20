from compiler import ( 
    
    lexico, 
    sintatico, 
    semantico

)


def main():

    with open('codigo.txt', 'r', encoding='utf-8') as file:

        codigo_fonte = file.read()

    print('análise léxica')

    tokens = lexico.analisador_lexico(codigo_fonte)

    for token in tokens:

        print(token)

    print('análise sintática')

    try:

        ast = sintatico.parser(tokens)

        print('AST gerada com sucesso.')

    except Exception as erro:

        print(f'Erro sintático: {erro}')
        return

    print('Geração de AST')

    try:

        sintatico.gerar_ast(ast)

    except Exception as erro:

        print(f'Erro ao gerar AST: {erro}')

    print('PArte análise semântica')

    try:

        semantico.analisador_semantico(tokens)

    except Exception as erro:

        print(f'Erro semântico: {erro}')


if __name__ == '__main__':

    main()