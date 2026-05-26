# Mini-python

A3

## Pré-requisitos

Tecnologias necessárias:

- Python

## Clonando o repositório

```bash
git clone https://github.com/danielcerk/CompiladorPythonA3.git
cd CompiladorPythonA3
```

## Criando ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Instalando dependências

```bash
pip install -r requirements.txt
```

## Executando o projeto

```bash
python main.py
```

# Casos de teste

Os exemplos abaixo podem ser usados para validar o compilador.

---

## Casos válidos

### 1. Atribuição e chamada de função

```python
def teste_lexico():

    codigo = 'ola mundo'

    print(codigo)
```

Resultado esperado:

- análise léxica sem erros
- análise sintática gera AST
- análise semântica sem erros

---

### 2. Operação aritmética

```python
def soma():

    x = 10

    y = 20

    total = x + y

    print(total)
```

Resultado esperado:

- tokens reconhecidos corretamente
- AST com `BinOp (+)`
- sem erros semânticos

---

### 3. If simples

```python
def teste_if():

    codigo = 10

    if codigo < 20:

        print('menor')

    print(codigo)
```

Resultado esperado:

- `IF`
- `MENOR`
- `INDENT / DEDENT`
- AST com nó `If`

---

### 4. While

```python
def contador():

    numero = 0

    while numero < 3:

        print(numero)

        numero = numero + 1
```

Resultado esperado:

- `WHILE`
- comparação `<`
- AST com nó `While`

---

### 5. If + elif + else

```python
def validar():

    numero = 10

    if numero < 10:

        print('menor')

    elif numero == 10:

        print('igual')

    else:

        print('maior')
```

Resultado esperado:

- reconhecimento de `if`
- `elif`
- `else`
- AST completa

---

## Casos inválidos

### 1. Erro léxico — símbolo inválido

```python
def erro():

    valor = @
```

Resultado esperado:

```text
Erro léxico ( Linha 3 ): símbolo inválido "@"
```

---

### 2. Erro léxico — string não reconhecida

```python
def erro():

    texto = 'ola
#########################
def teste()

    print('ola')
##########################
def teste():

    print('ola'
##########################
def teste():

print('ola')
##########################
def teste():

    print(codigo)
```